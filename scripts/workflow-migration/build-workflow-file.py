import os
import sys
import json
import base64
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError

# --- Configuration ---
ENV0_API_KEY = os.getenv('ENV0_API_KEY')
ENV0_API_SECRET = os.getenv('ENV0_API_SECRET')
API_BASE_URL = 'https://api.env0.com'

def create_auth_header():
    """Create Basic Auth header for env0 API."""
    credentials = f"{ENV0_API_KEY}:{ENV0_API_SECRET}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    return f"Basic {encoded_credentials}"

def format_yaml_output(data, indent=0):
    """Convert dictionary to YAML-like format using built-in functions."""
    result = []
    spaces = "  " * indent
    
    for key, value in data.items():
        if isinstance(value, dict):
            result.append(f"{spaces}{key}:")
            result.append(format_yaml_output(value, indent + 1))
        elif isinstance(value, list):
            result.append(f"{spaces}{key}:")
            for item in value:
                if isinstance(item, dict):
                    result.append(f"{spaces}  -")
                    result.append(format_yaml_output(item, indent + 2))
                else:
                    result.append(f"{spaces}  - {item}")
        elif value is None:
            result.append(f"{spaces}{key}: null")
        elif isinstance(value, bool):
            result.append(f"{spaces}{key}: {str(value).lower()}")
        elif isinstance(value, str):
            # Handle strings that might need quoting
            if any(char in value for char in ['"', "'", '\n', '\r', '\t']) or value.strip() != value:
                result.append(f'{spaces}{key}: "{value}"')
            else:
                result.append(f"{spaces}{key}: {value}")
        else:
            result.append(f"{spaces}{key}: {value}")
    
    return "\n".join(result)

# --- Helper Functions ---
def get_environment(environment_id):
    """Fetches a specific environment by its ID."""
    try:
        url = f"{API_BASE_URL}/environments/{environment_id}"
        headers = {
            'accept': 'application/json',
            'content-type': 'application/json',
            'authorization': create_auth_header()
        }
        
        request = Request(url, headers=headers)
        with urlopen(request) as response:
            response_text = response.read().decode()
            if not response_text.strip():
                print(f"Error: Empty response from API for environment {environment_id}", file=sys.stderr)
                return None
            return json.loads(response_text)
    except HTTPError as err:
        print(f"An HTTP error occurred while fetching environment {environment_id}: {err.code} - {err.reason}", file=sys.stderr)
        # Try to read error response body
        try:
            error_body = err.read().decode()
            print(f"Error response body: {error_body}", file=sys.stderr)
        except:
            pass
        return None
    except URLError as err:
        print(f"A network error occurred while fetching environment {environment_id}: {err.reason}", file=sys.stderr)
        return None
    except json.JSONDecodeError as err:
        print(f"JSON decode error for environment {environment_id}: {err}", file=sys.stderr)
        return None
    except Exception as err:
        print(f"An error occurred: {err}", file=sys.stderr)
        return None

def get_blueprint(blueprint_id):
    """Fetches a specific blueprint by its ID."""
    try:
        url = f"{API_BASE_URL}/blueprints/{blueprint_id}"
        headers = {
            'accept': 'application/json',
            'content-type': 'application/json',
            'authorization': create_auth_header()
        }
        
        request = Request(url, headers=headers)
        with urlopen(request) as response:
            response_text = response.read().decode()
            if not response_text.strip():
                print(f"Error: Empty response from API for blueprint {blueprint_id}", file=sys.stderr)
                return None
            return json.loads(response_text)
    except HTTPError as err:
        print(f"An HTTP error occurred while fetching blueprint {blueprint_id}: {err.code} - {err.reason}", file=sys.stderr)
        # Try to read error response body
        try:
            error_body = err.read().decode()
            print(f"Error response body: {error_body}", file=sys.stderr)
        except:
            pass
        return None
    except URLError as err:
        print(f"A network error occurred while fetching blueprint {blueprint_id}: {err.reason}", file=sys.stderr)
        return None
    except json.JSONDecodeError as err:
        print(f"JSON decode error for blueprint {blueprint_id}: {err}", file=sys.stderr)
        return None
    except Exception as err:
        print(f"An error occurred while fetching blueprint {blueprint_id}: {err}", file=sys.stderr)
        return None

