# Bird Migration Data Pipeline

## Overview
This project demonstrates a full data engineering pipeline that ingests bird migration observation data from the eBird API, processes it using dbt and DuckDB, orchestrates workflows with Dagster, and visualizes results with Streamlit.  An API key is required and can be requested directly from Cornell Lab.

## Project Components

- **Data Ingestion:**  
  Python scripts fetch recent bird observations and store raw data in CSV format.

- **Data Modeling:**  
  dbt models in DuckDB curate and incrementally build staging tables for recent bird observations.

- **Orchestration:**  
  Dagster manages job scheduling, running dbt builds and tests automatically via defined jobs and schedules.

- **Visualization:**  
  Streamlit app connects directly to the DuckDB database for interactive exploration of bird migration data.

## Setup & Installation

1. Clone the repo  
   ```bash
   git clone <repo_url>
   cd bird-migration-dbt

2. Create and activate virtual environment
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate

3. Install dependencies
   ```bash
   pip install -r requirements.txt

4. Export environment variables
   ```bash
   export DAGSTER_HOME=~/dagster_home
   export EBIRD_API_KEY=your_ebird_api_key
   export PROJECT_ROOT=$(pwd)

## Running the Pipeline

### Dagster

- Start the Dagster webserver:
  ```bash
     dagster-webserver -f dags/repository.py

- Start the Dagster daemon to enable scheduled runs:
  ```bash
     dagster-daemon run

- Access Dagster UI at http://localhost:3000 to monitor jobs and runs.

### dbt

- Run dbt build manually (optional):
  ```bash
  dbt build --select stg_recent_observations

### Streamlit Visualization

- Run the Streamlit app:
  ```bash
  streamlit run app.py

- View the app at http://localhost:8501

## Project Structure
```
bird-migration-dbt/
├── dags/
│   ├── ebird_pipeline.py      # Dagster job definitions and ops
│   ├── repository.py          # Dagster repository aggregating jobs and schedules
│   ├── schedules.py           # Dagster schedules
│   └── __init__.py
├── models/                    # dbt models directory
│   └── staging/
│       └── stg_recent_observations.sql
├── data/
│   └── recent_bird_obs.csv    # Raw data CSV (optional)
├── dev.duckdb                 # Development DuckDB database file
├── prod.duckdb                # Production DuckDB database file (optional)
├── app.py                    # Streamlit app to visualize data
├── requirements.txt
├── README.md
└── ...
```

## Notes & Next Steps

- The pipeline currently runs on an hourly schedule via Dagster’s scheduler daemon.
- The DuckDB file stores the curated bird migration data for quick local querying.
- Streamlit app uses this DuckDB file directly to create interactive visualizations.
- Future improvements:
* Add more detailed tests and validations in dbt.
* Deploy Streamlit app publicly (e.g., Streamlit Cloud).
* Integrate Tableau for advanced BI dashboards.
* Expand ingestion with historical data and richer features.
