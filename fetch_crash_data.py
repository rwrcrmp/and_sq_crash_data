# Import the 'requests' library for making HTTP requests (similar to httr in R)
# This is not part of Python's standard library, so it must be installed via pip
import requests

# Import the 'json' library for working with JSON data (built into Python)
# Provides functions to convert between Python objects and JSON strings
import json

# Define the API endpoint URL
# This is Austin's open data portal (Socrata SODA API) containing crash data
url = "https://data.austintexas.gov/resource/y2wy-tgr5.json"

# Define the date filter for 2024 and 2025
# Using SoQL (Socrata Query Language) syntax
date_filter = "crash_timestamp_ct >= '2024-01-01T00:00:00' AND crash_timestamp_ct < '2026-01-01T00:00:00'"

# Initialize an empty list to store all records across multiple API calls
# In Python, lists are similar to vectors in R but can hold mixed types
all_records = []

# Set pagination parameters
# limit: maximum number of records to fetch per request (API caps at 1000)
# offset: starting position for each request (used to paginate through results)
limit = 1000
offset = 0

# Start an infinite loop that will continue until we explicitly break out
# We use this pattern because we don't know how many total records exist
while True:
    # Create a dictionary of query parameters to send with the request
    # $limit: tells the API how many records to return
    # $offset: tells the API where to start (skip this many records)
    # $where: filter condition for date range
    # $order: sort by date for consistent pagination
    params = {
        "$limit": limit,
        "$offset": offset,
        "$where": date_filter,
        "$order": "crash_timestamp_ct DESC"
    }

    # Make an HTTP GET request to the API
    # requests.get() sends the request and returns a Response object
    # The params argument automatically appends the query string to the URL
    response = requests.get(url, params=params)

    # Check if the request was successful
    # HTTP status code 200 means "OK" - the request succeeded
    # Any other code (like 404 or 500) indicates an error
    if response.status_code != 200:
        # f-strings (f"...") allow embedding variables directly in strings
        # Similar to paste0() or glue() in R
        print(f"Error: {response.status_code}")
        break

    # Parse the JSON response into a Python list
    # .json() converts the response body from JSON text to Python objects
    # Similar to jsonlite::fromJSON() in R
    # The SODA API returns a direct array of records (not nested under a key)
    records = response.json()

    # Check if we received any records
    # An empty list evaluates to False in Python, so "not records" is True when empty
    # This is our exit condition - no more data to fetch
    if not records:
        break

    # Add the new records to our master list
    # .extend() adds each item from records individually to all_records
    # (Unlike .append() which would add the entire list as a single item)
    all_records.extend(records)

    # Print progress update showing total records fetched so far
    # len() returns the number of items in a list (like length() in R)
    print(f"Fetched {len(all_records)} records...")

    # Move the offset forward for the next iteration
    # This ensures we fetch the next batch of records, not the same ones
    offset += limit

# Save the collected data to a JSON file
# open() creates/opens a file; "w" means write mode (overwrites if exists)
# "as f" assigns the file object to variable f
# The "with" statement automatically closes the file when done (even if errors occur)
with open("crash_data.json", "w") as f:
    # json.dump() writes Python objects to a file as JSON
    # indent=2 formats the output with 2-space indentation for readability
    json.dump(all_records, f, indent=2)

# Print final confirmation with total record count
print(f"Saved {len(all_records)} total records to crash_data.json")
