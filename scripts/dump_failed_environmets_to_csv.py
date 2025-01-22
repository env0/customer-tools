"""
This script retrieves failed environments from the env0 API and exports them to a CSV file.

It uses the `env0` client to list all environments associated with the specified organization ID.
Environments with a status of 'FAILED' are filtered and written to a CSV file defined by `OUTPUT_FILE_PATH`.

Constants:
- `ENV0_API_KEY`: API key for authenticating with the env0 API.
- `ENV0_API_SECRET`: API secret for authenticating with the env0 API.
- `ENV0_ORGANIZATION_ID`: ID of the organization whose environments are being queried.
- `STATUS_FAILED`: The status used to filter environments.
- `OUTPUT_FILE_PATH`: File path for the output CSV.

Usage:
- Run the script as a standalone module to generate the CSV file of failed environments.

Example Output:
- A CSV file named `failed_environments.csv` containing details of all failed environments.

Usage:
 python3 dump_failed_environmets_to_csv.py
"""
import csv

import clients


ENV0_API_KEY = ''
ENV0_API_SECRET = ''
ENV0_ORGANIZATION_ID = ''

STATUS_FAILED = 'FAILED'
OUTPUT_FILE_PATH = 'failed_environments.csv'


if __name__ == '__main__':
    env0_client = clients.env0.Env0APIClient(
        api_key=ENV0_API_KEY,
        api_secret=ENV0_API_SECRET,
    )
    
    failed_environments = [
        env for env in env0_client.list_environments(organization_id=ENV0_ORGANIZATION_ID)
        if env['status'] == STATUS_FAILED
    ]
    
    with open(
        OUTPUT_FILE_PATH, 
        mode='w', 
        newline='',
    ) as csv_file:
        fieldnames = failed_environments[0].keys() if failed_environments else []

        writer = csv.DictWriter(
            csv_file, 
            fieldnames=fieldnames,
        )
        writer.writeheader()
        writer.writerows(failed_environments)