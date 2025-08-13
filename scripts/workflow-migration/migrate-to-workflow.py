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

def make_api_request(url, method='GET', data=None):
    """Make an API request to env0."""
    headers = {
        'accept': 'application/json',
        'content-type': 'application/json',
        'authorization': create_auth_header()
    }
    
    if data:
        data = json.dumps(data).encode()
    
    request = Request(url, headers=headers, data=data)
    request.get_method = lambda: method
    
    try:
        with urlopen(request) as response:
            response_text = response.read().decode()
            if not response_text.strip():
                return None
            return json.loads(response_text)
    except HTTPError as err:
        print(f"HTTP error ({method} {url}): {err.code} - {err.reason}", file=sys.stderr)
        try:
            error_body = err.read().decode()
            print(f"Error response: {error_body}", file=sys.stderr)
        except:
            pass
        return None
    except URLError as err:
        print(f"Network error: {err.reason}", file=sys.stderr)
        return None
    except json.JSONDecodeError as err:
        print(f"JSON decode error: {err}", file=sys.stderr)
        return None
    except Exception as err:
        print(f"An error occurred: {err}", file=sys.stderr)
        return None

def get_environment(environment_id):
    """Fetch environment details to get organizationId."""
    url = f"{API_BASE_URL}/environments/{environment_id}"
    return make_api_request(url)

def get_environment_variables(environment_id, organization_id):
    """Fetch environment-scope variables for a specific environment."""
    url = f"{API_BASE_URL}/configuration"
    params = f"organizationId={organization_id}&environmentId={environment_id}"
    full_url = f"{url}?{params}"
    return make_api_request(full_url)

def lock_environment(environment_id):
    """Lock an environment using the correct API endpoint."""
    url = f"{API_BASE_URL}/environments/{environment_id}/lock"
    data = {
        "isLocked": True,
        "lockReason": "Migration to workflow"
    }
    return make_api_request(url, method='PUT', data=data)

def archive_environment(environment_id):
    """Archive an environment using the correct API endpoint."""
    url = f"{API_BASE_URL}/environments/{environment_id}"
    data = {
        "isArchived": True
    }
    return make_api_request(url, method='PUT', data=data)

def deploy_workflow(project_id, workflow_template_id, variable_overrides):
    """Deploy a workflow with variable overrides and remote backend."""
    url = f"{API_BASE_URL}/environments"
    
    # Convert variable overrides to configurationChanges format
    configuration_changes = []
    for var in variable_overrides:
        config_change = {
            "type": var.get('type', 0),
            "name": var.get('name'),
            "value": var.get('value'),
            "isSensitive": False
        }
        # Add schema if present
        if var.get('schema'):
            config_change['schema'] = var.get('schema')
        configuration_changes.append(config_change)
    
    data = {
        "deployRequest": {
            "triggerName": "user",
            "blueprintId": workflow_template_id,
            "comment": "Migration to workflow",
            "configurationChanges": configuration_changes,
        },
        "projectId": project_id,
        "name": "Workflow Migration",
        "requiresApproval": False,
        "isRemoteBackend": True
    }
    return make_api_request(url, method='POST', data=data)

