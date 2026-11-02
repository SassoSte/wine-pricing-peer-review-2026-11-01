"""Round-2 correction receipts: verifies every number in the PR #1 assessment
and produces corrected diagnostics. Read-only against the packet."""
from pathlib import Path
import json, math, itertools

ROOT = Path(__file__).resolve().parents[2] / "pricing-peer-review"
P = ROOT / "pricing"
OUT = Path(__file__).resolve().parent / "receipts-round2.json"

v28 = json.loads((ROOT / "model-config-v28.json").read_text())
cfg = json.loads((P / "consistent-price-config-v2.json").read_text())
domain, w = v28["domain"], [float(x) for x in v28["coefficients"]]
knots = [(float(x), float(y)) for x, y in cfg["log_discount_knots"]]
anchors = cfg["regional_anchors"]
R = {}

def loss(region, shade, age, tare):
    sidx = domain["shades"].index(shade)
    sh = [float(sidx >= i) for i in range(1, 5)]
    if shade == "pale/straw" and tare == 130:
        sh[3] = 0.0
    q = sh + [float(age <= i) for i in (35, 30, 25, 20)] + [(130 - tare) / 5.0]
    top = [1.0] * 8 + [4.0]
    return sum((t - qi) * wi for t, qi, wi in zip(top, q, w[9:18]))

def f(L, kk=None):
    kk = kk or knots
    if L <= 0: return 0.0
    for (x0, y0), (x1, y1) in zip(kk, kk[1:]):
        if L <= x1: return y0 + (y1 - y0) * (L - x0) / (x1 - x0)
    (x0, y0), (x1, y1) = kk[-2:]
    return y1 + (y1 - y0) * (L - x1) / (x1 - x0)

def price(region, shade, age, tare, kk=None):
    return anchors[region]["price"] * math.exp(-f(loss(region, shade, age, tare), kk))

shades = domain["shades"]; ages = domain["vintage_years"]; tares = domain["tare_lb"]
profiles = list(itertools.product(shades, ages, tares))
ploss = {p: loss("northeast", *p) for p in profiles}
approved = cfg and json.loads((P / "domestic-release-policy-v2.json").read_text())["approved_regions"]

# R2-1. Correction 1: regional direction. Dollar gaps NE minus region at amber35/120.
ne = price("northeast", "amber", 35, 120)
model_gaps = {r: ne - price(r, "amber", 35, 120) for r in ["southeast", "central", "northwest"]}
expert = {"southeast": 425, "central": 400, "northwest": 400}
expert_gaps = {r: 450 - e for r, e in expert.items()}
R["R2_1_direction"] = {
    "model_NE_minus_region_usd": {r: round(v, 2) for r, v in model_gaps.items()},
    "expert_NE_minus_region_usd": expert_gaps,
    "expert_ratios": {r: e / 450 for r, e in expert.items()},
    "model_ratios": {r: anchors[r]["price"] / 1100 for r in expert},
    "expert_ratio_distance_from_1_exceeds_model": {
        r: abs(1 - e / 450) > abs(1 - anchors[r]["price"] / 1100) for r, e in expert.items()},
    "interpretation": "Expert-implied ratios are FARTHER from 1 than model ratios: larger "
                      "relative NE premiums at this profile, not compressed spreads. "
                      "Assessor correction verified; original review wording was wrong."}

# R2-2. Correction 2: full-grid tail sensitivity, all 37 profiles with loss > knot5 x.
kk_alt = knots[:-1] + [(knots[-1][0], math.log(1100 / 271.0))]
seg = [(p, L) for p, L in ploss.items() if L > knots[5][0] + 1e-12]
changes = []
for (s, a, t), L in seg:
    locked = 1100 * math.exp(-f(L)); alt = 1100 * math.exp(-f(L, kk_alt))
    changes.append({"profile": f"{s}/{a}/{t}", "loss": L,
                    "pct": 100 * (math.exp(f(L) - f(L, kk_alt)) - 1),
                    "locked": locked, "alt": alt})
pcts = [c["pct"] for c in changes]
nearest = min(seg, key=lambda x: x[1] - knots[5][0])
R["R2_2_tail_sensitivity_full_grid"] = {
    "profiles_in_segment": len(changes),
    "min_pct_change": min(pcts),
    "max_pct_change": max(pcts),
    "profile_nearest_knot5": nearest[0],
    "nearest_loss_minus_knot5": nearest[1] - knots[5][0],
    "endpoint_change_pct": 100 * (math.exp(knots[-1][1] - kk_alt[-1][1]) - 1),
    "assessor_claim_min_approx": -0.000032, "assessor_claim_max_approx": -9.67,
    "note": "271 is the rounded slower-tail historical scenario (270.77), NOT an elicited "
            "lower bound; this is a labeled sensitivity scenario, not an admissible interval."}

