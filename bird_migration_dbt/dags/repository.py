from dagster import repository
from dags.schedules import hourly_ebird_schedule
from dags.ebird_pipeline import ebird_update_job

@repository
def my_repository():
    return [
        ebird_update_job,
        hourly_ebird_schedule
    ]
