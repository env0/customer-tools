# Uses public module.

terraform {
  source = "git::"
}

# Gathers configuration from parent terragrunt files.

include {
  path = find_in_parent_folders()
}