import sys
import os
import requests
import json
from datetime import datetime

# Check for correct number of command-line arguments
if len(sys.argv) != 2:
    print("Usage: {} <organization>/<workspace>".format(sys.argv[0]))
    sys.exit(1)


if 'ENV0_TOKEN' in os.environ:
            TOKEN = os.environ['ENV0_TOKEN']
else:
            logger.error("Error: Environment variable 'ENV0_TOKEN' missing")
            exit(1)

# Extract command-line arguments
ORG_NAME, WORKSPACE_NAME = sys.argv[1].split('/')




UPLOAD_FILE_NAME = "./content-{}.tar.gz".format(int(datetime.now().timestamp()))

env0_remote_backend_host = "backend.api.env0.com"
env0_api_host = "api.env0.com"

# Define API endpoints
CREATE_WORKSPACE_URL = f"https://{env0_remote_backend_host}/api/v2/organizations/{ORG_NAME}/workspaces"

# Define request headers
headers = {
    "Authorization": "Bearer {}".format(TOKEN),
    "Content-Type": "application/vnd.api+json"
}

# Create workspace data
create_workspace_data = {
    "data": {
        "type": "workspaces",
        "attributes": {
            "name": WORKSPACE_NAME,
            "terraform_version": "1.5.7"
        }
    }
}

# Make POST request to create workspace
workspace_response = requests.post(CREATE_WORKSPACE_URL, headers=headers, json=create_workspace_data)

# Check if request was successful
if workspace_response.status_code != 200:
    print("Failed to create workspace. Status code:", workspace_response.status_code)
    sys.exit(1)

# Extract workspace ID from response
WORKSPACE_ID = workspace_response.json()['data']['id']
print("Workspace ID:", WORKSPACE_ID)

# Define update workspace data
update_workspace_data = {
    "isRemoteApplyEnabled": True
}

UPDATE_WORKSPACE_URL = f"https://{env0_api_host}/environments/{WORKSPACE_ID}"


# Make PUT request to update workspace
update_response = requests.put(UPDATE_WORKSPACE_URL, headers=headers, json=update_workspace_data)

# Check if request was successful
if update_response.status_code != 200:
    print("Failed to update workspace. Status code:", update_response.status_code)
    sys.exit(1)

print("Environment created successfully")