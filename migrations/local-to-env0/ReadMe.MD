# Migrate local Terraform runs to env0 

## State in Bucket

1. Create a new environment using the VCS option.

2. Configure the 'Settings' as needed.

3. Configure the 'VCS' as needed.

4. Configure the 'Load Variables' as needed.
* Load Variables if required

5. Configure the 'Environmental Details' as needed.
* IMPORTANT - Set the 'Workspace Name' correctly otherwise new resources will be created.
* If the workspace name is unknown, you can find it using 'terraform workspace list'.
* Most commonly the workspace name will be 'default'

## Local state

*Do not create a template or environment before running this procedure.*

1. While the resources are still configured to run locally, run the following commands to ensure no changes are required to the resource(s).

* terraform init
* teraform apply 

2. Once satisfied that the resource(s) are up to date, create a new file in the repo named 'remote-backend.tf'.  In this file copy the following code:

```
terraform {
  backend "remote" {
    hostname = "backend.api.env0.com" 
    organization = "[Org ID].[Project ID]"
    workspaces {
      name = "[workspaceName]"
    }
  }
}
```

3. Run the following command to reconfigure your local terraform code to point towards env0.

* terraform init -migrate-state

This will create an env0 template and env0 environment based on the [workspaceName].

4. Find the newly created template and click 'Settings'.  In the settings, update the following:

* (optional) Terraform version
* VCS selection
* Git Repository
* Branch
* Terraform Folder
* Load Variables & update them as appropriate

Save the changes.

5. Find the environment that was created using the [workspaceName] and redploy.

6. *(optional but recommended) Untick 'Approve plan automatically' and save.*

7. Update any variables as appropriate.

8. Click 'Run'

9. The apply stage should be skipped as no changes should be seen.  

Your environment is now managed by env0 using the env0 remote backend.
