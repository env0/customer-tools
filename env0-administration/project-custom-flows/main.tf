# How to configure project-level custom-flows with the env0 Terraform Provider

# a sample template that you've already configured manually
# we use this template to help populate some fields like the repo and github installation id
data "env0_template" "reference_template" {
  name = "ACME S3 Bucket"
}

# the root project we want to create sub-projects from
data "env0_project" "my_project" {
  #name = "Andrew"
  id = "6932f811-a7d0-4c8e-923c-3f2f285dacc3"
}

resource "env0_custom_flow" "project_custom_flow" {
  for_each = toset(local.projects)

  # due to UI or FrontEnd behavior the name of the Custom Flow MUST match this format project-<project.id>
  name                   = "project-${env0_project.test_projects[each.key].id}"  
  repository             = data.env0_template.reference_template.repository
  github_installation_id = data.env0_template.reference_template.github_installation_id
  path                   = "ec2-opa/env0.yml"
}

resource "env0_custom_flow_assignment" "my_assignment" {
  for_each = toset (local.projects)

  scope_id    = env0_project.test_projects[each.key].id
  template_id = env0_custom_flow.project_custom_flow[each.key].id
}

resource "env0_project" "test_projects" {
  for_each = toset(local.projects)
  name = each.value
  parent_project_id = data.env0_project.my_project.id
}

# locals to help show that you can set the same custom flow for multiple projects
locals {
  projects = ["deva", "devb", "devc"]
}