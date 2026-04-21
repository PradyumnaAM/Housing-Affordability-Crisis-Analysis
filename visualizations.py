"""
visualizations.py  —  Person 3 (Visualization Lead)
Produces all interactive Plotly charts for the Housing Affordability
Crisis Analysis project.  All outputs are saved to plots/.

TODO: implement all functions below.
      Input is the merged DataFrame from data/master_housing.csv
      (and cluster labels from models/cluster_labels.csv where noted).
      Save every chart as an HTML file in plots/.
"""

import pandas as pd


def plot_choropleth(df: pd.DataFrame) -> None:
    """
    US choropleth map coloured by affordability ratio.

    TODO:
    - Aggregate to most-recent year per metro
    - Use plotly.express.choropleth with locationmode='USA-states'
      or a GeoJSON of metro boundaries
    - Save to plots/choropleth.html
    """
    raise NotImplementedError("Person 3 — Day 2")


def plot_trend_lines(df: pd.DataFrame) -> None:
    """
    Multi-line time-series of rent (ZORI) and home-value (ZHVI) trends.

    TODO:
    - Allow filtering by a list of metros (default: top 10 by population)
    - Use plotly.express.line with a dropdown or facet_col
    - Add a horizontal reference line at 30 % income threshold
    - Save to plots/trend_lines.html
    """
    raise NotImplementedError("Person 3 — Day 2")


def plot_cluster_scatter(df: pd.DataFrame) -> None:
    """
    Scatter plot of metros coloured by KMeans cluster assignment.

    TODO:
    - Load cluster labels from models/cluster_labels.csv
    - x-axis: median ZHVI (home value), y-axis: median ZORI (rent)
    - Colour points by cluster; hover shows metro name
    - Save to plots/cluster_scatter.html
    """
    raise NotImplementedError("Person 3 — Day 3")


def plot_deterioration(df: pd.DataFrame) -> None:
    """
    Horizontal bar chart of top-20 fastest-deteriorating metros.

    TODO:
    - Use the ranked DataFrame returned by modeling.fastest_deteriorating()
    - Colour bars by cluster assignment
    - Save to plots/deterioration.html
    """
    raise NotImplementedError("Person 3 — Day 3")


def plot_crisis_heatmap(df: pd.DataFrame) -> None:
    """
    Heatmap of affordability ratio: metros (rows) × years (columns).

    TODO:
    - Pivot df to metros × years, fill value = affordability_ratio
    - Use plotly.express.imshow with a diverging colour scale
    - Save to plots/crisis_heatmap.html
    """
    raise NotImplementedError("Person 3 — Day 3")


def run_visualizations():
    """
    Orchestrate all chart generation.

    TODO:
    - Load data/master_housing.csv
    - Call each plot function in sequence
    - Print paths of generated HTML files
    """
    raise NotImplementedError("Person 3 — Day 3")


if __name__ == "__main__":
    print("visualizations.py — not implemented yet (Person 3)")
