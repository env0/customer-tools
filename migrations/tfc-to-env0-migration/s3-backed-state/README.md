# TFC to env0 Migration - S3 Backed State

This script can be used to migrate a single workspace in Terraform Cloud to env0.

## Prerequisites

- Clone this repository.
- Create a file named "inputs.txt" and populate it with the below, changing INSERT to the relevant data.

tfcOrgName="INSERT"

tfcWorkspaceID="INSERT"

tfcBearerToken="INSERT"


env0OrgID="INSERT"

env0ProjectID="INSERT"

env0BearerToken="INSERT"

## Migrate from TFC to env0

Execute the script using the below command.

./tfc2env0.sh

# Use cases

Currently this will migrate a single workspace from TFC to env0 when the state is stored remotely (i.e. AWS S3 bucket).
