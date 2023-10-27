# TFC to env0 Migration - TFC Local State

The manual workflow can be found in the env0 documentation.
https://docs.env0.com/docs/state-migration

## Prerequisite

The following applications should be installed on your local machine:

- Terraform
- sed
- curl

Find the workspace you are looking to migrate and set TFC "Execution Mode" to "Custom" & "Local".

The backend should be defined as Remote and not Cloud.

```
backend "remote" {  
  organization = "example_corp"
  workspaces {
    name = "my-prod-resource"
	}
}
```

## Procedure - Migrate run while leaving state in TFC

Copy or clone the files to a location where you are able to execute the scripts.

Fill in the "inputs.txt" file with relevant data.

Run the "tfc2env0-migrateRun.sh" script to migrate the run logic to env0, leaving the state in TFC.

Once you are happy with the env0 platform, migrate the state by executing the "tfc2env0-migrateState.sh" script.