# TFC to env0 Migration - TFC Local State

## Prerequisite

> The following applications should be installed on your local machine:

>> Terraform
>> sed
>> curl

> Set TFC "Apply Method" to "Manual Apply".

> Backend should be defined as Cloud and not Remote.

> Login to TFC: "terraform login"

> Login to env0: "terraform login backend.api.env0.com"

## Procedure

> Copy or clone the "inputs.txt" and "tfc2env0.sh" files to directory which requires migrating.

> Fill in the "inputs.txt" file with relevant data.

> Run the "tfc2env0.sh" script.

> Update the env0 template with correct VCS configuration.

> Trigger a redploy of the newly created environment.