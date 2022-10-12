# customer-tools

This script can be used to migrate a single workspace in Terraform Cloud to env0.

## Prerequisites

- Clone this repository.
- Create a file named "inputs.txt" and populate it with the below, changing INSERT to the relevant data.

tfcOrgName="INSERT" \n
tfcWorkspaceID="INSERT" \n
tfcBearerToken="INSERT" \n

env0OrgID="INSERT" \n
env0ProjectID="INSERT" \n
env0BearerToken="INSERT" \n

## Migrate from TFC to env0

Execute the script using the below command.

./tfc2env0.sh

## Remaining Tasks

- Include code to migrate state.