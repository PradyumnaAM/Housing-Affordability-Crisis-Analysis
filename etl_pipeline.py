"""
etl_pipeline.py  —  Person 1 (Data Engineer)
Responsible for downloading, cleaning, and merging all raw data sources
into a single master_housing.csv used by modeling.py and visualizations.py.

Day 1 : download helpers + Zillow loaders + metro normalisation
Day 2 : TODO — load BLS unemployment / income data, merge with Zillow
Day 3 : TODO — build final merge → data/master_housing.csv
"""

import os
import pathlib
import requests
import pandas as pd

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
DATA_RAW = pathlib.Path("data/raw")
DATA_RAW.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Zillow source URLs
# ---------------------------------------------------------------------------
ZORI_URL = (
    "https://files.zillowstatic.com/research/public_csvs/zori/"
    "Metro_zori_uc_sfrcondomfr_sm_sa_month.csv"
)
ZHVI_URL = (
    "https://files.zillowstatic.com/research/public_csvs/zhvi/"
    "Metro_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv"
)

# ---------------------------------------------------------------------------
# Metro name normalisation map
# Zillow and BLS use slightly different spellings for the same metro areas.
# Keys   = raw strings that appear in source files
# Values = canonical name used throughout this project
# ---------------------------------------------------------------------------
METRO_MAP: dict[str, str] = {
    "New York, NY":                          "New York",
    "New York-Newark-Jersey City, NY-NJ-PA": "New York",
    "Los Angeles-Long Beach-Anaheim, CA":    "Los Angeles",
    "Los Angeles, CA":                       "Los Angeles",
    "Chicago-Naperville-Elgin, IL-IN-WI":   "Chicago",
    "Chicago, IL":                           "Chicago",
    "Houston-The Woodlands-Sugar Land, TX":  "Houston",
    "Houston, TX":                           "Houston",
    "Phoenix-Mesa-Chandler, AZ":             "Phoenix",
    "Phoenix, AZ":                           "Phoenix",
    "Philadelphia-Camden-Wilmington, PA-NJ": "Philadelphia",
    "Philadelphia, PA":                      "Philadelphia",
    "San Antonio-New Braunfels, TX":         "San Antonio",
    "San Diego-Chula Vista-Carlsbad, CA":    "San Diego",
    "San Diego, CA":                         "San Diego",
    "Dallas-Fort Worth-Arlington, TX":       "Dallas",
    "Dallas, TX":                            "Dallas",
    "Austin-Round Rock-Georgetown, TX":      "Austin",
    "Austin, TX":                            "Austin",
    "Seattle-Tacoma-Bellevue, WA":           "Seattle",
    "Seattle, WA":                           "Seattle",
    "Denver-Aurora-Lakewood, CO":            "Denver",
    "Denver, CO":                            "Denver",
    "Miami-Fort Lauderdale-Pompano Beach, FL": "Miami",
    "Miami, FL":                             "Miami",
    "Atlanta-Sandy Springs-Alpharetta, GA":  "Atlanta",
    "Atlanta, GA":                           "Atlanta",
    "Minneapolis-St. Paul-Bloomington, MN-WI": "Minneapolis",
    "Minneapolis, MN":                       "Minneapolis",
    "Portland-Vancouver-Hillsboro, OR-WA":   "Portland",
    "Portland, OR":                          "Portland",
    "Las Vegas-Henderson-Paradise, NV":      "Las Vegas",
    "Las Vegas, NV":                         "Las Vegas",
    "Nashville-Davidson--Murfreesboro--Franklin, TN": "Nashville",
    "Nashville, TN":                         "Nashville",
    "Charlotte-Concord-Gastonia, NC-SC":     "Charlotte",
    "Charlotte, NC":                         "Charlotte",
    "Riverside-San Bernardino-Ontario, CA":  "Riverside",
    "Sacramento-Roseville-Folsom, CA":       "Sacramento",
    "Sacramento, CA":                        "Sacramento",
    "Orlando-Kissimmee-Sanford, FL":         "Orlando",
    "Orlando, FL":                           "Orlando",
    "Tampa-St. Petersburg-Clearwater, FL":   "Tampa",
    "Tampa, FL":                             "Tampa",
    "Boston-Cambridge-Newton, MA-NH":        "Boston",
    "Boston, MA":                            "Boston",
    "Baltimore-Columbia-Towson, MD":         "Baltimore",
    "Baltimore, MD":                         "Baltimore",
    "San Francisco-Oakland-Berkeley, CA":    "San Francisco",
    "San Francisco, CA":                     "San Francisco",
    "Washington-Arlington-Alexandria, DC-VA-MD-WV": "Washington DC",
    "Washington, DC":                        "Washington DC",
    "Richmond, VA":                          "Richmond",
    "Jacksonville, FL":                      "Jacksonville",
    "Columbus, OH":                          "Columbus",
    "Indianapolis-Carmel-Anderson, IN":      "Indianapolis",
    "Indianapolis, IN":                      "Indianapolis",
    "Cincinnati, OH-KY-IN":                  "Cincinnati",
    "Cincinnati, OH":                        "Cincinnati",
    "Kansas City, MO-KS":                    "Kansas City",
    "Kansas City, MO":                       "Kansas City",
    "Oklahoma City, OK":                     "Oklahoma City",
    "Louisville/Jefferson County, KY-IN":    "Louisville",
    "Louisville, KY":                        "Louisville",
    "Memphis, TN-MS-AR":                     "Memphis",
    "Memphis, TN":                           "Memphis",
    "Virginia Beach-Norfolk-Newport News, VA-NC": "Virginia Beach",
    "Providence-Warwick, RI-MA":             "Providence",
    "Providence, RI":                        "Providence",
    "Hartford-East Hartford-Middletown, CT": "Hartford",
    "Hartford, CT":                          "Hartford",
    "New Orleans-Metairie, LA":              "New Orleans",
    "New Orleans, LA":                       "New Orleans",
    "Buffalo-Cheektowaga, NY":               "Buffalo",
    "Buffalo, NY":                           "Buffalo",
    "Raleigh-Cary, NC":                      "Raleigh",
    "Raleigh, NC":                           "Raleigh",
    "Birmingham-Hoover, AL":                 "Birmingham",
    "Birmingham, AL":                        "Birmingham",
    "Salt Lake City, UT":                    "Salt Lake City",
    "Tucson, AZ":                            "Tucson",
    "St. Louis, MO-IL":                      "St. Louis",
    "St. Louis, MO":                         "St. Louis",
    "Pittsburgh, PA":                        "Pittsburgh",
    "Cleveland-Elyria, OH":                  "Cleveland",
    "Cleveland, OH":                         "Cleveland",
    "Detroit-Warren-Dearborn, MI":           "Detroit",
    "Detroit, MI":                           "Detroit",
}


