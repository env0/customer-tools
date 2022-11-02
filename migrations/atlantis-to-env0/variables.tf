variable "project" {
  description = "The project ID"
  type = string
  default = "terraformprojects-365816"
}

variable "region" {
  description = "Cloud Region"
  type = string
  default = "us-central1"
}

variable "zone" {
  description = "Zone in the Cloud Region"
  type = string
  default = "us-central1-a"
}

variable "instance_name" {
  description = "Name of the VM instance"
  type = string
  default = "atlantis-vm-dev"
}

