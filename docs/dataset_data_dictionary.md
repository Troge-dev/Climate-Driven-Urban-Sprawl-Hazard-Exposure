# Data Dictionary — CDO Sprawl x Hazard Pipeline

All source tables are from [Project CCHAIN](https://www.kaggle.com/datasets/thinkdatasci/project-cchain), filtered to Cagayan de Oro City's 80 barangays via `adm4_pcode`.

## Raw tables used

| Table | Frequency | Coverage (CDO) | Key columns used |
|---|---|---|---|
| `location.csv` | static | 80 rows | `adm4_pcode`, `adm4_en`, `adm3_en` — used to filter to CDO and get barangay names |
| `brgy_geography.csv` | static (2003) | 80 rows | `geometry` (WKT polygon) — used for the risk map |
| `project_noah_hazards.csv` | static (2015) | 80 rows | `pct_area_flood_hazard_{5,25,100}yr_high`, `pct_area_landslide_hazard_{med,high}` |
| `google_open_buildings.csv` | static (2023) | 80 rows | `google_bldgs_count`, `google_bldgs_density`, `google_bldgs_pct_built_up_area`, `google_bldgs_count_lt100_sqm` |
| `esa_worldcover.csv` | static (2021) | 80 rows | `pct_area_builtup`, `pct_area_tree_cover`, `pct_area_cropland` |
| `tm_relative_wealth_index.csv` | yearly (2016–2022) | 560 rows | `rwi_mean` — latest year kept as current wealth; first vs. latest kept as trend |
| `worldpop_population.csv` | yearly (2000–2020) | 1,680 rows | `pop_count_total` — first vs. last year used to compute CAGR |
| `calendar.csv` | — | not used directly | standard date reference table, not joined |

## Engineered fields (in `data/processed/cdo_sprawl_hazard_ready.csv`)

| Column | Description |
|---|---|
| `hazard_exposure` | Sum of `pct_area_flood_hazard_100yr_high` + `pct_area_landslide_hazard_high` (0–100 scale, higher = more of the barangay's land area sits in high-risk zones) |
| `pop_first`, `pop_last` | Population at the barangay's first and last available WorldPop years |
| `pop_cagr` | Compound annual growth rate, `(pop_last / pop_first)^(1/years) - 1` |
| `pop_projected_2030` | `pop_last` compounded forward at `pop_cagr` to the year 2030 |
| `projected_growth_pct` | Percent growth implied by `pop_projected_2030` vs. `pop_last` |
| `rwi_latest` | Most recent available Relative Wealth Index mean for the barangay |
| `rwi_trend` | `rwi_latest - rwi_first` (change in wealth index since 2016) |
| `risk_score` | Composite 0–1 score: `0.40×hazard + 0.30×growth + 0.15×building_density + 0.15×inverse_wealth`, each min-max normalized across the 80 CDO barangays |
| `risk_tier` | `risk_score` bucketed into Tier 1 (Monitor, <0.33), Tier 2 (Priority Mitigation, 0.33–0.60), Tier 3 (Critical Intervention, ≥0.60) |

## Known limitations (be ready to defend these)

1. **Not a true multi-year land-use time series.** `google_open_buildings`, `project_noah_hazards`, and `esa_worldcover` are each a single snapshot in CCHAIN — they cannot show buildings or hazard zones *changing* over time. The pipeline treats them as the current exposure baseline and uses population/wealth trends as the actual longitudinal evidence of sprawl.
2. **CAGR extrapolation assumes constant growth.** A 10-year linear-in-log projection is a simplification; real growth is rarely perfectly compounding. This is disclosed in the README as a deliberate, transparent choice for an undergraduate-scope model rather than a full time-series forecast (e.g., ARIMA or Prophet).
3. **Risk score weights are analyst-chosen, not statistically fit.** If challenged in defense, the honest answer is the weights (0.40/0.30/0.15/0.15) reflect a reasoned prioritization (hazard and growth as the two primary drivers of the "sprawl into danger" narrative) rather than a regression-fit set of coefficients — a worthwhile stretch extension would be a sensitivity analysis showing the ranking is stable across a plausible weight range.
