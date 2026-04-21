"""
modeling.py  —  Person 2 (Analyst & Modeler)
Trains regression and clustering models on the merged housing dataset
produced by etl_pipeline.py, and identifies the fastest-deteriorating metros.

TODO: implement all functions below using data/master_housing.csv as input.
      Save trained models to models/ using joblib.
"""

import pandas as pd


def train_regression(df: pd.DataFrame):
    """
    Train a regression model predicting housing affordability.

    TODO:
    - Select features (ZHVI, ZORI, unemployment rate, median income, year, metro dummies)
    - Split train/test by date (e.g. pre-2022 train, 2022+ test)
    - Fit a LinearRegression or GradientBoostingRegressor
    - Print R², MAE on the test set
    - Save model to models/regression_model.pkl via joblib
    """
    raise NotImplementedError("Person 2 — Day 2")


def train_clustering(df: pd.DataFrame):
    """
    Cluster metros by their affordability trajectory.

    TODO:
    - Pivot data so each metro is a feature vector of monthly affordability ratios
    - Impute missing values (forward-fill then back-fill)
    - Run KMeans (try k=3..6, pick with elbow / silhouette score)
    - Print cluster assignments and cluster centers
    - Save cluster labels to models/cluster_labels.csv
    - Save KMeans model to models/kmeans_model.pkl via joblib
    """
    raise NotImplementedError("Person 2 — Day 2")


def fastest_deteriorating(df: pd.DataFrame) -> pd.DataFrame:
    """
    Rank metros by how quickly affordability has worsened.

    TODO:
    - Compute year-over-year change in affordability ratio per metro
    - Rank metros from worst deterioration to best
    - Return a DataFrame sorted by deterioration score (descending)
    - Print the top-10 worst metros to console
    """
    raise NotImplementedError("Person 2 — Day 3")


def run_modeling():
    """
    Orchestrate the full modeling pipeline.

    TODO:
    - Load data/master_housing.csv
    - Call train_regression(), train_clustering(), fastest_deteriorating()
    - Print a summary of results
    """
    raise NotImplementedError("Person 2 — Day 3")


if __name__ == "__main__":
    print("modeling.py — not implemented yet (Person 2)")
