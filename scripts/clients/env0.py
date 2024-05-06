import requests

from . import _http_client


class Env0APIClient(
    _http_client.HttpClient,
):
    base_url = 'https://api.env0.com'
    
    def __init__(
        self,
        api_key,
        api_secret,
    ):
        session = requests.session()
        session.auth = requests.auth.HTTPBasicAuth(
            username=api_key,
            password=api_secret,
        )

        self.session = session
        self.headers = {
            'accept': 'application/json',
            'content-type': 'application/json'
        }
        
    def create_new_provider(
        self,
        provider_type,
        org_id,
    ):
        response = self.send_request(
            method=self.session.post,
            url=f'{self.base_url}/providers',
            params={
                'type': provider_type,
                'organizationId': org_id,
            },
            headers=self.headers,
        )
        
        return response
    
    def create_module(
        self,
        module_name,
        module_provider,
        repository,
        org_id,
        module_type='module',
    ):
        response = self.send_request(
            method=self.session.post,
            url=f'{self.base_url}/modules',
            params={
                'type': module_type,
                'moduleName': module_name,
                'moduleProvider': module_provider,
                'repository': repository,
                'organizationId': org_id,
                
            },
            headers=self.headers,
        )
        
        return response

    def archive_environment(
        self,
        environment_id,
    ):
        response = self.send_request(
            method=self.session.put,
            url=f'{self.base_url}/environments/{environment_id}',
            params={
                'isArchived': True,
            },
            headers=self.headers,
        )
        
        return response
    
    def get_environment(
        self,
        environment_id,
    ):
        response = self.send_request(
            method=self.session.get,
            url=f'{self.base_url}/environments/{environment_id}',
            headers=self.headers,
            json_response=True,
        )
        
        return response

    def create_environment(
        self,
        environment_name,
        workspace_name,
        project_id,
        blueprint_id,
        blueprint_revision,
        blueprint_repository,
        custom_env0_environment_variables_commit_hash,
        custom_env0_environment_variables_commit_url,
        continuous_deployment,
        pull_request_plan_deployments,
        vcs_commands_alias,
        auto_deploy_on_path_changes_only,
    ):
        response = self.send_request(
            method=self.session.post,
            url=f'{self.base_url}/environments/',
            params={
                'name': environment_name,
                'workspaceName': workspace_name,
                'projectId': project_id,
                'continuousDeployment': continuous_deployment,
                'pullRequestPlanDeployments': pull_request_plan_deployments,
                'vcsCommandsAlias': vcs_commands_alias,
                'autoDeployOnPathChangesOnly': auto_deploy_on_path_changes_only,
                'ttl': {
                    'type': 'INFINITE',
                },
                'customEnv0EnvironmentVariables': {
                    'commitHash': custom_env0_environment_variables_commit_hash,
                    'commitUrl': custom_env0_environment_variables_commit_url,
                },
                'configurationChanges': {
                    'name': 'a',
                    'type': 0,
                },
                'deployRequest': {
                    'configurationChanges': {
                        'type': 0,
                        'name': 'a'
                    },
                    'ttl': {
                        'type': 'INFINITE',
                    },
                    'blueprintId': blueprint_id,
                    'blueprintRevision': blueprint_revision,
                    'blueprintRepository': blueprint_repository,
                },
            },
            headers=self.headers,
        )
        
        return response
