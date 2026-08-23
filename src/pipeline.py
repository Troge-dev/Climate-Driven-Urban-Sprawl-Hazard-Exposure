"""
CDO Urban Sprawl x Hazard Exposure Pipeline
=============================================
Data Mining and Applications - Laboratory Activity 1
Project CCHAIN dataset, filtered to Cagayan de Oro City (80 barangays)

Pipeline stages:
    1. Load & Filter   -> descriptive baseline (hazard, buildings, land cover, wealth, population)
    2. Diagnose         -> growth/hazard/wealth overlap analysis
    3. Predict           -> 2030 population growth projection per barangay
    4. Prescribe         -> composite risk score + priority tiering

Run:
    python src/pipeline.py
"""

import os
import pandas as pd
import numpy as np

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "cchain_raw")
PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")
CITY_NAME = "Cagayan de Oro City"


# ---------------------------------------------------------------------------
# STAGE 1: LOAD & FILTER (Descriptive foundation)
# ---------------------------------------------------------------------------

def load_cdo_codes():
    """Return the set of adm4_pcode values for CDO's 80 barangays, plus a
    lookup table of pcode -> barangay name."""
    loc = pd.read_csv(os.path.join(RAW_DIR, "location.csv"))
    cdo = loc[loc["adm3_en"] == CITY_NAME].copy()
    lookup = cdo[["adm4_pcode", "adm4_en"]].drop_duplicates()
    return set(cdo["adm4_pcode"]), lookup


def load_static_table(filename, value_cols, cdo_codes):
    """Load a single-snapshot CCHAIN table, filter to CDO, keep id + value cols."""
    df = pd.read_csv(os.path.join(RAW_DIR, filename))
    df = df[df["adm4_pcode"].isin(cdo_codes)].copy()
    keep = ["adm4_pcode"] + value_cols
    return df[keep]


def load_hazard(cdo_codes):
    cols = [
        "pct_area_flood_hazard_100yr_high", "pct_area_flood_hazard_25yr_high",
        "pct_area_flood_hazard_5yr_high", "pct_area_landslide_hazard_high",
        "pct_area_landslide_hazard_med",
    ]
    return load_static_table("project_noah_hazards.csv", cols, cdo_codes)


def load_buildings(cdo_codes):
    cols = [
        "google_bldgs_count", "google_bldgs_density",
        "google_bldgs_pct_built_up_area", "google_bldgs_count_lt100_sqm",
    ]
    return load_static_table("google_open_buildings.csv", cols, cdo_codes)


def load_landcover(cdo_codes):
    cols = ["pct_area_builtup", "pct_area_tree_cover", "pct_area_cropland"]
    return load_static_table("esa_worldcover.csv", cols, cdo_codes)


def load_wealth_latest(cdo_codes):
    """tm_relative_wealth_index has 7 yearly snapshots (2016-2022). Keep the
    latest year per barangay as the 'current' wealth read, and separately
    compute the wealth trend (2016 -> 2022 delta) for diagnostics."""
    df = pd.read_csv(os.path.join(RAW_DIR, "tm_relative_wealth_index.csv"))
    df = df[df["adm4_pcode"].isin(cdo_codes)].copy()
    df["date"] = pd.to_datetime(df["date"])

    latest = (
        df.sort_values("date")
        .groupby("adm4_pcode")
        .tail(1)[["adm4_pcode", "rwi_mean"]]
        .rename(columns={"rwi_mean": "rwi_latest"})
    )

    first = df.sort_values("date").groupby("adm4_pcode").head(1)[["adm4_pcode", "rwi_mean"]]
    first = first.rename(columns={"rwi_mean": "rwi_first"})
    trend = latest.merge(first, on="adm4_pcode")
    trend["rwi_trend"] = trend["rwi_latest"] - trend["rwi_first"]
    return trend[["adm4_pcode", "rwi_latest", "rwi_trend"]]


