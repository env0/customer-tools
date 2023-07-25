# Generates provider code

generate "aws_provider" {
  path      = "aws_provider.tf"
  if_exists = "overwrite_terragrunt"
  contents  = <<EOF
 terraform {
   required_providers {
     aws = {
       source = "hashicorp/aws"
     }
   }
 }

 provider "aws" {
   region     = "eu-north-1"
 }
EOF
}

