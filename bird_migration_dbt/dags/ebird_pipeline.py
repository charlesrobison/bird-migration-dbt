from dagster import job, op
import subprocess
import sys
from pathlib import Path

@op
def fetch_ebird_data():
    result = subprocess.run([sys.executable, "etl/fetch_ebird.py"], capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Fetch script failed:\n{result.stderr}")
    print(result.stdout)
    return Path("data/raw/ebird.csv").resolve()

@op
def run_dbt_models(_):
    result = subprocess.run(["dbt", "run", "--select", "stg_recent_observations"], capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"dbt run failed:\n{result.stderr}")
    print(result.stdout)

@op
def run_dbt_tests(_):
    result = subprocess.run(["dbt", "test"], capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"dbt tests failed:\n{result.stderr}")
    print(result.stdout)

@job
def ebird_update_job():
    fetch_ebird_data()
    run_dbt_models()
    run_dbt_tests()
