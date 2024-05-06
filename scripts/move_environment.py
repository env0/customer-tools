"""
This script is designed to move environments from one project to another within the env0 platform.
It automates the process of archiving specified environments and recreating them in a new project with identical configurations.

Prerequisites:
- Python 3
- An API key and secret for env0
- The `ENV0_ENVIRONMENT_IDS_TO_MOVE` list populated with the IDs of the environments you wish to migrate.
- The `ENV0_PROJECT_ID_TO_MOVE_TO` variable set to the ID of the project you are moving the environments to.

Usage:
python3 move_environments.py

The script will:
- Retrieve the relevant data from the archived environments, including configurations and variables.
- Archive each environment specified in the `ENV0_ENVIRONMENT_IDS_TO_MOVE` list.
- Create new environments with the same configurations in the target project specified by `ENV0_PROJECT_ID_TO_MOVE_TO`.
"""
import clients


ENV0_API_KEY = ''
ENV0_API_SECRET = ''

ENV0_ENVIRONMENT_IDS_TO_MOVE = ['8533be85-57f5-4cf7-b14f-00538e5ea156']
ENV0_PROJECT_ID_TO_MOVE_TO = '989a5109-9f40-4770-970b-2e64bba46393'


if __name__ == '__main__':
    env0_client = clients.env0.Env0APIClient(
        api_key=ENV0_API_KEY,
        api_secret=ENV0_API_SECRET,
    )
    
    for environment_id in ENV0_ENVIRONMENT_IDS_TO_MOVE:
        environment_data = env0_client.get_environment(
            environment_id=environment_id,
        ) 
        env0_client.archive_environment(
            environment_id=environment_id,
        )
        template_is_used = not environment_data.get('isSingleUseBlueprint')
        if template_is_used:
            pass
            # TODO 
            # assign template to the new project
            # create new environment with the assigned template
        new_environment_in_new_project = env0_client.create_environment(
            environment_name=environment_data.get('name'),
            workspace_name=environment_data.get('workspaceName'),
            custom_env0_environment_variables_commit_hash=environment_data.get('customEnv0EnvironmentVariables', {}).get('commitHash'),
            custom_env0_environment_variables_commit_url=environment_data.get('customEnv0EnvironmentVariables', {}).get('commitUrl'),
            blueprint_id=environment_data.get('latestDeploymentLog', {}).get('blueprintId'),
            blueprint_revision=environment_data.get('latestDeploymentLog', {}).get('blueprintRevision'),
            blueprint_repository=environment_data.get('latestDeploymentLog', {}).get('blueprintRepository'),
            continuous_deployment=environment_data.get('continuousDeployment'),
            pull_request_plan_deployments=environment_data.get('pullRequestPlanDeployments'),
            vcs_commands_alias=environment_data.get('vcsCommandsAlias'),
            auto_deploy_on_path_changes_only=environment_data.get('autoDeployOnPathChangesOnly'),
            project_id=ENV0_PROJECT_ID_TO_MOVE_TO,
        )
