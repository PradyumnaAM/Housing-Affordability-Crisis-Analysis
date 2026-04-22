"""
modeling.py  —  Person 2 (Analyst & Modeler): Sai Kommuru / Peter Chen
Trains regression and clustering models on data/master_housing.csv.

=============================================================================
MASTER DATASET — columns you will work with
=============================================================================
Load with:
    df = pd.read_csv("data/master_housing.csv")

Columns:
    metro                    str    canonical metro name (12 metros)
    year                     int    2015-2023
    median_household_income  float  ACS annual income ($)
    zori                     float  Zillow Observed Rent Index (monthly $)
    zhvi                     float  Zillow Home Value Index ($)
    unemployment_rate        float  BLS annual average (%, NaN for 2015)
    monthly_income           float  median_household_income / 12
    rent_to_income           float  zori / monthly_income  (key metric)
    price_to_income          float  (zhvi * 0.065) / median_household_income
    in_crisis                int    1 if rent_to_income > 0.30, else 0
    yoy_rent_growth          float  year-over-year % change in zori
    yoy_income_growth        float  year-over-year % change in income
    yoy_hv_growth            float  year-over-year % change in zhvi
    rent_income_gap          float  yoy_rent_growth - yoy_income_growth

Sample row (Austin 2019):
    zori=1361, zhvi=320227, income=81400, rent_to_income=0.20, in_crisis=0

=============================================================================
YOUR PIPELINE STRUCTURE (adapt from Lab 3 template)
=============================================================================
Use sklearn Pipeline + ColumnTransformer — same structure as Lab 3, but:
    - numerical_features = ['zori', 'zhvi', 'unemployment_rate',
                            'rent_to_income', 'price_to_income',
                            'yoy_rent_growth', 'yoy_income_growth']
    - categorical_features = ['metro']          (for regression only)
    - target (regression) = 'rent_to_income'    (predict 2 years forward)
    - target (clustering) = no target — unsupervised on rent_to_income pivot

Train/test split strategy:
    Train on years <= 2020, test on years 2021-2023
    (do NOT use random_state split — temporal data needs time-based split)

=============================================================================
IMPLEMENTATION GUIDE PER FUNCTION
=============================================================================
"""

import pandas as pd
import numpy as np


def train_regression(df: pd.DataFrame):
    """
    Predict rent_to_income ratio using regression.

    Steps (follow Lab 3 Pipeline structure):
    1. Drop rows where unemployment_rate is NaN (year 2015)
    2. Features (X):
           numerical  = ['zori', 'zhvi', 'unemployment_rate',
                         'yoy_rent_growth', 'yoy_income_growth',
                         'median_household_income']
           categorical = ['metro']
    3. Target (y) = 'rent_to_income'
    4. Split: X_train = year <= 2020, X_test = year >= 2021
    5. Build sklearn Pipeline:
           numeric_transformer  → SimpleImputer(mean) + StandardScaler
           categorical_transformer → SimpleImputer(most_frequent) + OneHotEncoder
           classifier → LinearRegression() (or try GradientBoostingRegressor)
    6. Fit on train, predict on test
    7. Print: R², MAE, RMSE on test set
    8. Save model: joblib.dump(model, "models/regression_model.pkl")

    Evaluation target: RMSE < 0.05 (rent_to_income is on 0-1 scale)
    """
    raise NotImplementedError("Person 2 — implement using sklearn Pipeline (see Lab 3 template)")


def train_clustering(df: pd.DataFrame):
    """
    Cluster the 12 metros into affordability risk tiers using KMeans.

    Steps:
    1. Pivot df so each row = one metro, columns = rent_to_income per year
           pivot = df.pivot(index='metro', columns='year', values='rent_to_income')
    2. Impute any NaN (forward-fill then back-fill)
    3. StandardScaler on the pivot table
    4. Try KMeans for k = 2, 3, 4 — pick best k using silhouette score
    5. Assign cluster labels back to each metro
    6. Print cluster assignments and describe each cluster
           (e.g. Cluster 0: Austin, Dallas, Phoenix → "affordable/improving")
    7. Save:
           cluster labels → "models/cluster_labels.csv"
           KMeans model  → "models/kmeans_model.pkl"

    Evaluation target: silhouette score > 0.4
    Expected clusters (roughly):
           Tier 1 (crisis)      → Los Angeles, San Jose, New York
           Tier 2 (at-risk)     → Seattle, San Diego, Chicago
           Tier 3 (affordable)  → Austin, Dallas, Phoenix, Houston, San Antonio
    """
    raise NotImplementedError("Person 2 — implement KMeans clustering")


def fastest_deteriorating(df: pd.DataFrame) -> pd.DataFrame:
    """
    Rank metros by how fast rent_to_income worsened from 2016 to 2023.

    Steps:
    1. For each metro, compute:
           deterioration_score = rent_to_income[2023] - rent_to_income[2016]
           avg_rent_income_gap = mean of rent_income_gap column (2016-2023)
    2. Sort metros by deterioration_score descending
    3. Print top 5 worst metros to console
    4. Return the ranked DataFrame

    Use the 'rent_income_gap' column — it already measures
    rent growth minus income growth per year per metro.
    """
    raise NotImplementedError("Person 2 — implement deterioration ranking")


def run_modeling():
    """
    Orchestrate the full modeling pipeline.

    Steps:
    1. df = pd.read_csv("data/master_housing.csv")
    2. Call train_regression(df)  — saves models/regression_model.pkl
    3. Call train_clustering(df)  — saves models/kmeans_model.pkl + cluster_labels.csv
    4. Call fastest_deteriorating(df) — prints and returns ranked DataFrame
    5. Print summary: model scores, cluster assignments, top 3 deteriorating metros
    """
    raise NotImplementedError("Person 2 — wire up after implementing above functions")


if __name__ == "__main__":
    print("modeling.py — not implemented yet (Person 2)")
    print("Run run_modeling() once train_regression, train_clustering,")
    print("and fastest_deteriorating are implemented.")