def main():
    """Main function to migrate environments to workflow."""
    if not all([ENV0_API_KEY, ENV0_API_SECRET]):
        print("Error: ENV0_API_KEY and ENV0_API_SECRET environment variables must be set.", file=sys.stderr)
        sys.exit(1)

    # Parse command line arguments
    if len(sys.argv) < 4:
        print("Usage: python migrate-to-workflow.py <project_id> <workflow_template_id> <environment_id_1> [environment_id_2] ...", file=sys.stderr)
        sys.exit(1)

    project_id = sys.argv[1]
    workflow_template_id = sys.argv[2]
    environment_ids = sys.argv[3:]

    print(f"Starting migration of {len(environment_ids)} environments to workflow...", file=sys.stderr)
    print(f"Project ID: {project_id}", file=sys.stderr)
    print(f"Workflow Template ID: {workflow_template_id}", file=sys.stderr)
    print(f"Environment IDs: {', '.join(environment_ids)}", file=sys.stderr)

    # Step 1: Get organizationId from the first environment
    print("\n" + "="*50, file=sys.stderr)
    print("STEP 1: Getting organization information", file=sys.stderr)
    print("="*50, file=sys.stderr)
    
    print(f"Fetching organization ID from environment {environment_ids[0]}...", file=sys.stderr)
    first_env = get_environment(environment_ids[0])
    if not first_env:
        print(f"Error: Could not fetch environment {environment_ids[0]} to get organization ID", file=sys.stderr)
        sys.exit(1)
    
    organization_id = first_env.get('organizationId')
    if not organization_id:
        print("Error: Could not get organization ID from environment", file=sys.stderr)
        sys.exit(1)
    
    print(f"Organization ID: {organization_id}", file=sys.stderr)

    # Step 2: Collect environment variables
    print("\n" + "="*50, file=sys.stderr)
    print("STEP 2: Collecting environment variables", file=sys.stderr)
    print("="*50, file=sys.stderr)

    all_variables = {}
    sensitive_variables = []
    
    for env_id in environment_ids:
        print(f"Fetching variables for environment {env_id}...", file=sys.stderr)
        variables = get_environment_variables(env_id, organization_id)
        
        if not variables:
            print(f"Warning: Could not fetch variables for environment {env_id}", file=sys.stderr)
            continue
            
        env_variables = []
        for var in variables:
            if var.get('scope') == 'ENVIRONMENT':  # Only environment-scope variables
                env_variables.append(var)
                if var.get('isSensitive', False):
                    sensitive_variables.append({
                        'environment_id': env_id,
                        'variable_name': var.get('name'),
                        'variable_id': var.get('id')
                    })
        
        all_variables[env_id] = env_variables
        print(f"Found {len(env_variables)} environment-scope variables", file=sys.stderr)

    # Step 2: Print warnings for sensitive variables
    if sensitive_variables:
        print("\n" + "⚠️ " * 20, file=sys.stderr)
        print("WARNING: SENSITIVE ENVIRONMENT-SCOPE VARIABLES DETECTED", file=sys.stderr)
        print("⚠️ " * 20, file=sys.stderr)
        print("\nThe following sensitive variables are scoped to individual environments:", file=sys.stderr)
        print("You should move these to PROJECT SCOPE or WORKFLOW SCOPE before migration:\n", file=sys.stderr)
        
        for var in sensitive_variables:
            print(f"  Environment: {var['environment_id']}", file=sys.stderr)
            print(f"  Variable: {var['variable_name']} (ID: {var['variable_id']})", file=sys.stderr)
            print("", file=sys.stderr)
        
        print("Please move these variables to project or workflow scope and re-run the migration.", file=sys.stderr)
        print("Migration aborted due to sensitive environment-scope variables.", file=sys.stderr)
        sys.exit(1)

    # Step 3: Lock all environments
    print("\n" + "="*50, file=sys.stderr)
    print("STEP 3: Locking environments", file=sys.stderr)
    print("="*50, file=sys.stderr)

    locked_environments = []
    for env_id in environment_ids:
        print(f"Locking environment {env_id}...", file=sys.stderr)
        result = lock_environment(env_id)
        if result:
            locked_environments.append(env_id)
            print(f"✅ Environment {env_id} locked successfully", file=sys.stderr)
        else:
            print(f"❌ Failed to lock environment {env_id}", file=sys.stderr)

    # Step 4: Archive all environments
    print("\n" + "="*50, file=sys.stderr)
    print("STEP 4: Archiving environments", file=sys.stderr)
    print("="*50, file=sys.stderr)

    archived_environments = []
    for env_id in environment_ids:
        print(f"Archiving environment {env_id}...", file=sys.stderr)
        result = archive_environment(env_id)
        if result:
            archived_environments.append(env_id)
            print(f"✅ Environment {env_id} archived successfully", file=sys.stderr)
        else:
            print(f"❌ Failed to archive environment {env_id}", file=sys.stderr)

    # Step 5: Prepare variable overrides
    print("\n" + "="*50, file=sys.stderr)
    print("STEP 5: Preparing workflow deployment", file=sys.stderr)
    print("="*50, file=sys.stderr)

    # Combine all variables from all environments for workflow overrides
    variable_overrides = []
    for env_id, variables in all_variables.items():
        for var in variables:
            # Convert environment variable to workflow variable override
            variable_override = {
                "name": var.get('name'),
                "value": var.get('value'),
                "isSensitive": var.get('isSensitive', False),
                "type": var.get('type', 0),
                "scope": "WORKFLOW"  # Convert to workflow scope
            }
            
            # Add schema if present
            if var.get('schema'):
                variable_override['schema'] = var.get('schema')
                
            variable_overrides.append(variable_override)

    print(f"Prepared {len(variable_overrides)} variable overrides for workflow", file=sys.stderr)

    # Step 6: Deploy workflow
    print("\n" + "="*50, file=sys.stderr)
    print("STEP 6: Deploying workflow", file=sys.stderr)
    print("="*50, file=sys.stderr)

    print("Deploying workflow with remote backend and variable overrides...", file=sys.stderr)
    workflow_result = deploy_workflow(project_id, workflow_template_id, variable_overrides)
    
    if workflow_result:
        workflow_id = workflow_result.get('id', 'unknown')
        print(f"✅ Workflow deployed successfully! Workflow ID: {workflow_id}", file=sys.stderr)
    else:
        print("❌ Failed to deploy workflow", file=sys.stderr)
        sys.exit(1)

    # Step 7: Print summary
    print("\n" + "🎉" * 20, file=sys.stderr)
    print("MIGRATION COMPLETED SUCCESSFULLY!", file=sys.stderr)
    print("🎉" * 20, file=sys.stderr)
    
    print(f"\nSummary:", file=sys.stderr)
    print(f"  • Environments processed: {len(environment_ids)}", file=sys.stderr)
    print(f"  • Environments locked: {len(locked_environments)}", file=sys.stderr)
    print(f"  • Environments archived: {len(archived_environments)}", file=sys.stderr)
    print(f"  • Variables migrated: {len(variable_overrides)}", file=sys.stderr)
    print(f"  • Workflow ID: {workflow_result.get('id', 'unknown')}", file=sys.stderr)
    print(f"  • Remote backend: Enabled", file=sys.stderr)
    
    print(f"\nNext steps:", file=sys.stderr)
    print(f"  1. Monitor the workflow deployment in the env0 UI", file=sys.stderr)
    print(f"  2. Verify that all environments are running correctly in the workflow", file=sys.stderr)
    print(f"  3. Update any automation or scripts to reference the new workflow", file=sys.stderr)


if __name__ == "__main__":
    main()
