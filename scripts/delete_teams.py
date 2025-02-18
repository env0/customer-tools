"""
Script to list and delete teams in an env0 organization.

This script uses the env0 API client to retrieve all teams associated with a given
organization and deletes them.

Prerequisites:
- `clients` module must be available and contain the `env0.Env0APIClient` class.
- `ENV0_API_KEY`, `ENV0_API_SECRET`, and `ENV0_ORGANIZATION_ID` must be set with 
  valid credentials.

Workflow:
1. Initializes an `Env0APIClient` using API credentials.
2. Retrieves the list of teams within the specified env0 organization.
3. Iterates over the teams and deletes each one.

Note:
- Ensure that `ENV0_API_KEY`, `ENV0_API_SECRET`, and `ENV0_ORGANIZATION_ID` 
  contain valid values before executing the script.
- This script irreversibly deletes all teams in the organization. Use with caution.

Example Usage:
```bash
python delete_env0_teams.py
"""
import clients


ENV0_API_KEY = ''
ENV0_API_SECRET = ''
ENV0_ORGANIZATION_ID = ''


if __name__ == '__main__':
    env0_client = clients.env0.Env0APIClient(
        api_key=ENV0_API_KEY,
        api_secret=ENV0_API_SECRET,
    )
    
    teams = env0_client.list_teams(organization_id=ENV0_ORGANIZATION_ID)
    
    # Filter Team IDs
    
    
    # Delete Teams
    for team in teams:
        env0_client.delete_team(
            team_id=team['id']
        )
