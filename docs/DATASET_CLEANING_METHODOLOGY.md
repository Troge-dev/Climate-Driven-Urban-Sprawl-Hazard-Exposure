# Slide: Dataset Cleaning Methodology

> **Target Audience:** General public, non-technical stakeholders, and evaluators.  
> **Goal:** Clearly explain how raw data from multiple sources was gathered, cleaned, standardized, and transformed into actionable disaster risk decisions in under 2 minutes.

---

## Slide Content Blueprint (Copy-Paste Ready)

```
========================================================================================================
[SLIDE TITLE]  Dataset Cleaning Methodology
[SUBTITLE]     How we combined, cleaned, and standardized multi-source data for Cagayan de Oro
========================================================================================================

  1. EXTRACTION                             2. CLEANING & PREP                       3. INTERPRETATION
  "Gathering the Data"                      "Linking & Standardizing"                "Transforming into Decisions"
--------------------------------------------------------------------------------------------------------
• Sourced 7 official datasets:             • Merged all data by Barangay ID:        • Unified Risk Score (0 to 1):
  - Satellite building counts (Google)       Combined maps, population history,       Weighted 4 core factors:
  - Flood & landslide zones (NOAH)           and wealth into one unified table        - 40% Hazard Severity
  - 20-year population growth (WorldPop)     for all 80 barangays in CDO.             - 30% Population Growth Speed
  - Household wealth indices (Meta)                                                   - 15% Building Density
                                           • Standardized Diverse Metrics:             - 15% Economic Vulnerability
• Filtered specifically for:                 Converted incompatible units (counts,
  80 administrative barangays of             percentages, index scores) onto a       • Actionable 3-Tier Categories:
  Cagayan de Oro City.                       common 0 to 1 level playing field.       - Tier 3: Critical Danger (3 brgys)
                                                                                      - Tier 2: Priority Mitigation (33)
                                           • Vulnerability Inversion:                 - Tier 1: Monitoring (44)
                                             Lower economic wealth was converted
                                             into higher disaster vulnerability.    • Discovered 2 Key Risk Patterns:
                                                                                      1. Crowded river floodplains
                                                                                      2. Rapid sprawl onto steep hills
--------------------------------------------------------------------------------------------------------
[KEY TAKEAWAY] Raw, disconnected numbers were cleaned and standardized into an actionable municipal guide.
========================================================================================================
```

---

## Recommended Visual Slide Design (PowerPoint / Canva / Google Slides)

If you are designing this in presentation software, use a clean 3-card horizontal layout:

| Card / Section | Layout Suggestion | Color Accent | Content Focus |
|---|---|---|---|
| **Header** | Bold sans-serif typography (*Inter*, *Poppins*, or *Montserrat*) | Dark Navy (`#1E293B`) | Main slide title and subtitle |
| **Card 1: Extraction** | Left Column Card with bulleted source list | Ocean Blue (`#0284C7`) | What datasets were collected? |
| **Card 2: Cleaning & Prep** | Center Column Card showing merge & scaling steps | Amber (`#D97706`) | How were metrics standardized? |
| **Card 3: Interpretation** | Right Column Card with weights and tier badges | Crimson / Green (`#DC2626`) | How are the results used? |
| **Bottom Banner** | Full-width summary box across the bottom | Slate Gray (`#F1F5F9`) | The practical outcome for the city |

---

## Presenter Script (60–90 Seconds)

Here is a clear talk track in plain English:

> *"Good day, everyone. To identify which communities in Cagayan de Oro face the greatest climate hazards, we implemented a straightforward dataset cleaning and preparation methodology:*
> 
> * **1. Extraction — Gathering the data:**  
>   *We pulled together 7 reliable data sources across all 80 barangays in Cagayan de Oro. This included satellite building data from Google, official flood and landslide maps from Project NOAH, 20 years of population records from WorldPop, and household wealth data.*
> 
> * **2. Cleaning and Preparation — Linking and standardizing:**  
>   *Because you cannot directly compare building counts to flood percentages or economic scores, we matched every dataset using official barangay ID codes and converted every metric onto a standardized 0-to-1 scale. We also accounted for social vulnerability: communities with lower economic wealth have fewer resources and take longer to recover from disaster damage.*
> 
> * **3. Interpretation — Transforming data into decisions:**  
>   *Finally, we combined these factors into a single Risk Score from 0 to 1, prioritizing areas where high hazard meets rapid population growth. This sorted all 80 barangays into three clear action tiers: Critical Intervention, Priority Mitigation, and Monitoring.*
> 
> *In summary, this cleaning methodology turns messy, disconnected numbers into a clear, prioritized guide for municipal planning and disaster prevention."*

---

## Quick Q&A Reference for Non-Technical Audiences

| Question | Simple Answer |
|---|---|
| **"Why did you need to normalize the data?"** | *"Because comparing building counts to flood percentages is like comparing apples to airplanes. Normalization puts everything on the same 0 to 1 scale so they can be fairly combined."* |
| **"Why is wealth included in disaster risk?"** | *"A hazard affects everyone, but higher-income areas have concrete drainage and insurance, while lower-income communities face higher vulnerability and take longer to rebuild."* |
| **"What makes this interpretation useful?"** | *"Instead of handing decision-makers confusing spreadsheets, it gives them an instant top-to-bottom priority list of which neighborhoods need urgent intervention."* |
