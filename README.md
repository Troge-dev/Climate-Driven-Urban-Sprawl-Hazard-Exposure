# 🏙️ Cagayan de Oro City Urban Sprawl & Hazard Exposure Risk Engine

> **A Spatial Risk-Scoring & Zoning-Priority Tool for the Cagayan de Oro City Local Government Unit (CDO LGU)**
> *Developed for the CDO City Planning and Development Office (CPDO) & City Disaster Risk Reduction and Management Office (CDRRMO)*
> *Pilot City: Cagayan de Oro City, Northern Mindanao, Philippines (80 Barangays | 2000–2023 CCHAIN Extracts)*
>
> 🎓 **Academic Fulfillment:** Data Mining and Applications — Laboratory Activity 1
> 🌐 **Primary Dataset Source:** Project CCHAIN (Kaggle: [`thinkdatasci/project-cchain`](https://www.kaggle.com/datasets/thinkdatasci/project-cchain))

---

> **Course & Data Attribution Notice**
> - **Academic Requirement:** This repository is submitted in fulfillment of Data Mining and Applications, Laboratory Activity 1.
> - **Data Provenance:** All hazard, building, land cover, wealth, and population data used here originate from **Project CCHAIN**, an open-access multi-partner initiative by Thinking Machines, EpiMetrics, Manila Observatory, and PACSII (funded by the Wellcome Trust & Lacuna Fund). 8 raw CCHAIN tables were filtered, joined, and engineered for the 80 barangays of Cagayan de Oro City.

## 1. Project Overview & CDO LGU Operational Problem Statement

Cagayan de Oro City has seen rapid population growth pushing settlement into its floodplains and landslide-prone uplands, yet the city government lacks a data-driven view of exactly **which barangays are absorbing the most growth in already-hazardous zones** — and whether it's lower-income communities bearing disproportionate risk.

Unlike disease-surveillance systems that react to case counts, this project addresses a **structural, slow-moving risk**: unmanaged urban sprawl quietly increasing the city's disaster vulnerability, barangay by barangay, year by year.

### The CDO LGU Risk-Prioritization Solution

This project builds a **barangay-level composite risk score** for CDO's 80 barangays by fusing:
- 20 years of **population growth** trends (WorldPop, 2000–2020)
- **Flood (5/25/100-yr) and landslide hazard exposure** (Project NOAH, 2015 snapshot)
- **Building density and footprint size** (Google Open Buildings, 2023 snapshot)
- **Relative wealth** trends (2016–2022) as an equity lens

This gives the CDO CPDO and CDRRMO a **ranked, defensible priority list** for zoning restriction, relocation planning, and infrastructure-hardening investment — instead of reactive, post-disaster response.

| Stage | Analytics Type | Key Deliverable for CDO LGU |
|---|---|---|
| 1. Baseline & GIS | Descriptive Analytics | Current hazard/building/land-cover profile per barangay |
| 2. Growth × Hazard Overlap | Diagnostic Analytics | Barangays where growth and danger coincide, by wealth tier |
| 3. 2030 Growth Projection | Predictive Analytics | Projected population exposure per barangay |
| 4. Priority Tiering | Prescriptive Analytics | 3-tier zoning/mitigation action matrix |

## 2. Geographic Scope: Cagayan de Oro City's 80 Barangays

All 80 barangays (`PH104305000`) are covered, ranging from dense poblacion barangays near the city center to rural upland barangays like Tignapoloan and Besigan. Barangay boundary polygons (`brgy_geography.csv`) are parsed directly from CCHAIN's WKT geometry to render a true choropleth risk map — no GIS software required.

## 3. Key Findings (from real CDO data)

- **752,064** people lived across CDO's 80 barangays as of the last WorldPop estimate (2020), growing at an average **2.86% CAGR** since 2000.
- **30 of 80 barangays** have more than 20% of their land area classified as high flood or landslide hazard.
- The three highest-risk barangays by composite score are **Barangay 17 (Poblacion)**, **Consolacion**, and **Tignapoloan** — a mix of dense urban-core and rural upland exposure, showing sprawl risk isn't just a downtown problem.
- **Tignapoloan** stands out diagnostically: the fastest-growing barangay in the dataset (**4.27% CAGR**) combined with the lowest wealth index in the top-risk group (**0.32**) — a textbook case of low-income growth outpacing hazard-aware planning.

*(Full ranked table: `data/processed/cdo_sprawl_hazard_ready.csv`)*

## 4. Repository Directory Layout

```
sprawl-repo/
├── data/
│   ├── cchain_raw/                        # 8 raw Project CCHAIN CSVs (location, hazards, buildings, etc.)
│   └── processed/
│       └── cdo_sprawl_hazard_ready.csv    # Final scored & ranked 80-barangay matrix
├── docs/
│   ├── dataset_data_dictionary.md         # Column-level documentation & lineage
│   └── RESEARCH_ANALYSIS_REPORT.md        # Comprehensive Academic Evaluation & Research Report
├── notebooks/
│   └── 01_cdo_sprawl_hazard_pipeline.ipynb # Full pipeline, walked through with plots
├── RESEARCH_ANALYSIS_REPORT.md            # Root copy of the comprehensive professor-grade report
├── figures/
│   ├── cdo_risk_map.png                   # Choropleth of barangay risk tiers
│   ├── top_risk_barangays.png             # Top 15 barangays by risk score
│   └── hazard_vs_growth.png               # Diagnostic scatter: hazard vs. growth, colored by tier
├── src/
│   ├── pipeline.py                        # Load -> merge -> score -> rank
│   └── figures.py                         # Generates all chart/map outputs
├── requirements.txt
└── README.md
```

## 5. Prescriptive CDO Zoning & Mitigation Decision Matrix

| Risk Score | Tier | Recommended CDO Action |
|---|---|---|
| < 0.33 | Tier 1: Monitor | Routine hazard monitoring; no zoning restriction needed |
| 0.33 – 0.60 | Tier 2: Priority Mitigation | Drainage/slope-stabilization investment; building permit review in hazard-adjacent zones |
| ≥ 0.60 | Tier 3: Critical Intervention | Zoning moratorium on new construction; relocation program feasibility study; priority infrastructure hardening |

## 6. Quickstart

```bash
pip install -r requirements.txt
python src/pipeline.py     # builds data/processed/cdo_sprawl_hazard_ready.csv
python src/figures.py      # builds figures/*.png
jupyter notebook notebooks/01_cdo_sprawl_hazard_pipeline.ipynb
```

## 7. Methodology Notes

- **Join key:** `adm4_pcode` (PSGC barangay code) links all CCHAIN tables; filtered via `location.csv` to `adm3_en == "Cagayan de Oro City"`.
- **Why population/wealth are the time-series, not buildings/hazards/land cover:** the CCHAIN `google_open_buildings`, `project_noah_hazards`, and `esa_worldcover` tables are each single static snapshots (2023, 2015, and 2021 respectively — `freq: S`). Only `worldpop_population` (2000–2020) and `tm_relative_wealth_index` (2016–2022) are true yearly time series. The pipeline uses population CAGR as the growth signal and treats hazard/building/land-cover data as the current exposure baseline being grown into — not something that itself changes year to year in this dataset.
- **Composite risk score:** `0.40 × hazard_exposure + 0.30 × population_growth + 0.15 × building_density + 0.15 × inverse_wealth`, each min-max normalized across CDO's 80 barangays. Weights are a defensible starting point (hazard and growth prioritized as the two irreducible drivers of the "sprawl into danger" story) — see `docs/dataset_data_dictionary.md` for a sensitivity-testing suggestion if your professor asks about weight justification.
- **2030 projection:** each barangay's own 2000–2020 CAGR is compounded forward 10 years — a simple, transparent, defensible extrapolation method for an undergraduate lab activity (versus a black-box time-series model).

## 8. Data Source & Course Attribution

- **Course Fulfillment:** Data Mining and Applications — Laboratory Activity 1.
- **Primary Dataset:** Project CCHAIN — Kaggle [`thinkdatasci/project-cchain`](https://www.kaggle.com/datasets/thinkdatasci/project-cchain)
- **Citation:** Thinking Machines Data Science (2024). *Project CCHAIN Dataset: Open validated health, climate, environment, and socioeconomic data in 12 Philippine cities.* Kaggle. https://doi.org/10.34740/kaggle/ds/4918229
