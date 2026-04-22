"""
visualizations.py  —  Person 3 (Visualization & Report Lead): remaining teammate
Produces all interactive Plotly charts for the Housing Affordability project.

=============================================================================
MASTER DATASET — columns you will work with
=============================================================================
Load with:
    df = pd.read_csv("data/master_housing.csv")

Key columns for visualizations:
    metro                    str    12 metro areas
    year                     int    2015-2023
    zori                     float  monthly rent index ($)
    zhvi                     float  home value index ($)
    median_household_income  float  annual income ($)
    rent_to_income           float  rent / monthly income (0.30 = crisis threshold)
    price_to_income          float  annual housing cost / income
    in_crisis                int    1 = above 30% rent burden threshold
    yoy_rent_growth          float  year-over-year rent % change
    yoy_income_growth        float  year-over-year income % change
    rent_income_gap          float  rent growth minus income growth

Cluster labels (after Person 2 runs modeling.py):
    clusters = pd.read_csv("models/cluster_labels.csv")
    (columns: metro, cluster)

All charts save to plots/ as .html files using plotly.

=============================================================================
IMPLEMENTATION GUIDE PER FUNCTION
=============================================================================
"""

import pandas as pd


def plot_choropleth(df: pd.DataFrame) -> None:
    """
    US choropleth map: shade each metro by rent_to_income in the most recent year.

    Steps:
    1. Filter to most recent year: df[df['year'] == df['year'].max()]
    2. Use plotly.express.scatter_geo or choropleth_mapbox
       - lat/lon dict for the 12 metros (hardcode or use a geocoder)
       - color = 'rent_to_income'
       - color_scale = 'RdYlGn_r'  (red = crisis, green = affordable)
       - Add a dashed line at 0.30 in the color bar
       - hover_data = ['metro', 'rent_to_income', 'zori', 'in_crisis']
    3. Title: "Rent-to-Income Ratio by Metro (2023)"
    4. Save: fig.write_html("plots/choropleth.html")

    Approx lat/lon for the 12 metros:
        New York (40.71, -74.01), Los Angeles (34.05, -118.24),
        Chicago (41.88, -87.63), Houston (29.76, -95.37),
        Phoenix (33.45, -112.07), Philadelphia (39.95, -75.17),
        San Antonio (29.42, -98.49), San Diego (32.72, -117.16),
        Dallas (32.78, -96.80), San Jose (37.34, -121.89),
        Seattle (47.61, -122.33), Austin (30.27, -97.74)
    """
    raise NotImplementedError("Person 3 — implement choropleth map")


def plot_trend_lines(df: pd.DataFrame) -> None:
    """
    Multi-line time-series: rent_to_income per metro from 2015-2023.

    Steps:
    1. Use plotly.express.line:
           x='year', y='rent_to_income', color='metro', markers=True
    2. Add a horizontal dashed red line at y=0.30 (crisis threshold):
           fig.add_hline(y=0.30, line_dash='dash', line_color='red',
                         annotation_text='30% Crisis Threshold')
    3. Highlight 2020 (COVID spike) with a vertical shaded region:
           fig.add_vrect(x0=2019.5, x1=2020.5, fillcolor='gray', opacity=0.1)
    4. Title: "Rent-to-Income Trends by Metro (2015-2023)"
    5. Save: fig.write_html("plots/trend_lines.html")
    """
    raise NotImplementedError("Person 3 — implement trend line chart")


def plot_cluster_scatter(df: pd.DataFrame) -> None:
    """
    Scatter plot: median ZHVI vs median ZORI, colored by cluster tier.

    Steps:
    1. Load cluster labels: clusters = pd.read_csv("models/cluster_labels.csv")
    2. Aggregate df to one row per metro:
           summary = df.groupby('metro')[['zori','zhvi','rent_to_income']].mean()
    3. Merge summary with clusters on 'metro'
    4. Use plotly.express.scatter:
           x='zhvi', y='zori', color='cluster' (treat as string for discrete colors)
           text='metro', size='rent_to_income'
           hover_data=['rent_to_income']
    5. Add cluster tier labels in annotation (e.g. "Tier 1: Crisis")
    6. Title: "Metro Clusters: Home Value vs Rent (Affordability Tiers)"
    7. Save: fig.write_html("plots/cluster_scatter.html")

    Note: run modeling.py first — this chart requires models/cluster_labels.csv
    """
    raise NotImplementedError("Person 3 — implement cluster scatter (needs modeling.py first)")


def plot_deterioration(df: pd.DataFrame) -> None:
    """
    Horizontal bar chart: metros ranked by affordability deterioration 2016-2023.

    Steps:
    1. For each metro, compute:
           score = rent_to_income[2023] - rent_to_income[2016]
    2. Sort descending (worst deterioration at top)
    3. Use plotly.express.bar:
           x='deterioration_score', y='metro', orientation='h'
           color='deterioration_score', color_scale='Reds'
    4. Add a vertical line at x=0 (no change reference)
    5. Title: "Affordability Deterioration by Metro (2016-2023)"
    6. Save: fig.write_html("plots/deterioration.html")

    Expected result: LA, New York, Seattle near top; San Antonio, Austin near bottom
    """
    raise NotImplementedError("Person 3 — implement deterioration bar chart")


def plot_crisis_heatmap(df: pd.DataFrame) -> None:
    """
    Heatmap: metros (rows) x years (columns), colored by rent_to_income.

    Steps:
    1. Pivot: pivot = df.pivot(index='metro', columns='year', values='rent_to_income')
    2. Use plotly.express.imshow:
           color_continuous_scale='RdYlGn_r'
           zmin=0.15, zmax=0.50  (fix scale so 0.30 is the midpoint)
    3. Add a text annotation on each cell showing the value (round to 2 decimal)
    4. Add a bold outline or asterisk on cells where in_crisis == 1
    5. Title: "Rent-to-Income Heatmap: Metros x Year"
    6. Save: fig.write_html("plots/crisis_heatmap.html")

    This is the key summary chart — it shows at a glance which metros
    crossed the 30% threshold and when.
    """
    raise NotImplementedError("Person 3 — implement crisis heatmap")


def run_visualizations():
    """
    Generate all charts in sequence.

    Steps:
    1. df = pd.read_csv("data/master_housing.csv")
    2. Call each plot function, catch NotImplementedError gracefully
    3. Print paths of successfully generated HTML files

    Run order:
        plot_choropleth(df)      → plots/choropleth.html
        plot_trend_lines(df)     → plots/trend_lines.html
        plot_deterioration(df)   → plots/deterioration.html
        plot_crisis_heatmap(df)  → plots/crisis_heatmap.html
        plot_cluster_scatter(df) → plots/cluster_scatter.html  (needs modeling.py first)
    """
    raise NotImplementedError("Person 3 — wire up after implementing plot functions")


if __name__ == "__main__":
    print("visualizations.py — not implemented yet (Person 3)")
    print("Implement each plot function, then call run_visualizations().")
    print("Start with plot_trend_lines() and plot_crisis_heatmap() — no dependencies.")
    print("plot_cluster_scatter() requires models/cluster_labels.csv from Person 2.")
