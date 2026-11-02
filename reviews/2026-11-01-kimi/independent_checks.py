"""Independent reviewer diagnostics for Domestic Release Pricing v2.

Read-only. Reimplements the loss coordinate and log-discount curve from the
published description (pricing-peer-review.md section 4) WITHOUT importing the
packet's pricing modules, then cross-checks every quantitative claim the
reviewer could verify. Writes receipts.json next to this script.
"""
from pathlib import Path
import json, math, hashlib, itertools
import numpy as np

ROOT = Path(__file__).resolve().parents[2] / "pricing-peer-review"
P = ROOT / "pricing"
OUT = Path(__file__).resolve().parent / "receipts.json"

v28 = json.loads((ROOT / "model-config-v28.json").read_text())
cfg = json.loads((P / "consistent-price-config-v2.json").read_text())
domain, w = v28["domain"], [float(x) for x in v28["coefficients"]]
knots = [(float(x), float(y)) for x, y in cfg["log_discount_knots"]]
anchors = cfg["regional_anchors"]
R = {}

# --- independent reimplementation of the spec ---
def loss(region, shade, age, tare):
    sidx = domain["shades"].index(shade)
    sh = [float(sidx >= i) for i in range(1, 5)]
    if shade == "pale/straw" and tare == 130:
        sh[3] = 0.0
    q = sh + [float(age <= i) for i in (35, 30, 25, 20)] + [(130 - tare) / 5.0]
    top = [1.0] * 8 + [4.0]
    return sum((t - qi) * wi for t, qi, wi in zip(top, q, w[9:18]))

def f(L):
    if L <= 0:
        return 0.0
    for (x0, y0), (x1, y1) in zip(knots, knots[1:]):
        if L <= x1:
            return y0 + (y1 - y0) * (L - x0) / (x1 - x0)
    (x0, y0), (x1, y1) = knots[-2:]
    return y1 + (y1 - y0) * (L - x1) / (x1 - x0)

def price(region, shade, age, tare):
    return anchors[region]["price"] * math.exp(-f(loss(region, shade, age, tare)))

shades = domain["shades"]; ages = domain["vintage_years"]; tares = domain["tare_lb"]
grid = list(itertools.product(domain["provenances"], shades, ages, tares))

# A. weight provenance and nonnegativity
R["A_weights_match_v28"] = cfg["base_coefficients"] == v28["coefficients"]
R["A_loss_weights_nonneg"] = all(x >= 0 for x in w[9:18])
R["A_loss_weights"] = w[9:18]

# B. knot x-values are exactly the losses of the claimed profiles
claimed = {
    "knot1 golden20/110": ("northeast", "golden", 20, 110),
    "knot2 pale20/115": ("northeast", "pale/straw", 20, 115),
    "knot3 pale25/110": ("northeast", "pale/straw", 25, 110),
    "knot4 golden25/115": ("northeast", "golden", 25, 115),
    "knot5 amber35/120": ("northeast", "amber", 35, 120),
    "knot6 brown40/130": ("northeast", "brown", 40, 130),
}
R["B_knot_profile_losses"] = {
    k: {"loss": loss(*v), "knot_x": knots[i + 1][0],
        "exact_float_equal": loss(*v) == knots[i + 1][0]}
    for i, (k, v) in enumerate(claimed.items())
}

# C. endpoint construction and the one-ULP claim
ln_450 = math.log(1100 / 450.0)
ln_300 = math.log(1100 / 300.0)
R["C_knot5_y_equals_ln1100_450"] = knots[5][1] == ln_450
R["C_knot6_y_equals_nextafter_ln1100_300"] = knots[6][1] == float(np.nextafter(ln_300, np.inf))
R["C_ne_brown40_130_price_locked"] = 1100 * math.exp(-knots[6][1])
R["C_ne_brown40_130_price_without_ulp"] = 1100 * math.exp(-ln_300)
R["C_overshoot_without_ulp"] = 1100 * math.exp(-ln_300) > 300.0
R["C_ne_amber35_120_price_locked"] = 1100 * math.exp(-knots[5][1])

