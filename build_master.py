"""
build_master.py  —  Person 1 (Data Engineer)
One-off script: merges all data sources into data/master_housing.csv
and data/housing.db.  Run once; re-run only if sources change.

Sources
-------
- data/raw/Metro_zori.csv        Zillow rent index (monthly)
- data/raw/Metro_zhvi.csv        Zillow home-value index (monthly)
- data/raw/bls_unemployment.csv  BLS annual unemployment by metro
- Hardcoded ACS income estimates  (2015-2023, 12 metros)

Usage
-----
    python build_master.py
"""

import pathlib
import sqlite3
import sys

import pandas as pd

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from etl_pipeline import load_zillow_wide, normalise_metro, DATA_RAW

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
DATA       = pathlib.Path("data")
MASTER_CSV = DATA / "master_housing.csv"
MASTER_DB  = DATA / "housing.db"

# ---------------------------------------------------------------------------
# Supplemental metro-name map (names not already in etl_pipeline.METRO_MAP)
# ---------------------------------------------------------------------------
_EXTRA = {
    "San Jose-Sunnyvale-Santa Clara, CA":  "San Jose",
    "San Jose, CA":                        "San Jose",
    "Dallas-Fort Worth, TX":               "Dallas",
    "Houston-Pasadena-The Woodlands, TX":  "Houston",
}

TARGET_METROS = {
    "New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
    "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose",
    "Seattle", "Austin",
}


def _norm(name: str) -> str:
    s = name.strip()
    return _EXTRA.get(s, normalise_metro(s))


# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------
def load_bls_unemployment() -> pd.DataFrame:
    path = DATA_RAW / "bls_unemployment.csv"
    if not path.exists():
        print("[warn] bls_unemployment.csv missing — unemployment_rate will be NaN")
        rows = [{"metro": m, "year": y, "unemployment_rate": None}
                for m in TARGET_METROS for y in range(2015, 2024)]
        return pd.DataFrame(rows)

    df = pd.read_csv(path)
    df["metro"] = df["metro"].apply(_norm)
    return df[["metro", "year", "unemployment_rate"]]


def load_census_income() -> pd.DataFrame:
    """
    ACS 5-year median household income estimates (USD).
    Source: American Community Survey, 2015-2023.
    Values are approximate metro-level estimates.
    """
    income_table = {
        #                  2015    2016    2017    2018    2019    2020    2021    2022    2023
        "New York":     [64800,  67200,  69500,  72900,  76500,  79200,  81400,  86300,  90100],
        "Los Angeles":  [60100,  63000,  65900,  69100,  73100,  75700,  79200,  83600,  87300],
        "Chicago":      [61500,  64200,  66800,  70200,  73500,  75300,  77400,  81900,  85200],
        "Houston":      [56800,  59000,  61400,  64300,  67900,  68500,  71200,  75500,  78900],
        "Phoenix":      [53900,  56900,  59600,  63400,  67200,  70100,  73800,  78500,  82400],
        "Philadelphia": [63100,  65700,  68300,  71600,  75300,  77900,  80200,  85000,  88700],
        "San Antonio":  [50100,  52400,  54800,  57500,  60700,  62400,  64900,  68600,  71500],
        "San Diego":    [65800,  68900,  72400,  76500,  81100,  84700,  89300,  94800,  99200],
        "Dallas":       [58600,  61800,  65100,  68900,  72800,  74600,  78300,  83700,  87900],
        "San Jose":     [97300, 103100, 109600, 117900, 124800, 128400, 134500, 143900, 151200],
        "Seattle":      [77200,  82100,  88200,  95300, 102400, 107100, 114300, 123700, 130900],
        "Austin":       [64200,  67800,  71500,  76300,  81400,  84900,  90200,  97100, 102300],
    }
    years = list(range(2015, 2024))
    rows = [
        {"metro": metro, "year": year, "median_household_income": inc}
        for metro, vals in income_table.items()
        for year, inc in zip(years, vals)
    ]
    return pd.DataFrame(rows)


def aggregate_zillow_annual(df: pd.DataFrame, value_col: str) -> pd.DataFrame:
    """Average monthly Zillow data to annual, filtered to the 12 target metros."""
    df = df.copy()
    df["year"]  = df["date"].dt.year
    df["metro"] = df["metro"].apply(_norm)
    df = df[df["metro"].isin(TARGET_METROS)]
    df = df[(df["year"] >= 2015) & (df["year"] <= 2023)]
    return (
        df.groupby(["metro", "year"])[value_col]
          .mean()
          .round(2)
          .reset_index()
    )


# ---------------------------------------------------------------------------
# Master build
# ---------------------------------------------------------------------------
def build_master() -> pd.DataFrame:
    print("  Loading ZORI ...")
    zori = aggregate_zillow_annual(
        load_zillow_wide(DATA_RAW / "Metro_zori.csv", "zori"), "zori"
    )

    print("  Loading ZHVI ...")
    zhvi = aggregate_zillow_annual(
        load_zillow_wide(DATA_RAW / "Metro_zhvi.csv", "zhvi"), "zhvi"
    )

    print("  Loading BLS unemployment ...")
    bls = load_bls_unemployment()

    print("  Loading census income ...")
    income = load_census_income()

    # Income is the base (12 metros x 9 years = 108 rows)
    master = income.copy()
    master = master.merge(zori, on=["metro", "year"], how="left")
    master = master.merge(zhvi, on=["metro", "year"], how="left")
    master = master.merge(bls,  on=["metro", "year"], how="left")
    master = master.sort_values(["metro", "year"]).reset_index(drop=True)

    # --- Derived columns ---
    master["monthly_income"]  = (master["median_household_income"] / 12).round(2)
    master["rent_to_income"]  = (master["zori"] / master["monthly_income"]).round(4)
    master["price_to_income"] = ((master["zhvi"] * 0.065) / master["median_household_income"]).round(4)
    master["in_crisis"]       = (master["rent_to_income"] > 0.30).astype("Int64")

    # Year-over-year growth rates (NaN for first year per metro)
    master = master.sort_values(["metro", "year"])
    master["yoy_rent_growth"]   = master.groupby("metro")["zori"].pct_change(fill_method=None).round(4)
    master["yoy_income_growth"] = master.groupby("metro")["median_household_income"].pct_change(fill_method=None).round(4)
    master["yoy_hv_growth"]     = master.groupby("metro")["zhvi"].pct_change(fill_method=None).round(4)
    master["rent_income_gap"]   = (master["yoy_rent_growth"] - master["yoy_income_growth"]).round(4)

    return master.reset_index(drop=True)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    if MASTER_CSV.exists():
        print(f"[skip] {MASTER_CSV} already exists. Delete it to rebuild.")
        sys.exit(0)

    print("=== build_master.py ===\n")
    master = build_master()

    # Save CSV
    master.to_csv(MASTER_CSV, index=False)
    print(f"\n[ok] {MASTER_CSV}  ({len(master):,} rows)")

    # Save SQLite
    with sqlite3.connect(MASTER_DB) as conn:
        master.to_sql("housing", conn, if_exists="replace", index=False)
    print(f"[ok] {MASTER_DB}  (table: housing)")

    # Summary
    print(f"\nRow count   : {len(master):,}")
    print(f"Metro count : {master['metro'].nunique()}")
    print(f"Year range  : {master['year'].min()} - {master['year'].max()}")

    preview = ["metro", "year", "zori", "zhvi", "median_household_income",
               "rent_to_income", "in_crisis"]
    print("\nFirst 10 rows:")
    print(master[preview].head(10).to_string(index=False))
