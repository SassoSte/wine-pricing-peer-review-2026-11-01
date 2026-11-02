"""Provisional preference fit, revision E.

Baseline lightness: one point per 5 lb; sparse context adjustments may alter it. Numerical coefficients are a feasible calibration,
not uniquely inferred prices. See comparisons.json for observed constraints.
Shade/age values and unobserved combinations remain provisional.
"""
from __future__ import annotations
import json
from itertools import product
from pathlib import Path

SPEC_PATH = Path(__file__).resolve().parent / "spec.json"
COMPARISONS_PATH = SPEC_PATH.with_name("comparisons.json")
SHADES = ("brown", "copper", "amber", "golden", "pale/straw")
VINTAGES = (40, 35, 30, 25, 20)
WEIGHTS = (130, 125, 120, 115, 110)

# Baseline is Eastern Europe. Exact values are provisional except where
# constrained by ties. Older vintage steps = 1; younger steps narrowly > 1.
SHADE_POINTS = dict(zip(SHADES, (0.0, 2.6, 3.6, 4.5, 6.5)))
VINTAGE_POINTS = dict(zip(VINTAGES, (0.0, 1.0, 2.0, 3.1, 4.2)))
# Each tuple follows SHADES. No forced convergence of domestic pale prices.
ORIGIN_POINTS = {
    "West Asia / Middle East": (-0.5, -0.5, -0.5, -0.5, -0.5),
    "South/Eastern Asia": (-0.5, -1.55, -0.5, -0.5, -0.5),
    "West Central Asia": (-1/6, -1.5, -1.4, -1/6, -1/6),
    "Eastern Europe": (0.0, 0.0, 0.0, 0.0, 0.0),
    "Western Europe": (3.0, 0.5, 3.0, 3.0, 3.0),
    "central": (-0.6, 0.6, 0.0, 2.0, 4.0),
    "northeast": (0.5, 0.8, 1.9, 2.25, 4.05),
    "northwest": (1.0, 0.6, 2.8, 3.2, 4.0),
    "southwest": (1.25, 0.8, 1.25, 2.625, 4.1),
    "southeast": (1.0, 0.8, 4.3, 4.0, 4.1),
}
# Sparse provenance/shade/vintage corrections. Coefficients are a feasible
# choice, not measured decimal margins. Unlisted cells keep the baseline.
# Central/brown at 30 years follows the explicit Round 7 correction.
# European golden/20-year corrections jointly implement the observed 5 lb
# tie while retaining younger/lighter-shade ordering and earlier trade-offs.
# Their absolute offsets are provisional; only the relative gap is identified.
VINTAGE_ADJUSTMENTS = {
    ("northwest", "amber"): {40: 0.15, 35: 0.1, 30: 0.0, 25: 1.1, 20: 0.2},
    ("central", "brown"): {40: 0.3, 35: 0.7, 30: 2.2, 25: 2.2, 20: 2.2},
    ("southeast", "pale/straw"): {40: -0.05},
    ("southeast", "brown"): {40: -0.1},
    ("southeast", "amber"): {40: -0.1},
    ("southwest", "amber"): {40: -0.1},
    ("southwest", "pale/straw"): {40: -0.05},
    ("northeast", "golden"): {20: 1.75},
    ("southwest", "golden"): {20: 1.375},
    ("central", "golden"): {20: 1.2},
    ("Eastern Europe", "golden"): {20: 1.2},
    ("Western Europe", "golden"): {20: -0.8},
    ("West Central Asia", "brown"): {30: -1/3},
    ("northeast", "brown"): {30: 0.75},
    ("West Central Asia", "copper"): {40: -0.1},
    ("South/Eastern Asia", "copper"): {40: -0.1},
}


# This narrow interaction is observed across all five allowed tares at 20 years.
# Do not extrapolate the threshold to other ages, shades, or provenances.
def _tare_context(provenance: str, shade: str, vintage_years: int, weight_lb: int) -> float:
    if (provenance == "northeast" and shade == "pale/straw"
            and vintage_years == 20 and weight_lb >= 120):
        return 0.05
    return 0.0


def load_spec(path: Path = SPEC_PATH) -> dict:
    return json.loads(path.read_text())


def _lightness(weight_lb: int) -> float:
    if weight_lb not in WEIGHTS:
        raise ValueError(f"unknown tare {weight_lb}")
    return (130 - weight_lb) / 5


