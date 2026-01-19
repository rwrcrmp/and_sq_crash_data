# Austin Crash Data Extract

Python scripts to fetch and process crash records from Austin's Open Data Portal.

## Setup

```cmd
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Scripts

### fetch_crash_data.py
Fetches crash records from the [Austin Open Data Portal](https://data.austintexas.gov/) (Socrata API) for 2024-2025. Saves results to `data/crash_data.json`.

```cmd
python fetch_crash_data.py
```

### json_to_shapefile.py
Reads the JSON data, filters crashes within a specified radius of a reference point, and exports to:
- Shapefile (`outputs/crash_records_extract/crash_data.shp`)
- CSV (`outputs/crash_records_extract/crash_data.csv`)

```cmd
python json_to_shapefile.py
```

## Data Source

- **Dataset**: Austin Crash Report Data
- **Endpoint**: `https://data.austintexas.gov/resource/y2wy-tgr5.json`
- **ID**: y2wy-tgr5
