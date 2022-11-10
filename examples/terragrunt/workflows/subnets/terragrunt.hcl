# Uses public module.

terraform {
  source = "git::https://github.com/env0/customer-tools.git//examples/terragrunt/workflows/modules/subnets"
}

# Gathers configuration from parent terragrunt files.

include {
  path = find_in_parent_folders()
}