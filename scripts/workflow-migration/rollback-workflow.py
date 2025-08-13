#!/usr/bin/env python3
"""
env0 Workflow Rollback Script

This script rolls back a workflow migration by:
1. Locking and archiving the workflow environment
2. Unlocking and unarchiving the original environments

Usage: python3 rollback-workflow.py <workflow_environment_id> <original_env_id_1> [original_env_id_2] ...

Requires environment variables:
- ENV0_API_KEY: Your env0 API key
- ENV0_API_SECRET: Your env0 API secret
"""

import sys
import os
import json
import urllib.request
import urllib.parse
import urllib.error
import base64

# --- Configuration ---
ENV0_API_KEY = os.getenv('ENV0_API_KEY')
ENV0_API_SECRET = os.getenv('ENV0_API_SECRET')
API_BASE_URL = 'https://api.env0.com'

def make_api_request(url, method='GET', data=None):
    """Make an authenticated API request to env0."""
    try:
        # Create authentication header
        credentials = f"{ENV0_API_KEY}:{ENV0_API_SECRET}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        
        headers = {
            'Authorization': f'Basic {encoded_credentials}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        # Prepare request data
        request_data = None
        if data is not None:
            request_data = json.dumps(data).encode('utf-8')
        
        # Create request
        req = urllib.request.Request(url, data=request_data, headers=headers, method=method)
        
        # Make request
        with urllib.request.urlopen(req) as response:
            response_data = response.read().decode('utf-8')
            if response_data:
                return json.loads(response_data)
            return {}
            
    except urllib.error.HTTPError as err:
        error_body = err.read().decode('utf-8')
        print(f"HTTP Error {err.code}: {error_body}", file=sys.stderr)
        return None
    except urllib.error.URLError as err:
        print(f"URL Error: {err}", file=sys.stderr)
        return None
    except Exception as err:
        print(f"An error occurred: {err}", file=sys.stderr)
        return None

def unlock_environment(environment_id):
    """Unlock an environment using the correct API endpoint."""
    url = f"{API_BASE_URL}/environments/{environment_id}"
    data = {
        "isLocked": False
    }
    return make_api_request(url, method='PUT', data=data)

def lock_environment(workflow_environment_id):
    """Lock an environment using the correct API endpoint."""
    url = f"{API_BASE_URL}/environments/{workflow_environment_id}/lock"
    data = {
        "isLocked": True,
        "lockReason": "Workflow rollback"
    }
    return make_api_request(url, method='PUT', data=data)

def archive_environment(workflow_environment_id):
    """Archive an environment using the correct API endpoint."""
    url = f"{API_BASE_URL}/environments/{workflow_environment_id}"
    data = {
        "isArchived": True
    }
    return make_api_request(url, method='PUT', data=data)

def unarchive_environment(environment_id):
    """Unarchive an environment using the correct API endpoint."""
    url = f"{API_BASE_URL}/environments/{environment_id}"
    data = {
        "isArchived": False
    }
    return make_api_request(url, method='PUT', data=data)

def main():
    if not all([ENV0_API_KEY, ENV0_API_SECRET]):
        print("Error: ENV0_API_KEY and ENV0_API_SECRET environment variables must be set.", file=sys.stderr)
        sys.exit(1)

    if len(sys.argv) < 3:
        print("Usage: python3 rollback-workflow.py <workflow_environment_id> <original_env_id_1> [original_env_id_2] ...", file=sys.stderr)
        sys.exit(1)

    workflow_environment_id = sys.argv[1]
    original_environment_ids = sys.argv[2:]

    print("=" * 60, file=sys.stderr)
    print("ENV0 WORKFLOW ROLLBACK", file=sys.stderr)
    print("=" * 60, file=sys.stderr)
    print(f"Workflow Environment ID: {workflow_environment_id}", file=sys.stderr)
    print(f"Original Environment IDs: {', '.join(original_environment_ids)}", file=sys.stderr)

    # Step 1: Lock and archive the workflow environment
    print("\n" + "="*50, file=sys.stderr)
    print("STEP 1: Locking and archiving workflow environment", file=sys.stderr)
    print("="*50, file=sys.stderr)
    
    print(f"Locking workflow environment {workflow_environment_id}...", file=sys.stderr)
    lock_result = lock_environment(workflow_environment_id)
    if not lock_result:
        print(f"Error: Failed to lock workflow environment {workflow_environment_id}", file=sys.stderr)
        sys.exit(1)
    print("✅ Workflow environment locked successfully", file=sys.stderr)
    
    print(f"Archiving workflow environment {workflow_environment_id}...", file=sys.stderr)
    archive_result = archive_environment(workflow_environment_id)
    if not archive_result:
        print(f"Error: Failed to archive workflow environment {workflow_environment_id}", file=sys.stderr)
        sys.exit(1)
    print("✅ Workflow environment archived successfully", file=sys.stderr)

    # Step 2: Unarchive and unlock original environments
    print("\n" + "="*50, file=sys.stderr)
    print("STEP 2: Unarchiving and unlocking original environments", file=sys.stderr)
    print("="*50, file=sys.stderr)

    successful_rollbacks = []
    failed_rollbacks = []

    for env_id in original_environment_ids:
        print(f"\nProcessing environment {env_id}...", file=sys.stderr)
        
        # Unarchive first
        print(f"  Unarchiving environment {env_id}...", file=sys.stderr)
        unarchive_result = unarchive_environment(env_id)
        if not unarchive_result:
            print(f"  ❌ Failed to unarchive environment {env_id}", file=sys.stderr)
            failed_rollbacks.append(env_id)
            continue
        print(f"  ✅ Environment {env_id} unarchived successfully", file=sys.stderr)
        
        # Then unlock
        print(f"  Unlocking environment {env_id}...", file=sys.stderr)
        unlock_result = unlock_environment(env_id)
        if not unlock_result:
            print(f"  ❌ Failed to unlock environment {env_id}", file=sys.stderr)
            failed_rollbacks.append(env_id)
            continue
        print(f"  ✅ Environment {env_id} unlocked successfully", file=sys.stderr)
        
        successful_rollbacks.append(env_id)

    # Step 3: Print summary
    print("\n" + "="*50, file=sys.stderr)
    print("ROLLBACK SUMMARY", file=sys.stderr)
    print("="*50, file=sys.stderr)
    
    print(f"✅ Workflow environment {workflow_environment_id} locked and archived", file=sys.stderr)
    print(f"✅ Successfully rolled back {len(successful_rollbacks)} environments", file=sys.stderr)
    
    if successful_rollbacks:
        print("\nSuccessfully rolled back environments:", file=sys.stderr)
        for env_id in successful_rollbacks:
            print(f"  - {env_id}", file=sys.stderr)
    
    if failed_rollbacks:
        print(f"\n❌ Failed to rollback {len(failed_rollbacks)} environments:", file=sys.stderr)
        for env_id in failed_rollbacks:
            print(f"  - {env_id}", file=sys.stderr)
        print("\nPlease manually check and fix these environments.", file=sys.stderr)
    
    print("\n" + "="*50, file=sys.stderr)
    print("ROLLBACK COMPLETE", file=sys.stderr)
    print("="*50, file=sys.stderr)
    
    if failed_rollbacks:
        sys.exit(1)
    else:
        print("All environments successfully rolled back!", file=sys.stderr)

if __name__ == "__main__":
    main()
