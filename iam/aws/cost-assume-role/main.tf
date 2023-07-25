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
  default     = "env0-cost-role"
  description = "role name used in AWS"
}

### RESOURCES

resource "aws_iam_role" "env0_cost_role" {
  name = var.assume_role_name

  max_session_duration = 18000

  inline_policy {
    name = "env0-cost-policy"
    policy = jsonencode({
      "Version" : "2012-10-17",
      "Statement" : [
        {
          "Effect" : "Allow",
          "Action" : "ce:GetCostAndUsage",
          "Resource" : "*"
        }
      ]
    })
  }

  # see: https://docs.env0.com/docs/aws-costs#add-credentials-to-your-organization
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
  override_special = "=,.@:/-"
}

resource "env0_aws_cost_credentials" "credentials" {
  name        = aws_iam_role.env0_cost_role.arn
  arn         = aws_iam_role.env0_cost_role.arn
  external_id = random_string.externalid.result
}

output "externalid" {
  value     = random_string.externalid.result
  sensitive = true
}