def normalise_metro(name: str) -> str:
    """Return the canonical metro name, or the original string if not mapped."""
    return METRO_MAP.get(name.strip(), name.strip())


# ---------------------------------------------------------------------------
# Download helper
# ---------------------------------------------------------------------------
def download_file(url: str, dest: pathlib.Path, force: bool = False) -> pathlib.Path:
    """
    Download *url* to *dest*, skipping if the file already exists.

    Parameters
    ----------
    url   : remote URL to fetch
    dest  : local path to save the file
    force : re-download even if *dest* already exists

    Returns
    -------
    pathlib.Path pointing to the saved file.
    """
    if dest.exists() and not force:
        print(f"  [skip] {dest.name} already exists")
        return dest

    print(f"  [download] {url} → {dest}")
    resp = requests.get(url, timeout=60)
    resp.raise_for_status()
    dest.write_bytes(resp.content)
    print(f"  [ok] saved {dest.stat().st_size:,} bytes")
    return dest


# ---------------------------------------------------------------------------
# Zillow wide-format loader
# ---------------------------------------------------------------------------
def load_zillow_wide(path: pathlib.Path, value_name: str) -> pd.DataFrame:
    """
    Read a Zillow wide CSV (one column per date) and melt it to long format.

    Zillow publishes data with columns: RegionID, SizeRank, RegionName,
    RegionType, StateName, followed by one column per YYYY-MM-DD date.

    Parameters
    ----------
    path       : local path to the raw Zillow CSV
    value_name : label for the melted value column, e.g. "zori" or "zhvi"

    Returns
    -------
    DataFrame with columns: metro, date, <value_name>
    """
    df = pd.read_csv(path)

    # Identify date columns (format: YYYY-MM-DD)
    id_cols = ["RegionID", "SizeRank", "RegionName", "RegionType", "StateName"]
    date_cols = [c for c in df.columns if c not in id_cols]

    long = df.melt(
        id_vars=["RegionName"],
        value_vars=date_cols,
        var_name="date",
        value_name=value_name,
    )

    long["date"] = pd.to_datetime(long["date"])
    long["metro"] = long["RegionName"].apply(normalise_metro)
    long = long.drop(columns=["RegionName"])
    long = long.dropna(subset=[value_name])
    long = long.sort_values(["metro", "date"]).reset_index(drop=True)

    return long[["metro", "date", value_name]]


# ---------------------------------------------------------------------------
# TODO Day 2 — BLS / income data loaders
# ---------------------------------------------------------------------------
# def load_bls_unemployment(path):
#     """Load and reshape BLS metro unemployment CSV."""
#     raise NotImplementedError("Day 2")
#
# def load_median_income(path):
#     """Load ACS median household income by metro."""
#     raise NotImplementedError("Day 2")


# ---------------------------------------------------------------------------
# TODO Day 3 — master merge
# ---------------------------------------------------------------------------
# def build_master(zori_df, zhvi_df, bls_df, income_df):
#     """
#     Join all sources on (metro, date), compute affordability ratio,
#     and write data/master_housing.csv.
#     """
#     raise NotImplementedError("Day 3")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=== ETL Pipeline — Day 1 smoke test ===\n")

    zori_path = DATA_RAW / "Metro_zori.csv"
    zhvi_path = DATA_RAW / "Metro_zhvi.csv"

    try:
        download_file(ZORI_URL, zori_path)
        download_file(ZHVI_URL, zhvi_path)
    except Exception as exc:
        print(f"\n[warn] Download failed: {exc}")
        print("       Place CSVs manually in data/raw/ and re-run.\n")
    else:
        if zori_path.exists():
            zori = load_zillow_wide(zori_path, "zori")
            print(f"\nZORI long-format shape : {zori.shape}")
            print(zori.head(3).to_string(index=False))

        if zhvi_path.exists():
            zhvi = load_zillow_wide(zhvi_path, "zhvi")
            print(f"\nZHVI long-format shape : {zhvi.shape}")
            print(zhvi.head(3).to_string(index=False))

    print("\n[Day 1 done] Next: run Day 2 to add BLS + income sources.")
