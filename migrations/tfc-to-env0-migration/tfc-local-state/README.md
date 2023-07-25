# TFC to env0 Migration - TFC Local State

## Prerequisite

The following applications should be installed on your local machine:

- Terraform
- sed
- curl

Set TFC "Apply Method" to "Manual Apply".

Backend should be defined as Remote and not Cloud.

Login to TFC: "terraform login"

Login to env0: "terraform login backend.api.env0.com"

Remove the terraform directory and terraform.lock file from your local directory.

## Procedure

Copy or clone the "inputs.txt" and "tfc2env0.sh" files to directory which requires migrating.

Fill in the "inputs.txt" file with relevant data.

Run the "tfc2env0.sh" script.

Update the env0 template with correct VCS and variable configuration as prompted by the script.

Trigger a redploy of the newly created environment as prompted by the script.
Be aware auto-approval is turned on for this migrated environment.  We recommend disabling this on first redeploy.