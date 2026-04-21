"""
exploration.py  —  Person 1 (Data Engineer)
Quick sanity-check script — run after etl_pipeline.py has produced
data/master_housing.csv to verify the merged dataset looks right.

Day 1 : load check + shape / dtype / metro inventory
Day 2 : TODO — distribution plots, outlier detection, correlation matrix
Day 3 : TODO — affordability-ratio time-series spot-checks per metro
"""

import pathlib
import pandas as pd

MASTER_CSV = pathlib.Path("data/master_housing.csv")


def load_master() -> pd.DataFrame | None:
    """Return master_housing.csv as a DataFrame, or None if missing."""
    if not MASTER_CSV.exists():
        print("[error] data/master_housing.csv not found.")
        print("        Run etl_pipeline.py first to generate the master dataset.")
        return None
    return pd.read_csv(MASTER_CSV, parse_dates=["date"])


def basic_info(df: pd.DataFrame) -> None:
    """Print shape, column names, and dtypes."""
    print(f"\nShape   : {df.shape[0]:,} rows × {df.shape[1]} columns")
    print(f"\nColumns : {list(df.columns)}")
    print("\nDtypes:")
    print(df.dtypes.to_string())
    print("\nFirst 5 rows:")
    print(df.head().to_string(index=False))


def metro_inventory(df: pd.DataFrame) -> None:
    """List all metros present in the dataset and their date ranges."""
    if "metro" not in df.columns:
        print("[warn] No 'metro' column found.")
        return

    summary = (
        df.groupby("metro")["date"]
        .agg(start="min", end="max", n_obs="count")
        .reset_index()
        .sort_values("metro")
    )
    print(f"\nMetros in dataset ({len(summary)} total):")
    print(summary.to_string(index=False))


# ---------------------------------------------------------------------------
# TODO Day 2 — deeper EDA
# ---------------------------------------------------------------------------
# def plot_distributions(df):
#     """Histograms for ZORI, ZHVI, unemployment, income."""
#     raise NotImplementedError("Day 2")
#
# def outlier_report(df):
#     """Flag metros with anomalous values (IQR method)."""
#     raise NotImplementedError("Day 2")
#
# def correlation_matrix(df):
#     """Print and save Pearson correlation heatmap of numeric columns."""
#     raise NotImplementedError("Day 2")


# ---------------------------------------------------------------------------
# TODO Day 3 — affordability spot-checks
# ---------------------------------------------------------------------------
# def affordability_spot_check(df, metro):
#     """Plot rent-to-income ratio over time for a single metro."""
#     raise NotImplementedError("Day 3")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=== Exploration — Day 1 ===")

    df = load_master()
    if df is not None:
        basic_info(df)
        metro_inventory(df)
        print("\n[Day 1 done] Next: add distribution plots in Day 2.")
