"""
This script duplicates environments within the env0 platform.
It automates the process of retrieving environment configurations and creating duplicate environments within the same project.

Prerequisites:
- Python 3
- An API key, secret, and Organization ID for env0
- The `ENV0_ENVIRONMENT_IDS_TO_DUPLICATE` list populated with the IDs of the environments you wish to duplicate.

Usage:
python3 duplicate_environments.py

The script will:
- Retrieve the relevant data from the specified environments, including configurations and variables.
- Create new environments with the same configurations and settings as the original environments.
"""
import clients
import utils


ENV0_API_KEY = ''
ENV0_API_SECRET = ''
ENV0_ORGANIZATION_ID = ''

ENV0_ENVIRONMENT_IDS_TO_DUPLICATE = ['']

if __name__ == '__main__':
    env0_client = clients.env0.Env0APIClient(
        api_key=ENV0_API_KEY,
        api_secret=ENV0_API_SECRET,
    )
    
    for environment_id in ENV0_ENVIRONMENT_IDS_TO_DUPLICATE:
        environment_data = env0_client.get_environment(
            environment_id=environment_id,
        ) 
        environment_variables = env0_client.list_variables_by_scope(
            organization_id=ENV0_ORGANIZATION_ID,
            environment_id=environment_data['id']
        )
        duplicated_environment = env0_client.create_environment(
            environment_name=f"DUPLICATED-{environment_data.get('name')}",
            workspace_name=utils.randomize_workspace_name(),
            blueprint_id=environment_data.get('latestDeploymentLog', {}).get('blueprintId'),
            blueprint_revision=environment_data.get('latestDeploymentLog', {}).get('blueprintRevision'),
            blueprint_repository=environment_data.get('latestDeploymentLog', {}).get('blueprintRepository'),
            configuration_changes=environment_variables,
            continuous_deployment=environment_data.get('continuousDeployment'),
            pull_request_plan_deployments=environment_data.get('pullRequestPlanDeployments'),
            vcs_commands_alias=environment_data.get('vcsCommandsAlias'),
            auto_deploy_on_path_changes_only=environment_data.get('autoDeployOnPathChangesOnly'),
            project_id=environment_data.get('projectId'),
        )
