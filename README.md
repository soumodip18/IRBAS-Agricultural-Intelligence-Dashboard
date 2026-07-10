# IRBAS Agricultural Intelligence Dashboard

# 🌾 Mul Biotech Farms — Agricultural Intelligence Platform

**28-state Indian Agricultural Intelligence Dashboard** for crop water analytics, irrigation risk assessment, commodity intelligence, and state-level SWOT profiling.

**Position:** Data Engineering & Analytics Intern  
**Organization:** Mul Biotech Farms / SequestraBionix Foundation

---

# Overview

This project develops an agricultural intelligence platform covering **30 Indian states** by integrating research datasets into a production-ready analytical model.

The platform answers two primary questions:

- **Where are agricultural risks concentrated?**
  - State-wise environmental and economic risks
  - SWOT analysis
  - Commodity price intelligence
  - Interactive geographic visualization

- **How are agricultural resources utilized?**
  - Crop water footprints
  - Irrigation dependency analysis
  - Seasonal crop calendars
  - Resource allocation insights

The repository contains the complete ETL workflow, normalized data model, Power BI dashboards, and deployment assets.

---

# Repository Structure

```text
IRBAS-Agricultural-Intelligence-Dashboard/
│
├── index.html
├── README.md
│
├── .github/
│   └── workflows/
│       └── scrape.yml
│
├── dashboard/
│   ├── commodity_price_intelligence_dashboard-lavanya.pbix
│   ├── executive_commodity_analysis-malvika.pbix
│   └── india_crop_water_resource_dashboard-kartik.pbix
│
├── data/
│   ├── Custom_PowerBI_Agriculture_Model.xlsx
│   └── State Assessment Dashboard Agriculture.xlsx
│
├── docs/
│   └── data_dictionary.md
│
└── scripts/
    └── cloud_pipeline.py
```

---

# Data Architecture

The project uses a **Star Schema** optimized for Power BI.

```
                dim_State
                    │
      ┌─────────────┼─────────────┐
      │             │             │
fact_Risks   fact_CropTimeline   fact_SWOT
      │
fact_WaterEconomics
      │
fact_AdvantagesConstraints
```

Every fact table joins directly to:

```
dim_State[State]
```

---

# Data Model

| Table | Rows | Description |
|------|------:|-------------|
| `dim_State` | 30 | State master table containing regions, contributors, and source mappings |
| `fact_Risks` | 56 | Environmental and economic risk profiles |
| `fact_CropTimeline` | 511 | Crop season classifications with sowing and harvesting schedules |
| `fact_WaterEconomics` | 326 | Water footprint and irrigation dependency metrics |
| `fact_SWOT` | 269 | Strengths, weaknesses, opportunities, and threats |
| `fact_AdvantagesConstraints` | 760 | State-wise operational advantages and constraints |

---

# Data Engineering Highlights

- Resolved **87** preprocessing issues.
- Filled **332** missing seasonal values.
- Recomputed **49** missing crop water footprint values.
- Reconstructed **70** irrigation dependency rankings.
- Removed **8** invalid placeholder records.
- Backfilled missing agricultural profiles for **9** states.
- Converted a fragmented **30-sheet Excel workbook** into a normalized production-ready star schema.

---

# Dashboards

The repository contains three Power BI dashboards.

| Dashboard | Description |
|-----------|-------------|
| **India Crop Water Resource Dashboard** | Water footprint, irrigation dependency, crop analytics |
| **Commodity Price Intelligence Dashboard** | Commodity market and mandi price analysis |
| **Executive Commodity Analysis Dashboard** | Executive-level agricultural KPIs |

---

# Technologies Used

- Python
- Pandas
- Selenium
- OpenPyXL
- Google APIs
- Power BI
- GitHub Actions
- HTML

---

# Installation

Clone the repository.

```bash
git clone https://github.com/soumodip18/IRBAS-Agricultural-Intelligence-Dashboard.git

cd IRBAS-Agricultural-Intelligence-Dashboard
```

Install the required packages.

```bash
pip install pandas selenium webdriver-manager openpyxl \
google-auth google-api-python-client
```

Run the ETL pipeline.

```bash
python scripts/cloud_pipeline.py
```

---

# Power BI Configuration

1. Open one of the `.pbix` files inside the `dashboard` directory.
2. Open **Transform Data**.
3. Navigate to:

```
Data Source Settings
```

4. Update the source path to:

```
data/Custom_PowerBI_Agriculture_Model.xlsx
```

5. Refresh the dataset.

---

# Dashboard Deployment

After publishing the report to Power BI Service, generate an embed link and replace the iframe source inside `index.html`.

```html
<iframe
    src="YOUR_POWERBI_EMBED_URL"
    width="100%"
    height="800"
    frameborder="0"
    allowfullscreen>
</iframe>
```

---

# DAX Measures

| Measure | Purpose |
|----------|---------|
| `Selected State Key Risk` | Displays state-specific risk summaries |
| `Gauge Irrigation Score` | Calculates average irrigation dependency |
| `% High Irrigation Dependency` | Percentage of crops with dependency rank ≥ 6 |
| `National Avg Irrigation Score` | National benchmark using `REMOVEFILTERS()` |
| `Dynamic Profile Title` | Updates report titles dynamically |
| `Avg Water Footprint` | Average crop water requirement (L/kg) |

---

# Team

| Member | Responsibility |
|---------|----------------|
| **Kartik Patade** | ETL Development, Crop and Water Analysis Dashboard |
| **Roshan** | Regional Agricultural Research and Analytics |
| **Lavanya Dive** | Commodity Price Intelligence Dashboard |
| **Malavika Nair** | Executive Commodity Analytics Dashboard |
| **Soumodip Atanu Roy** | Technical Mentor and Project Lead |

---

# Project Features

- Agricultural intelligence across **30 Indian states**
- Automated ETL pipeline
- Power BI interactive dashboards
- Crop water footprint analytics
- Irrigation dependency scoring
- SWOT profiling
- Commodity intelligence
- GitHub Actions automation
- Normalized relational data model

---

# License

This project is licensed under the **MIT License**.

See the `LICENSE` file for details.