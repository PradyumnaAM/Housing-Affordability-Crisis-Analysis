# Housing Affordability Crisis Analysis
CS 210 Final Project — Spring 2026

Analyzes housing affordability trends across US metro areas using
Zillow rent/home-value data, BLS unemployment data, and ACS income data.

---

## Team

| Person | Role | Files owned |
|--------|------|-------------|
| Person 1 | Data Engineer | `etl_pipeline.py`, `exploration.py` |
| Person 2 | Analyst & Modeler | `modeling.py` |
| Person 3 | Visualization Lead | `visualizations.py` |

---

## Project Structure

```
housing_affordability/
├── etl_pipeline.py      # Download, clean, and merge all data sources
├── exploration.py       # Sanity-check the merged dataset
├── modeling.py          # Regression + clustering models
├── visualizations.py    # Interactive Plotly charts
├── main.py              # End-to-end orchestration
├── requirements.txt
├── data/
│   └── raw/             # Raw CSVs (gitignored — see below)
├── models/              # Saved .pkl model files (gitignored)
└── plots/               # Generated .html charts (gitignored)
```

---

## Setup

```bash
git clone https://github.com/PradyumnaAM/Housing-Affordability-Crisis-Analysis.git
cd Housing-Affordability-Crisis-Analysis/housing_affordability
pip install -r requirements.txt
```

---

## Running the pipeline

```bash
# Step 1 — download Zillow data and verify shapes (Person 1)
python etl_pipeline.py

# Step 2 — sanity-check the merged dataset (Person 1)
python exploration.py

# Step 3 — train models (Person 2, after ETL is complete)
python modeling.py

# Step 4 — generate charts (Person 3, after modeling is complete)
python visualizations.py

# Full pipeline (Day 3+)
python main.py
```

---

## Data Sources

| Source | What it provides | Format |
|--------|-----------------|--------|
| [Zillow ZORI](https://www.zillow.com/research/data/) | Monthly observed rent index by metro | Wide CSV |
| [Zillow ZHVI](https://www.zillow.com/research/data/) | Monthly home value index by metro | Wide CSV |
| BLS LAUS | Metro unemployment rate (Day 2) | CSV |
| ACS 5-Year | Median household income by metro (Day 2) | CSV |

Raw CSVs are placed in `data/raw/` (gitignored due to size).

---

## Implementation Schedule

| Day | Owner | Deliverable |
|-----|-------|-------------|
| Day 1 | Person 1 | ETL scaffold, Zillow download + melt, metro normalisation |
| Day 2 | Person 1 | BLS + income loaders, full master merge → `data/master_housing.csv` |
| Day 2 | Person 2 | Regression model, clustering model |
| Day 2 | Person 3 | Choropleth + trend-line charts |
| Day 3 | All | Integration, fastest-deteriorating analysis, final charts, write-up |
