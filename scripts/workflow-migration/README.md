## Please be aware of a few prerequisites and changes in behavior
1) Single Project: The scripts assume that all environments you intend to migrate reside within the same project.
2) Sensitive Variables: The process assumes that there are no sensitive variables defined specifically for individual environments. Variables defined at the project level are fully supported.
3) Remote Backend: All environments must be configured to use a remote backend.
4) PR Plan Behavior: Please note that PR Plans operate differently in a workflow context. A plan is run workflow-wide, which means a separate plan comment will be posted on your pull request for each sub-environment in the workflow. For instance, a workflow with five sub-environments will generate five comments on a relevant push.
5) Post Migration: No deployments that occured before the migration will be available.

## We have 3 scripts
1) Workflow File Generation (build-workflow-file.py): The first script assists by automatically generating the necessary workflow file based on your existing environments.
2) Environment Migration (migrate-to-workflow.py): After you create an env0 template for the new workflow, a second script handles the migration. It will automatically lock and archive the old individual environments and then deploy the new workflow with the required configurations.
3) Rollback (rollback-workflow.py): In case of needing to rollback to the old configuration, this script can be used to lock and archive the workflow, and reactivate the old individual environments

## Running the scripts
1) Create an Admin API Key in env0. Set environment variables locally based on that API key - ENV0_API_KEY and ENV0_API_SECRET
2) Run python build-workflow-file.py <environment_id_1> <environment_id_2> ... to generate a YAML text for the workflow file. This action is non-destructive and can be run multiple times
3) Follow the instructions in the output of the script: Create the env0.workflow.yml somewhere in your GitHub (it should be same repository as the sub-environments), create a workflow template.
4) Run python migrate-to-workflow.py <project_id> <workflow_template_id> <environment_id_1> <environment_id_2> ... to start locking and archiving the old environments, and migrate them to a workflow. The script will validate early and fail if there are any secret variables defined specifically for one of these environments
5) If at any point you’d like to roll back, run python3 rollback-workflow.py <workflow_environment_id> <original_env_id_1> <original_env_id_2> ...
