# env0 Workflow exmaple using Terragrunt templates.

This example will build out a AWS VPC and Subnet in 2 stages.  The VPC folder contains the code to create the VPC and the subnet folder contains the code to provision a single subnet.

Typically when using Terragrunt, dependancies need to be created.  However with env0 you can run both sets of code in a specific order.

The way this is accomplished is by using an env0.workflow.yml file which can be found in the root directory.

## How to use this code.

