"""
main.py  —  Housing Affordability Crisis Analysis
Orchestrates the full pipeline: ETL → Modeling → Visualizations.

TODO: wire up run_all() once all three modules are complete.
"""

from etl_pipeline import load_zillow_wide          # noqa: F401  (Day 2+)
from modeling import run_modeling                   # noqa: F401  (Day 2+)
from visualizations import run_visualizations       # noqa: F401  (Day 2+)


def run_all():
    """Run ETL, modeling, and visualization pipelines end-to-end."""
    # TODO Day 3: uncomment once all modules are implemented
    # run_etl()
    # run_modeling()
    # run_visualizations()
    print("Pipeline not fully implemented yet — check back after Day 3.")


if __name__ == "__main__":
    run_all()
