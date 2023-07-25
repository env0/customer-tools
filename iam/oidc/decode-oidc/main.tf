terraform {
  backend "remote" {
    hostname     = "backend.api.env0.com"
    organization = "bde19c6d-d0dc-4b11-a951-8f43fe49db92"

    workspaces {
      name = "env023ad94"
    }
  }
}

resource "null_resource" "null" {
  count = var.num_resources
}

variable "num_resources" {
  type    = number
  default = 2
}