# D. grid coverage: no extrapolation beyond final knot; span bookkeeping
losses = [loss(*o) for o in grid]
R["D_max_grid_loss_equals_final_knot"] = max(losses) == knots[-1][0]
R["D_min_grid_loss"] = min(losses)
distinct = sorted(set(losses))
profiles = list(itertools.product(shades, ages, tares))  # 125 attribute profiles
ploss = [loss("northeast", s, a, t) for s, a, t in profiles]
prior_span = cfg["prior_supported_loss"]
in_span_profiles = sum(1 for L in ploss if L <= prior_span + 1e-12)
R["D_distinct_loss_values"] = len(distinct)
R["D_attribute_profiles_total"] = len(profiles)
R["D_profiles_within_prior_span"] = in_span_profiles
R["D_profiles_beyond_prior_span"] = len(profiles) - in_span_profiles
R["D_in_span_prices_10_regions"] = in_span_profiles * 10
R["D_non_NE_transfer_profiles"] = (len(profiles) - in_span_profiles) * 9
R["D_on_grid_extrapolations"] = sum(1 for L in losses if L > knots[-1][0] + 1e-12)

# E. structural collapses of the loss coordinate
amber_golden_identical = all(
    abs(price(z, "amber", a, t) - price(z, "golden", a, t)) < 1e-9
    for z in domain["provenances"] for a in ages for t in tares)
pale_golden_130 = all(
    abs(price(z, "pale/straw", a, 130) - price(z, "golden", a, 130)) < 1e-9
    for z in domain["provenances"] for a in ages)
R["E_amber_equals_golden_all_vintages_tares"] = amber_golden_identical
R["E_pale_equals_golden_at_130lb"] = pale_golden_130
R["E_distinct_prices_per_region"] = len({round(price("northeast", s, a, t), 9)
                                         for s in shades for a in ages for t in tares})
R["E_golden_to_pale_increment_usd_at_top_ne"] = 1100 - price("northeast", "golden", 20, 110)

# F. reproduce frozen values from evidence files (own math vs recorded numbers)
def check_file(fname, price_key, offering_key="offering"):
    data = json.loads((P / fname).read_text())
    rows = []
    for q in data.get("checks", data.get("questions", [])):
        o = q[offering_key]
        mine = price(*o)
        rec = q.get(price_key)
        rows.append({"id": q.get("id", q.get("number")), "recorded": rec,
                     "recomputed": mine,
                     "match": (rec is not None and abs(mine - rec) < 1e-6)})
    return rows

R["F_anchors"] = {z: {"recorded": anchors[z]["price"],
                      "recomputed": price(z, "pale/straw", 20, 110)}
                  for z in ["northeast", "southeast", "central", "northwest"]}
# low-end scenarios are old tail values; constraints verified directly instead
R["F_low_end_constraints"] = {
    "ne_amber35_120_target_450": price("northeast", "amber", 35, 120),
    "ne_brown40_130_target_300_ceiling": price("northeast", "brown", 40, 130)}
R["F_regional_transfer"] = check_file("regional-low-end-transfer-v1.json", "frozen_price_usd")
R["F_middle_range"] = check_file("middle-range-checks-v1.json", "frozen_price_usd")

# G. independently recompute the published summary statistics
tr = R["F_regional_transfer"]
amber = [r for r in tr if "amber" in r["id"]]
est = {"northwest-amber-35-120": 400, "southeast-amber-35-120": 425, "central-amber-35-120": 400}
diffs = [abs(r["recomputed"] - est[r["id"]]) for r in amber]
pcts = [abs(r["recomputed"] - est[r["id"]]) / est[r["id"]] * 100 for r in amber]
R["G_transfer_amber_MAE"] = sum(diffs) / 3
R["G_transfer_amber_MAPE_pct"] = sum(pcts) / 3
R["G_transfer_all_predictions_high"] = all(r["recomputed"] > est[r["id"]] for r in amber)
R["G_transfer_expert_implied_regional_ratios_vs_model"] = {
    "SE/NE": {"expert": 425 / 450, "model": 1075 / 1100},
    "Central/NE": {"expert": 400 / 450, "model": 1050 / 1100},
    "NW/NE": {"expert": 400 / 450, "model": 1000 / 1100},
}

mr = json.loads((P / "middle-range-checks-v1.json").read_text())["questions"]
pts = [(q["frozen_price_usd"], q["expert_estimate"]["amount"])
       for q in mr if "expert_estimate" in q]
d = [m - e for m, e in pts]
R["G_middle_MAE_5pts"] = sum(abs(x) for x in d) / len(d)
R["G_middle_signed"] = sum(d) / len(d)
R["G_middle_MAPE_pct"] = sum(abs(m - e) / e * 100 for m, e in pts) / len(pts)
R["G_middle_n_underestimates"] = sum(1 for x in d if x < 0)

