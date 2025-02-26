import json
import os
import sys
from time import sleep
from urllib.parse import urlencode

import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)

# Constants
keycloak_url = "https://keycloak.ngiapi.no/auth/realms/tenant-geohub-public/protocol/openid-connect/token"
client_id = os.environ.get("KEYCLOAK_CLIENT_ID")
client_secret = os.environ.get("KEYCLOAK_CLIENT_SECRET")
project_id = os.environ.get("PROJECT_ID")

if not (client_id and client_secret):
    print("Client ID or secret not found in environment variables.")
    # Handle the case where environment variables are not set
    exit()

# Set up the payload for the token request
token_data = {
    "grant_type": "client_credentials",
    "client_id": client_id,
    "client_secret": client_secret,
}

# Make a POST request to the token endpoint
token_response = requests.post(keycloak_url, data=token_data)

# Pick the access token from the response
access_token = token_response.json()["access_token"]

# Print the token (for use with Swagger UI)
print(token_response.json())

# Using the NGI Live API
api_base_url = "https://api.ngilive.no"

if token_response.status_code != 200:
    print(f"Error: {token_response.status_code}, {token_response.text}")
    sys.exit(1)

# Request sensor metadata and print result
print("Getting sensors...")
api_response = requests.get(
    f"{api_base_url}/projects/{project_id}/sensors",
    headers={
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    },
)

print(f"Sensor response: {api_response.status_code}")
resp = api_response.json()
print(json.dumps(resp, indent=2))

# Request parameters for datapoints
LIMIT = 1000
START = "2025-02-24T09:15:30Z"
END = "2025-03-01T09:15:30Z"

# Create a dict to hold all sensor data
all_sensor_data = {s["name"]: [] for s in resp["sensors"]}

# Loop over all sensors and request data in pages with size LIMIT
for sensor, sensor_data in all_sensor_data.items():
    offset = 0
    while True:
        sleep(0.11)

        # Request LIMIT datapoints at a time
        url = f"{api_base_url}/projects/{project_id}/datapoints/json_array_v0?{urlencode({
                "name": sensor,
                "start" : START, 
                "end" : END, 
                "limit" : LIMIT,
                "offset" : offset, 
                }
            )}"

        api_response = requests.get(
            url,
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            },
        )

        # Print response code for this page
        print(f"{f"{sensor} (page {offset // LIMIT}):": <20} STATUS {api_response.status_code}")
        
        # Extract data and add to dict of sensor data
        resp = api_response.json()
        page, *_ = resp["data"]
        sensor_data.extend(page["data"])

        # Go to next sensor if we've fetched all data for this sensor
        if len(page["data"]) < LIMIT:
            break
        else:
            offset += LIMIT

print(all_sensor_data)
