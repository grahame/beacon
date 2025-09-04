import requests
import datetime

EMERGENCY_WA_BASE = "https://api.emergency.wa.gov.au/v1/"
EMERGENCY_WA_ENDPOINTS = [
    "warnings",
    # "incidents",
    # "centres",
    # "closures",
    # "events",
    # "total-fire-bans",
]


def get_latest_data():
    # we join together the data from all endpoints into a single dictionary
    data = {}
    for endpoint in EMERGENCY_WA_ENDPOINTS:
        url = f"{EMERGENCY_WA_BASE}{endpoint}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:141.0) Gecko/20100101 Firefox/141.0 Beacon/1.0"
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch data from {url}: {response.status_code}")
        data[endpoint] = response.json()
    return data