# G2. calibration circularity quantification (v1 fit targets)
val1 = json.loads((P / "consistent-price-validation-v1.json").read_text())
fits = val1["fit_observations"]
R["G2_fit_MAE_stored"] = val1["fit_mae"]
R["G2_fit_MAE_recomputed"] = float(np.mean([abs(x["residual"]) for x in fits]))
R["G2_fit_max_abs_stored"] = val1["fit_max_absolute_error"]
R["G2_single_slope_MAE_stored"] = val1["single_slope_fit_mae"]
R["G2_lopo_MAE_stored"] = val1["leave_profile_out_mae"]
R["G2_lopo_MAE_recomputed"] = float(np.mean([abs(x["error"]) for x in val1["leave_profile_out"]]))
comb = [x for x in val1["leave_profile_out"] if x["heldout_profile"] == ["golden", 25, 115] or
        tuple(x["heldout_profile"]) == ("golden", 25, 115)]
R["G2_combined_profile_holdout_errors"] = [round(x["error"], 2) for x in comb]
indep = json.loads((P / "independent-checks-v2.json").read_text())["checks"]
circ = []
for q in indep:
    tgt = round(q["frozen_estimate"])
    match = [x for x in fits if x["id"] == q["id"]]
    circ.append({"id": q["id"], "calibration_target": match[0]["accepted_price"] if match else None,
                 "rounded_model_frozen_estimate": tgt,
                 "target_is_rounded_model_output": bool(match and match[0]["accepted_price"] == tgt),
                 "fit_residual": match[0]["residual"] if match else None})
R["G2_self_referential_targets"] = circ
resid_circ = [abs(c["fit_residual"]) for c in circ if c["fit_residual"] is not None]
resid_other = [abs(x["residual"]) for x in fits if x["source"] == "valuation-checks-v1.json"]
R["G2_MAE_self_referential_subset"] = float(np.mean(resid_circ))
R["G2_MAE_remaining_subset"] = float(np.mean(resid_other))

# H. regional ratio constancy (structural)
ratios = {price(z, s, a, t) / price("northwest", s, a, t)
          for z in ["northeast"] for s in shades for a in ages for t in tares}
R["H_NE_over_NW_ratio_set"] = sorted(ratios)

# I. telescoping / closed-loop ratios with own implementation
a = price("northeast", "golden", 25, 115); b = price("northeast", "pale/straw", 25, 110)
c = price("northeast", "pale/straw", 20, 110)
R["I_telescoping_residual"] = (a - b) + (b - c) - (a - c)
R["I_closed_loop_ratio"] = (a / b) * (b / c) * (c / a)

# J. tail sensitivity illustration (what-if; packet untouched):
# replace ONLY the final knot's y so NE brown40/130 = 271 (slower-tail value the
# expert ceiling also permitted) and recompute deep-tail NE prices.
knots_alt = knots[:-1] + [(knots[-1][0], math.log(1100 / 271.0))]
def f_alt(L):
    if L <= 0: return 0.0
    for (x0, y0), (x1, y1) in zip(knots_alt, knots_alt[1:]):
        if L <= x1: return y0 + (y1 - y0) * (L - x0) / (x1 - x0)
    (x0, y0), (x1, y1) = knots_alt[-2:]
    return y1 + (y1 - y0) * (L - x1) / (x1 - x0)
sens = {}
for s_, a_, t_ in [("brown", 40, 130), ("copper", 40, 130), ("brown", 35, 125), ("amber", 40, 125), ("brown", 40, 120)]:
    L = loss("northeast", s_, a_, t_)
    if L > knots[4][0]:
        locked = 1100 * math.exp(-f(L)); alt = 1100 * math.exp(-f_alt(L))
        sens[f"ne-{s_}-{a_}-{t_}"] = {"loss": round(L, 6), "locked": round(locked, 2),
                                      "alt_tail_271": round(alt, 2),
                                      "pct_change": round((alt - locked) / locked * 100, 2)}
R["J_tail_sensitivity_endpoint_271_vs_300"] = sens

# K. low-end segment span: the 450->300 segment governs everything between losses
R["K_deep_tail_segment_span"] = {"from_loss": knots[5][0], "to_loss": knots[6][0],
                                 "profiles_in_segment": sum(1 for L in ploss if knots[5][0] < L <= knots[6][0])}
R["K_mid_segment_span"] = {"from_loss": knots[4][0], "to_loss": knots[5][0],
                           "profiles_in_segment": sum(1 for L in ploss if knots[4][0] < L < knots[5][0])}

# L. packet checksums
R["L_zip_sha256"] = hashlib.sha256((ROOT.parent / "pricing-peer-review-v2.zip").read_bytes()).hexdigest()
R["L_config_v2_sha256"] = hashlib.sha256((P / "consistent-price-config-v2.json").read_bytes()).hexdigest()

OUT.write_text(json.dumps(R, indent=2) + "\n")
print(json.dumps(R, indent=2))