def main():
    """Main function to generate the workflow file."""
    if not all([ENV0_API_KEY, ENV0_API_SECRET]):
        print("Error: ENV0_API_KEY and ENV0_API_SECRET environment variables must be set.", file=sys.stderr)
        sys.exit(1)

    # Get environment IDs from command line arguments
    environment_ids = sys.argv[1:]
    if not environment_ids:
        print("Usage: python build-workflow-file.py <environment_id_1> <environment_id_2> ...", file=sys.stderr)
        sys.exit(1)

    print(f"Processing {len(environment_ids)} environments...", file=sys.stderr)

    workflow_environments = {}

    print("Fetching detailed data for each environment...", file=sys.stderr)
    for env_id in environment_ids:
        # 1. Get Environment details
        env_data = get_environment(env_id)
        if not env_data:
            continue

        env_name = env_data.get('name')
        workspace_name = env_data.get('workspaceName')
        blueprint_id = env_data.get('latestDeploymentLog', {}).get('blueprintId')

        if not all([env_name, workspace_name, blueprint_id]):
            print(f"Warning: Missing critical data for environment ID {env_id}. Skipping.", file=sys.stderr)
            continue
            
        # 2. Get Blueprint details
        blueprint_data = get_blueprint(blueprint_id)
        if not blueprint_data:
            continue

        # 3. Construct the base definition for the environment
        env_definition = {
            'name': env_name
        }

        # 4. Conditionally add 'vcs' or 'templateName' based on 'isSingleUse'
        is_single_use = blueprint_data.get('isSingleUse', False)
        
        if is_single_use:
            # For single-use blueprints, define infrastructure inline using VCS
            vcs_details = {
                'type': blueprint_data.get('type')
            }
            
            # Add version fields first (following example format)
            if blueprint_data.get('terraformVersion'):
                vcs_details['terraformVersion'] = blueprint_data.get('terraformVersion')
            if blueprint_data.get('opentofuVersion'):
                vcs_details['opentofuVersion'] = blueprint_data.get('opentofuVersion')
            if blueprint_data.get('terragruntVersion'):
                vcs_details['terragruntVersion'] = blueprint_data.get('terragruntVersion')
            if blueprint_data.get('pulumiVersion'):
                vcs_details['pulumiVersion'] = blueprint_data.get('pulumiVersion')
            if blueprint_data.get('ansibleVersion'):
                vcs_details['ansibleVersion'] = blueprint_data.get('ansibleVersion')
                
            # Add repository and path
            if blueprint_data.get('repository'):
                vcs_details['repository'] = blueprint_data.get('repository')
            if blueprint_data.get('path'):
                vcs_details['path'] = blueprint_data.get('path')
                
            # Add VCS provider specific fields
            if blueprint_data.get('githubInstallationId'):
                vcs_details['githubInstallationId'] = blueprint_data.get('githubInstallationId')
            if blueprint_data.get('bitbucketClientKey'):
                vcs_details['bitbucketClientKey'] = blueprint_data.get('bitbucketClientKey')
            if blueprint_data.get('vcsConnectionId'):
                vcs_details['vcsConnectionId'] = blueprint_data.get('vcsConnectionId')
            if blueprint_data.get('fileName'):
                vcs_details['fileName'] = blueprint_data.get('fileName')
                
            env_definition['vcs'] = vcs_details
            print(f"✅ Processed '{env_name}' (as single-use with 'vcs' block)", file=sys.stderr)
        else:
            # For regular blueprints, reference the template by name
            env_definition['templateName'] = blueprint_data.get('name')
            print(f"✅ Processed '{env_name}' (using 'templateName')", file=sys.stderr)
            
        # Add optional fields that might be present
        if blueprint_data.get('revision'):
            env_definition['revision'] = blueprint_data.get('revision')
        if workspace_name:
            env_definition['workspace'] = workspace_name
            
        # Add empty needs array for parallel execution (can be customized later)
        env_definition['needs'] = []
            
        # Use environment name as alias (key in the workflow)
        workflow_environments[env_name] = env_definition

    # 5. Assemble and print the final workflow file
    final_workflow = {
        'environments': workflow_environments
    }

    print("\n" + "#" * 50)
    print("## Generated env0.workflow.yml Workflow File")
    print("#" * 50 + "\n")
    print(format_yaml_output(final_workflow))
    
    print("\n" + "#" * 50)
    print("## Instructions")
    print("#" * 50 + "\n")
    print("1. Save the YAML output above into a file named 'env0.workflow.yml'.")
    print("2. Place this 'env0.workflow.yml' file in the same repository as your other sub-environments.")
    print("3. In the env0 UI, create a new 'Workflow Template' pointing to this file.")
    print("4. All sub-environments will run in parallel as configured in the workflow.")
    print("\nNote: Each environment uses its name as the alias, includes template name,")
    print("workspace name, revision, and VCS details as specified.")


if __name__ == "__main__":
    main()