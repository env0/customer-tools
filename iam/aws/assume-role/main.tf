terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.36.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.4.3"
    }
    env0 = {
      source  = "env0/env0"
      version = ">= 1.2.7"
    }
  }
}

provider "env0" {
  # env0 Provider expects to find the environment variables defined.
  # to create an API key see:  https://docs.env0.com/docs/api-keys
  # ENV0_API_KEY    
  # ENV0_API_SECRET
}

provider "aws" {
  region = var.region
}

### VARIABLES

variable "region" {
  type    = string
  default = "us-east-1"
}

variable "assume_role_name" {
  type        = string
  default     = "env0-deployer-role"
  description = "name used for both env0 and AWS"
}

variable "managed_policy_arns" {
  type        = list(string)
  default     = ["arn:aws:iam::aws:policy/AdministratorAccess", ]
  description = "list of policy arns to assign to env0's deployer"
}

### RESOURCES 

resource "aws_iam_role" "env0_deployer_role" {
  name = var.assume_role_name

  max_session_duration = 18000 # env0 requirement, 5 hours for SaaS

  # Change to your policy
  managed_policy_arns = var.managed_policy_arns

  # 913128560466 is env0's AWS Account ID
  # see: https://docs.env0.com/docs/connect-your-cloud-account#using-aws-assume-role
  assume_role_policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Effect" : "Allow",
        "Principal" : {
          "AWS" : "arn:aws:iam::913128560467:root"
        },
        "Action" : "sts:AssumeRole",
        "Condition" : {
          "StringEquals" : {
            "sts:ExternalId" : "${random_string.externalid.result}"
          }
        }
      }
    ]
  })

  tags = {
    note = "Created through env0 Bootstrap"
  }
}

resource "random_string" "externalid" {
  length           = 32
  special          = true
  override_special = "=,.@:/-" # allowable characters defined here: https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html
}

resource "env0_aws_credentials" "credentials" {
  name        = aws_iam_role.env0_deployer_role.arn #easier to track in the UI which role exactly is being used
  arn         = aws_iam_role.env0_deployer_role.arn
  external_id = random_string.externalid.result
}

### OUTPUTS

output "externalid" {
  value     = random_string.externalid.result
  sensitive = true
}