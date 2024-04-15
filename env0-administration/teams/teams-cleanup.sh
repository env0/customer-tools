#!/bin/bash

# Define the authorization credentials for the API calls
ENV0_TOKEN=""  #base64 encoded token copied from env0 UI when creating a new API key.
organization="" #organization id e.g. bde19c6d-d0dc-4b11-a951-8f43fe49db92

# Define the API call to retrieve all teams
GET_TEAMS_URL="https://api.env0.com/teams/organizations/$organization"

# Execute the API call to retrieve all teams and save the results to a temporary file
curl --request GET \
    --url "$GET_TEAMS_URL" \
    --header 'accept: application/json' \
    --header "authorization: Basic $ENV0_TOKEN" \
    --header 'content-type: application/json' \
    > teams.json

# Retrieve the team IDs from the temporary file
team_ids=$(jq -r '.[].id' teams.json)

# Loop through each team ID and delete the team
for team_id in $team_ids; do
    echo "Deleting team with ID: $team_id"
    curl --request DELETE \
        --url "https://api.env0.com/teams/$team_id" \
        --header 'accept: application/json' \
        --header "authorization: Basic $ENV0_TOKEN" \
        --header 'content-type: application/json'
done

# Remove the temporary file
rm teams.json