def utility(provenance: str, shade: str, vintage_years: int, weight_lb: int) -> float:
    if provenance not in ORIGIN_POINTS:
        raise ValueError(f"unknown provenance {provenance!r}")
    if shade not in SHADES:
        raise ValueError(f"unknown shade {shade!r}")
    if vintage_years not in VINTAGES:
        raise ValueError(f"unknown vintage {vintage_years}")
    interaction = VINTAGE_ADJUSTMENTS.get((provenance, shade), {}).get(vintage_years, 0.0)
    return (SHADE_POINTS[shade] + VINTAGE_POINTS[vintage_years]
            + ORIGIN_POINTS[provenance][SHADES.index(shade)]
            + interaction + _lightness(weight_lb)
            + _tare_context(provenance, shade, vintage_years, weight_lb))


# Actual extrema of the supported offering: do not retain obsolete fixed
# floor/ceiling identities when new comparisons contradict them.
_GRID = tuple(product(ORIGIN_POINTS, SHADES, VINTAGES, WEIGHTS))
FLOOR_U = min(utility(*option) for option in _GRID)
CEILING_U = max(utility(*option) for option in _GRID)


def quote(
    provenance: str,
    shade: str,
    vintage_years: int,
    weight_lb: int,
    *,
    p_floor: float | None = None,
    p_ceiling: float | None = None,
    spec: dict | None = None,
) -> dict[str, float | None]:
    """Return t from 0 at the floor to 1 at the ceiling, and a price if both anchors are set."""
    if spec is not None:
        _check_against_spec(spec)
    value = utility(provenance, shade, vintage_years, weight_lb)
    index = (value - FLOOR_U) / (CEILING_U - FLOOR_U)
    price = None
    if p_floor is not None or p_ceiling is not None:
        if p_floor is None or p_ceiling is None:
            raise ValueError("set both a floor and a ceiling, or neither")
        if p_floor <= 0 or p_ceiling <= 0:
            raise ValueError("floor and ceiling must be positive")
        if p_floor > p_ceiling:
            raise ValueError("floor cannot exceed ceiling")
        price = p_floor * (p_ceiling / p_floor) ** index
    return {"index": index, "price": price}


def _check_against_spec(spec: dict) -> None:
    variant = spec["variant_stainless_304L"]
    shades = tuple(reversed(variant["products"]))
    if shades != SHADES:
        raise ValueError("shade order in spec does not match the calculator")
    if tuple(reversed(variant["vintages_years"])) != VINTAGES:
        raise ValueError("vintage order in spec does not match the calculator")
    weights = tuple(vessel["tare_lb"] for vessel in reversed(variant["vessels"]))
    if weights != WEIGHTS:
        raise ValueError("tares in spec do not match the calculator")


def _winner(left: float, right: float) -> str:
    if abs(left - right) <= 1e-9:
        return "tie"
    if left > right:
        return "A"
    return "B"


def check_anchors(spec: dict | None = None) -> None:
    """Check every active elicited ranking/tie; exclude deferred/superseded rows."""
    if spec is not None:
        _check_against_spec(spec)
    data = json.loads(COMPARISONS_PATH.read_text())
    ids = [row["id"] for row in data["comparisons"]]
    if len(ids) != len(set(ids)):
        raise AssertionError("duplicate comparison IDs")
    for row in data["comparisons"]:
        if row["status"] != "active":
            continue
        found = _winner(utility(*row["a"]), utility(*row["b"]))
        if found != row["winner"]:
            raise AssertionError(f"{row['id']}: {found}, expected {row['winner']}")
    for option in _GRID:
        index = quote(*option)["index"]
        if not -1e-9 <= index <= 1 + 1e-9:
            raise AssertionError(f"index outside [0, 1]: {option}")


    # Test every tare now that a provenance-specific tare interaction exists.
    # These remain model assumptions, not additional elicited comparisons.
    for zone, shade, year, weight in _GRID:
        value = utility(zone, shade, year, weight)
        if weight > 110 and utility(zone, shade, year, weight - 5) <= value:
            raise AssertionError(f"lighter tare ordering failed: {zone}, {shade}, {year}, {weight}")
        if year > 20 and utility(zone, shade, year - 5, weight) <= value:
            raise AssertionError(f"younger ordering failed: {zone}, {shade}, {year}, {weight}")
        shade_index = SHADES.index(shade)
        if shade_index < len(SHADES) - 1:
            if utility(zone, SHADES[shade_index + 1], year, weight) <= value:
                raise AssertionError(f"lighter shade ordering failed: {zone}, {shade}, {year}, {weight}")



if __name__ == "__main__":
    check_anchors(load_spec())
    rows = json.loads(COMPARISONS_PATH.read_text())["comparisons"]
    print(f"Passed {sum(r['status'] == 'active' for r in rows)} active comparisons; "
          f"checked {len(_GRID)} offering combinations")
