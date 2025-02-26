import json
import os
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

print(token_response.json())

# Pick the access token from the response
access_token = token_response.json()["access_token"]


### Using the NGI Live API
api_base_url = "https://api.ngilive.no"

if token_response.status_code == 200:
    print("Getting sensors...")
    api_response = requests.get(
        f"{api_base_url}/projects/{project_id}/sensors",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
    )

    print(f"Sensor response: {api_response.status_code}")
    print(json.dumps(api_response.json(), indent=2))

    ## Getting 100 datapoints

    api_response = requests.get(
        f"{api_base_url}/projects/{project_id}/datapoints/json_array_v0?{urlencode({
            "start" : "2023-01-01T09:15:30Z",
            "end" : "2025-01-01T09:15:30Z",
            "limit" : 100
            }
        )}",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
    )

    print(f"Sensor response: {api_response.status_code}")
    print(json.dumps(api_response.json(), indent=2))
else:
    print(f"Error: {token_response.status_code}, {token_response.text}")
