# 🏙️ Cagayan de Oro City Urban Sprawl & Hazard Exposure Risk Engine

> **A Spatial Risk-Scoring & Zoning-Priority Tool for the Cagayan de Oro City Local Government Unit (CDO LGU)**  
> *Developed for the CDO City Planning and Development Office (CPDO) & City Disaster Risk Reduction and Management Office (CDRRMO)*  
> *Pilot City: Cagayan de Oro City, Northern Mindanao, Philippines (80 Administrative Barangays | PSGC: `PH104305000` | 2000–2023 CCHAIN Extracts)*  
>
> 🎓 **Academic Fulfillment:** Data Mining and Applications (DMA) — Laboratory Activity 1  
> 🌐 **Primary Dataset Source:** Project CCHAIN (Kaggle: [`thinkdatasci/project-cchain`](https://www.kaggle.com/datasets/thinkdatasci/project-cchain))

---

## 📌 Course & Data Attribution Notice

- **Academic Requirement:** This repository is submitted in fulfillment of **Data Mining and Applications (DMA) — Laboratory Activity 1**.
- **Dataset Provenance:** All hazard, building, land cover, wealth, and demographic data originate from **Project CCHAIN**, an open-access multi-partner initiative by Thinking Machines, EpiMetrics, Manila Observatory, and PACSII (funded by Wellcome Trust & Lacuna Fund).
- **Scope & Resolution:** 8 raw tabular and spatial datasets were extracted, cleaned, and unified into an analysis-ready matrix covering all 80 barangays of Cagayan de Oro City.

---

## 1. Executive Summary & Operational Problem

Cagayan de Oro City has experienced rapid demographic expansion that has pushed residential and economic settlements directly into high-risk floodplains and steep, landslide-prone uplands. Municipal decision-makers frequently lack an integrated, data-driven system to identify **where population growth coincides with physical hazards** and whether economically vulnerable populations are disproportionately impacted.

This project implements a **Multi-Criteria Spatial Risk Index (MCSRI)** that fuses 20 years of historical population growth, physical multi-hazard exposure, satellite-derived building footprints, and socioeconomic resilience trends into an actionable 3-tier zoning and resource-allocation matrix.

### 4-Pillar Analytical Framework

| Pillar | Analytics Type | Core Objective & Deliverable |
| :--- | :--- | :--- |
| **Pillar 1** | **Descriptive Analytics** | Baseline spatial and temporal profiles (20-yr population CAGR, physical hazard footprint, building density). |
| **Pillar 2** | **Diagnostic Analytics** | 4-quadrant cross-tabulation and archetype discovery (Floodplain Inundation vs. Upland Mountain Sprawl). |
| **Pillar 3** | **Predictive Analytics** | 2030 demographic extrapolation and compounding risk exposure modeling. |
| **Pillar 4** | **Prescriptive Analytics** | Weighted Multi-Criteria Spatial Risk Index (MCSRI), 3-tier action matrix, and sensitivity validation. |

---

## 2. Key Empirical Findings (80 CDO Barangays)

- **Citywide Population Velocity:** Total CDO population reached **752,064** (WorldPop 2020), exhibiting a **2.86% mean annual CAGR** from 2000 to 2020.
- **Physical Hazard Exposure:** **30 of 80 barangays** have over 20% of their land area within high 100-year flood inundation ($>1.5\text{m}$) or critical landslide susceptibility zones.
- **Identified Spatial Archetypes:**
  1. **River Delta Inundation Archetype:** Core urban barangays (*Barangay 17 Poblacion*, *Consolacion*) with extreme building density and severe flood hazard.
  2. **Upland Mountain Sprawl Archetype:** Rural peripheral barangays (*Tignapoloan*, *Besigan*) exhibiting rapid growth (**4.27% CAGR**) into high-landslide terrain coupled with low economic resilience ($RWI = 0.32$).
- **Prescriptive Tier Breakdown:**
  - 🔴 **Tier 3: Critical Intervention (3 Barangays | Score $\ge 0.60$):** Immediate zoning moratoria, relocation feasibility, and priority structural hardening.
  - 🟡 **Tier 2: Priority Mitigation (33 Barangays | Score $0.33 - 0.60$):** Slope stabilization, drainage upgrades, and strict building permit enforcement.
  - 🟢 **Tier 1: Continuous Monitoring (44 Barangays | Score $< 0.33$):** Routine environmental surveillance and baseline land use monitoring.

---

## 3. Visualizations & Analytical Artifacts

All figures are programmatically generated and exported to the [`figures/`](./figures/) directory:

| Artifact | Description |
| :--- | :--- |
| **[`cdo_risk_map.png`](./figures/cdo_risk_map.png)** | Choropleth risk map visualizing the 80 barangays categorized into Tier 1, 2, and 3 zones. |
| **[`cdo_sprawl_points_map.png`](./figures/cdo_sprawl_points_map.png)** | Proportional symbol centroid map illustrating population growth velocity across hazard surfaces. |
| **[`hazard_vs_growth.png`](./figures/hazard_vs_growth.png)** | 4-quadrant diagnostic scatter plot mapping Physical Hazard Exposure vs. 20-Year Population CAGR. |
| **[`top_risk_barangays.png`](./figures/top_risk_barangays.png)** | Ranked horizontal bar chart displaying the Top 15 highest-risk barangays and score components. |

---

## 4. Repository Directory Structure

```text
Climate-Driven-Urban-Sprawl-Hazard-Exposure/
├── data/
│   ├── cchain_raw/                             # 8 raw Project CCHAIN CSV data tables
│   │   ├── brgy_geography.csv                  # WKT geometric boundaries & spatial polygons
│   │   ├── esa_worldcover.csv                  # Land cover classifications (built-up, tree, etc.)
│   │   ├── google_open_buildings.csv           # Building counts and footprint area (m^2)
│   │   ├── location.csv                        # PSGC administrative hierarchy metadata
│   │   ├── project_noah_hazards.csv            # 5/25/100-yr flood & landslide hazard %
│   │   ├── tm_relative_wealth_index.csv        # Micro-estimate socioeconomic wealth indices
│   │   └── worldpop_population.csv             # Longitudinal annual population (2000–2020)
│   └── processed/
│       └── cdo_sprawl_hazard_ready.csv         # Master scored and ranked 80-barangay dataset
├── docs/
│   ├── DATA_MINING_METHODOLOGY.md              # Complete mathematical reference & pipeline architecture
│   ├── DATASET_CLEANING_METHODOLOGY.md         # Non-technical stakeholder blueprint & presentation script
│   ├── RESEARCH_ANALYSIS_REPORT.md             # Formal research paper, analytical Q&A, and defense guide
│   └── dataset_data_dictionary.md              # Column-level schema lineage, units, and formulas
├── figures/                                    # High-resolution output maps & diagnostic plots
│   ├── cdo_risk_map.png                        # 3-Tier spatial choropleth map
│   ├── cdo_sprawl_points_map.png               # Centroid-based sprawl point distribution
│   ├── hazard_vs_growth.png                    # Diagnostic 4-quadrant scatter plot
│   └── top_risk_barangays.png                  # Top 15 priority barangay ranking chart
├── notebooks/
│   └── 01_cdo_sprawl_hazard_pipeline.ipynb      # Interactive step-by-step Jupyter notebook
├── src/
│   ├── pipeline.py                             # Complete ETL, feature engineering, & scoring pipeline
│   └── figures.py                              # Visualization & thematic cartography generation engine
├── RESEARCH_ANALYSIS_REPORT.md                 # Root reference copy of comprehensive report
├── requirements.txt                            # Python environment dependencies
└── README.md                                   # Project landing page & documentation index
```

---

## 5. Documentation & Methodological References

| Document | Focus & Target Audience | Key Contents |
| :--- | :--- | :--- |
| **[`DATA_MINING_METHODOLOGY.md`](./docs/DATA_MINING_METHODOLOGY.md)** | Technical & Academic Defense | Mathematical formulation of CAGR, Multi-Hazard Union, Min-Max Normalization, Inverted Social Vulnerability, MCSRI formula, and Spearman rank sensitivity testing. |
| **[`DATASET_CLEANING_METHODOLOGY.md`](./docs/DATASET_CLEANING_METHODOLOGY.md)** | Non-Technical & Slide Defense | 3-column slide blueprint for Slide 4 (Extraction $\rightarrow$ Cleaning $\rightarrow$ Interpretation) with a 60–90 second talk track and non-technical Q&A guide. |
| **[`RESEARCH_ANALYSIS_REPORT.md`](./docs/RESEARCH_ANALYSIS_REPORT.md)** | Formal Evaluation & Faculty Review | 36KB comprehensive research monograph detailing the operational problem, 7–10 analytical questions across all 4 analytics tiers, empirical results, and policy recommendations. |
| **[`dataset_data_dictionary.md`](./docs/dataset_data_dictionary.md)** | Engineering & Data Governance | Field-by-field definitions, data types, null handling, temporal resolutions, and source lineage. |

---

## 6. Mathematical Formulations Summary

### 1. Compound Annual Growth Rate (Demographic Velocity)
$$\text{CAGR}_i = \left( \frac{P_{i, 2020}}{P_{i, 2000}} \right)^{\frac{1}{20}} - 1$$

### 2. Multi-Hazard Physical Union
$$\text{HazardExposure}_i = \min\left(100, \; \text{Flood100YrHigh}_i + \text{LandslideHigh}_i\right)$$

### 3. Inverted Social Vulnerability
$$\widetilde{V}_i = 1 - \widetilde{\text{RWI}}_{\text{latest}, i} = 1 - \left(\frac{\text{RWI}_i - \min(\mathbf{RWI})}{\max(\mathbf{RWI}) - \min(\mathbf{RWI})}\right)$$

### 4. Multi-Criteria Spatial Risk Index (MCSRI)
$$\text{MCSRI}_i = 0.40 \cdot \widetilde{H}_i + 0.30 \cdot \widetilde{G}_i + 0.15 \cdot \widetilde{D}_i + 0.15 \cdot \widetilde{V}_i$$

*Where $\widetilde{H}_i$, $\widetilde{G}_i$, $\widetilde{D}_i$, and $\widetilde{V}_i$ represent the min-max normalized scores for Hazard Exposure, Population Growth, Building Density, and Social Vulnerability.*

---

## 7. Quickstart & Pipeline Reproduction

### Prerequisites
Ensure Python 3.10+ is installed on your workstation.

```bash
# 1. Clone the repository and navigate into the folder
cd Climate-Driven-Urban-Sprawl-Hazard-Exposure

# 2. Install dependencies
pip install -r requirements.txt

# 3. Execute the full end-to-end data mining pipeline
python src/pipeline.py

# 4. Generate all figures, choropleth maps, and diagnostic charts
python src/figures.py

# 5. (Optional) Run the interactive walkthrough notebook
jupyter notebook notebooks/01_cdo_sprawl_hazard_pipeline.ipynb
```

---

## 8. Prescriptive Policy Action Matrix

```text
+-------------------+----------------------+--------------------------------------------------------------------+
| Risk Score Range  | Intervention Tier    | Recommended Municipal Actions (CPDO / CDRRMO)                      |
+-------------------+----------------------+--------------------------------------------------------------------+
| Score >= 0.60     | Tier 3: Critical     | • Impose strict zoning moratoria on new residential permits.       |
| (3 Barangays)     | Intervention         | • Conduct structured relocation feasibility for riverbank zones.   |
|                   |                      | • Immediate budget allocation for structural flood defenses.       |
+-------------------+----------------------+--------------------------------------------------------------------+
| 0.33 <= Score < 0.60| Tier 2: Priority   | • Require geohazard clearance for all private construction.        |
| (33 Barangays)    | Mitigation           | • Invest in upland slope stabilization and runoff retention basins.|
|                   |                      | • Upgrade stormwater drainage networks in growing corridors.       |
+-------------------+----------------------+--------------------------------------------------------------------+
| Score < 0.33      | Tier 1: Continuous   | • Maintain routine baseline satellite and GIS surveillance.        |
| (44 Barangays)    | Monitoring           | • Preserve existing agricultural and forest land cover buffers.    |
|                   |                      | • Standard building code compliance audits.                        |
+-------------------+----------------------+--------------------------------------------------------------------+
```

---

## 9. Academic Citation & Data Sources

```bibtex
@misc{thinkingmachines2024cchain,
  title={Project CCHAIN: Climate Change, Health, and AI Network Dataset},
  author={Thinking Machines Data Science and EpiMetrics and Manila Observatory and PACSII},
  year={2024},
  publisher={Kaggle},
  url={https://www.kaggle.com/datasets/thinkdatasci/project-cchain},
  doi={10.34740/kaggle/ds/4918229}
}
```

