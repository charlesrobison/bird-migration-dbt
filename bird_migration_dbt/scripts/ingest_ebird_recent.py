# scripts/ingest_ebird_recent.py

import requests
import pandas as pd
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import os

# Configuration
load_dotenv()  # Load environment variables from .env file
API_KEY = os.getenv("EBIRD_API_KEY")
REGION = "US-NY"  # eBird region code
OUTPUT_PATH = Path("data/recent_bird_obs.csv")

def fetch_recent_observations(api_key: str, region: str) -> pd.DataFrame:
    url = f"https://api.ebird.org/v2/data/obs/{region}/recent"
    headers = {"X-eBirdApiToken": api_key}

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    data = response.json()
    df = pd.DataFrame(data)

    if not df.empty:
        df["fetch_timestamp"] = datetime.utcnow().isoformat()

    return df

def main():
    Path("data").mkdir(exist_ok=True)
    df = fetch_recent_observations(API_KEY, REGION)

    if df.empty:
        print("No recent observations found.")
    else:
        df.to_csv(OUTPUT_PATH, index=False)
        print(f"Wrote {len(df)} records to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
