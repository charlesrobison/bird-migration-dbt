from dagster import job, op
import subprocess
import sys
from pathlib import Path
import os

@op
def fetch_ebird_data():
    result = subprocess.run([sys.executable, "scripts/ingest_ebird_recent.py"], capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Fetch script failed:\n{result.stderr}")
    print(result.stdout)
    return Path("data/raw/ebird.csv").resolve()

@op
def build_dbt_models(_):
    try:
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    except NameError:
        # __file__ not defined, fallback to current working directory
        project_root = os.getcwd()

    result = subprocess.run(
        ["dbt", "build", "--select", "stg_recent_observations"],
        cwd=project_root,
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"dbt run failed:\n{result.stderr}")
    print(result.stdout)

@job
def ebird_update_job():
    fetch_ebird_data()
    build_dbt_models()

