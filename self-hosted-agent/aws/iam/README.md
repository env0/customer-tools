# Self Hosted Agent IAM Roles and Permissions

This example provides some Terraform examples to include in your setup for configuring IAM

## Summary

The self-hosted agent uses by default the EKS Node role.  For example, if your EKS nodes are built off EC2 instances, then this will be the EC2 Instance Role.  We will refer to this role as the **node role**.

Typically, in a production environment, the **node role** will not be used to deploy Terraform directly.  And, the Self-hosted agent is installed on a shared services cluster.  The infrastructure being provisioned by env0, will create and maintain resources in various other AWS accounts - **target accounts**.

We will show a common architecture that will allow Terraform to assume a **target account role** through the Self-hosted agent. 

## Common Architecture

* EKS Cluster is installed in a "Shared Services" AWS account (id: 444555666).
* **Target Account - Dev** is a development AWS account (id: 111222333).
* **Target Account - Prod** is a production AWS account (id: 777888999).

* **node role** (arn:aws:444555666::ec2-instance-role) is also the role used by the self-hosted agent. (for IRSA, or IAM through Kubernetes Service Account, see section on IRSA below. 
* **target account role - dev** (arn:aws:111222333::env0-deployer-role) - also referred to as the deployer role, has the necessary permissions to execute your Terraform code in Dev (typically a PowerUser level role since Terraform is provisioning all of your infrastructure).
* **target account role - prod** (arn:aws:777888999::env0-deployer-role) - also referred to as the deployer role, has the necessary permissions to execute your Terraform code in Dev (typically a PowerUser level role).

## IRSA - IAM role using Kubernetes Service Account

