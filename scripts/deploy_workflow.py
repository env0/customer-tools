"""
A script for deploying an environment using the env0 API client.

This script demonstrates how to deploy an environment by configuring and triggering a workflow via the env0 API.
It sets up authentication using API credentials, defines a deployment payload with various configuration 
changes and sub-environment settings, and then executes the deployment.

Globals:
    ENV0_API_KEY (str): The API key for authenticating with the env0 API.
    ENV0_API_SECRET (str): The API secret for authenticating with the env0 API.
    ENVIRONMENT_ID_TO_DEPLOY (str): The unique identifier of the environment to be deployed.
    payload (dict): A dictionary defining the deployment configuration, which includes:
        - configurationChanges: General configuration changes (with type, name, and value).
        - ttl: The time-to-live setting for the environment (e.g., "INFINITE").
        - subEnvironments: A mapping of sub-environment names to their respective configurations. 
          Each sub-environment (e.g., "vnet", "aks", "flux") includes:
              * revision: The version or branch of the configuration.
              * workspaceName: The name of the workspace.
              * configurationChanges: A list of configuration change dictionaries specific to the sub-environment.
        - workflowDeploymentOptions: Options that define the deployment workflow, such as:
              * operation: The deployment operation to perform (e.g., "run-from-here").
              * node: The specific node within the sub-environments to target (e.g., "vnet").

Usage:
    1. Set the ENV0_API_KEY, ENV0_API_SECRET, and ENVIRONMENT_ID_TO_DEPLOY variables with valid credentials 
       and identifiers.
    2. Modify the payload dictionary as needed to adjust configuration changes and sub-environment settings.
    3. Run the script:
        python3 deploy_workflow.py

    When executed, it will:
         - Instantiate the Env0APIClient with the provided API credentials.
         - Call the deploy_environment method using the specified environment ID and payload.
         - Store the result of the deployment in the deploy_workflow variable.
"""
import clients

ENV0_API_KEY = ''
ENV0_API_SECRET = ''

ENVIRONMENT_ID_TO_DEPLOY = ''
payload = {
    "configurationChanges": {
        "type": 0,
        "name": "kosta",
        "value": "kosta"
    },
    "ttl": {
        "type": "INFINITE",
    },
    "subEnvironments": {
        "vnet": { 
            "revision": "main",
            "workspaceName": "dfdf",
            "configurationChanges": [
                {
                    "type": 1,
                    "name": "my_variable",
                    "value": "my_value",
                }
            ]
        },
        "aks": {
            "revision": "main",
            "workspaceName": "dfdf",
            "configurationChanges": [
                {
                    "type": 0,
                    "name": "my_variable2",
                    "value": "my_value2",
                }
            ]
        },
        "flux": {
            "revision": "main",
            "workspaceName": "dfdf",
            "configurationChanges": [
                {
                    "type": 0,
                    "name": "my_variable3",
                    "value": "my_value3",
                }
            ]
        }
    },
    "workflowDeploymentOptions": {
        "operation": "run-from-here",
        "node": "vnet"
    }
}


if __name__ == '__main__':
    env0_client = clients.env0.Env0APIClient(
        api_key=ENV0_API_KEY,
        api_secret=ENV0_API_SECRET,
    )
    
    deploy_workflow = env0_client.deploy_environment(
        environment_id=ENVIRONMENT_ID_TO_DEPLOY,
        params=payload,
    )
    
