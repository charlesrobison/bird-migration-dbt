from dagster import schedule
from datetime import time
from dags.ebird_pipeline import ebird_update_job

@schedule(
    cron_schedule="0 * * * *",  # runs every hour at minute 0
    job=ebird_update_job,
    execution_timezone="UTC"
)
def hourly_ebird_schedule():
    return {}
