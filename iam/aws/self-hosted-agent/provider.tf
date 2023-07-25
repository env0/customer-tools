terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.60.0"
    }
    env0 = {
      source  = "env0/env0"
      version = ">= 1.4.1"
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