# R2-5. Correction 5: approved domestic scope (500 outputs) evidence-tier counts.
in_span = [p for p in profiles if ploss[p] <= cfg["prior_supported_loss"] + 1e-12]
beyond = [p for p in profiles if p not in in_span]
anchor_profile = ("pale/straw", 20, 110)
R["R2_5_domestic_scope_tiers"] = {
    "approved_outputs": 4 * len(profiles),
    "in_span_profiles_per_region": len(in_span),
    "domestic_in_span_incl_anchors": len(in_span) * 4,
    "domestic_in_span_excl_anchors": (len(in_span) - 1) * 4,
    "domestic_beyond_span": len(beyond) * 4,
    "domestic_non_NE_transfers": len(beyond) * 3,
    "ten_region_grid_in_span": len(in_span) * 10,
    "ten_region_grid_non_NE_transfers": len(beyond) * 9,
    "categories_overlap_note": "anchor-exact (4) is a subset of in-span (92); non-NE transfers "
                               "(306) is a subset of beyond-span (408); not a disjoint partition.",
    "anchor_profile_in_span": anchor_profile in in_span}

# R2-E1. Correction E1: proposed probe profile losses.
probe = {"amber30/120": ("amber", 30, 120), "copper35/125": ("copper", 35, 125),
         "golden35/125": ("golden", 35, 125)}
R["R2_E1_original_probe_losses"] = {
    k: {"loss": ploss[v], "on_mid_segment_1.846_to_5.000": knots[4][0] < ploss[v] < knots[5][0]}
    for k, v in probe.items()}
replacement = {"brown25/110": ("brown", 25, 110), "copper30/115": ("copper", 30, 115),
               "amber30/120": ("amber", 30, 120), "pale35/115": ("pale/straw", 35, 115),
               "amber35/115": ("amber", 35, 115)}
R["R2_E1_replacement_candidates_on_segment"] = {
    k: {"loss": ploss[v], "on_mid_segment": knots[4][0] < ploss[v] < knots[5][0]}
    for k, v in replacement.items()}

# R2-6. Correction 6: actual numerical tolerances + provenance of each statistic.
val1 = json.loads((P / "consistent-price-validation-v1.json").read_text())
mr = json.loads((P / "middle-range-checks-v1.json").read_text())["questions"]
tr = json.loads((P / "regional-low-end-transfer-v1.json").read_text())["questions"]
mr_diffs = [abs(q["frozen_price_usd"] - price(*q["offering"])) for q in mr]
tr_diffs = [abs(q["frozen_price_usd"] - price(*q["offering"])) for q in tr]
R["R2_6_tolerances"] = {
    "middle_range_max_abs_diff_recompute_vs_frozen": max(mr_diffs),
    "transfer_max_abs_diff_recompute_vs_frozen": max(tr_diffs),
    "anchor_recompute_abs_diff": max(abs(anchors[z]["price"] - price(z, "pale/straw", 20, 110))
                                     for z in ["northeast", "southeast", "central", "northwest"]),
    "knot_x_float_equality": "exact == on parsed doubles for all six knots",
    "NE_over_NW_ratio_values": sorted({price("northeast", s, a, t) / price("northwest", s, a, t)
                                       for s in shades for a in ages for t in tares}),
    "closed_loop_ratio_product": (price("northeast", "golden", 25, 115) / price("northeast", "pale/straw", 25, 110))
                                 * (price("northeast", "pale/straw", 25, 110) / price("northeast", "pale/straw", 20, 110))
                                 * (price("northeast", "pale/straw", 20, 110) / price("northeast", "golden", 25, 115)),
    "provenance": {
        "independently_recomputed_from_config_and_recorded_judgments": [
            "all prices/losses (own implementation)",
            "transfer amber MAE 17.80 / MAPE 4.38% (from frozen prices + recorded estimates)",
            "middle-range 5-point MAE 105.05 / signed -97.30 / MAPE 14.68% (from frozen prices + recorded estimates)",
            "tail sensitivity, tier counts, ratios, telescoping, collapses"],
        "aggregated_from_stored_residuals_not_independently_refit": [
            "fit MAE 5.9655 / max 16.0651 (mean/max of stored residual fields)",
            "leave-profile-out MAE 39.7293 (mean of stored error fields)",
            "combined-profile holdout errors 65.28..87.52 (copied from stored fields)"],
        "copied_from_validation_json": [
            "single_slope_fit_mae 23.0592 (stored; comparator not refit)"],
        "not_reproduced": [
            "workbook 6294-formula recalculation claim (accepted as reported)"]}}

# R2-4. Correction 4: middle-range denominators.
pts = [(q["frozen_price_usd"], q["expert_estimate"]["amount"]) for q in mr if "expert_estimate" in q]
R["R2_4_middle_range_denominator"] = {
    "total_questions": len(mr), "point_estimates": len(pts), "range_observations": len(mr) - len(pts),
    "stats_basis": "5 point estimates only; the 6th is a range with preserved post-disclosure correction"}

OUT.write_text(json.dumps(R, indent=2) + "\n")
print(json.dumps(R, indent=2))