def load_population_trend(cdo_codes):
    """worldpop_population has 21 yearly snapshots (2000-2020). Compute total
    population at first/last available year and a compound annual growth
    rate (CAGR) per barangay -- this is the real time-series evidence for
    'sprawl' since building/hazard/land-cover tables are single snapshots."""
    df = pd.read_csv(os.path.join(RAW_DIR, "worldpop_population.csv"))
    df = df[df["adm4_pcode"].isin(cdo_codes)].copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    first = df.groupby("adm4_pcode").head(1)[["adm4_pcode", "date", "pop_count_total"]]
    first = first.rename(columns={"date": "pop_year_first", "pop_count_total": "pop_first"})
    last = df.groupby("adm4_pcode").tail(1)[["adm4_pcode", "date", "pop_count_total"]]
    last = last.rename(columns={"date": "pop_year_last", "pop_count_total": "pop_last"})

    out = first.merge(last, on="adm4_pcode")
    n_years = (out["pop_year_last"].dt.year - out["pop_year_first"].dt.year).clip(lower=1)
    # Compound annual growth rate; guard against zero/negative starting pop
    safe_first = out["pop_first"].replace(0, np.nan)
    out["pop_cagr"] = (out["pop_last"] / safe_first) ** (1 / n_years) - 1
    out["pop_cagr"] = out["pop_cagr"].fillna(0)
    return out[["adm4_pcode", "pop_first", "pop_last", "pop_cagr"]]


# ---------------------------------------------------------------------------
# STAGE 2: DIAGNOSE + STAGE 3: PREDICT (feature engineering)
# ---------------------------------------------------------------------------

def build_master_table():
    cdo_codes, lookup = load_cdo_codes()

    hazard = load_hazard(cdo_codes)
    buildings = load_buildings(cdo_codes)
    landcover = load_landcover(cdo_codes)
    wealth = load_wealth_latest(cdo_codes)
    pop = load_population_trend(cdo_codes)

    df = lookup.merge(hazard, on="adm4_pcode", how="left")
    df = df.merge(buildings, on="adm4_pcode", how="left")
    df = df.merge(landcover, on="adm4_pcode", how="left")
    df = df.merge(wealth, on="adm4_pcode", how="left")
    df = df.merge(pop, on="adm4_pcode", how="left")

    # Composite hazard exposure (0-1): worst-case flood + landslide high-risk share
    df["hazard_exposure"] = (
        df[["pct_area_flood_hazard_100yr_high", "pct_area_landslide_hazard_high"]]
        .fillna(0)
        .sum(axis=1)
    )

    # Predictive: projected 2030 population using each barangay's own CAGR
    LAST_YEAR = 2020
    TARGET_YEAR = 2030
    years_out = TARGET_YEAR - LAST_YEAR
    df["pop_projected_2030"] = df["pop_last"] * (1 + df["pop_cagr"]).pow(years_out)
    df["projected_growth_pct"] = (df["pop_projected_2030"] / df["pop_last"] - 1) * 100

    return df


# ---------------------------------------------------------------------------
# STAGE 4: PRESCRIBE (composite risk score + tiering)
# ---------------------------------------------------------------------------

def minmax(s):
    s = s.fillna(0)
    rng = s.max() - s.min()
    if rng == 0:
        return s * 0
    return (s - s.min()) / rng


def score_and_rank(df):
    df = df.copy()
    hz = minmax(df["hazard_exposure"])
    growth = minmax(df["pop_cagr"].clip(lower=0))
    density = minmax(df["google_bldgs_density"])
    inv_wealth = 1 - minmax(df["rwi_latest"])  # lower wealth -> higher score

    # Weighted composite: hazard and growth matter most for a "sprawl into
    # danger" story; density and inverse wealth add informal-settlement signal
    df["risk_score"] = (
        0.40 * hz + 0.30 * growth + 0.15 * density + 0.15 * inv_wealth
    )

    df["risk_tier"] = pd.cut(
        df["risk_score"],
        bins=[-0.01, 0.33, 0.60, 1.01],
        labels=["Tier 1: Monitor", "Tier 2: Priority Mitigation", "Tier 3: Critical Intervention"],
    )

    return df.sort_values("risk_score", ascending=False).reset_index(drop=True)


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def run():
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    master = build_master_table()
    scored = score_and_rank(master)

    out_path = os.path.join(PROCESSED_DIR, "cdo_sprawl_hazard_ready.csv")
    scored.to_csv(out_path, index=False)

    print(f"Processed {len(scored)} CDO barangays -> {out_path}")
    print("\nTop 10 highest-risk barangays:")
    print(
        scored[["adm4_en", "hazard_exposure", "pop_cagr", "rwi_latest", "risk_score", "risk_tier"]]
        .head(10)
        .to_string(index=False)
    )
    return scored


if __name__ == "__main__":
    run()
