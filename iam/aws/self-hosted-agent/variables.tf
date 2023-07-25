variable "role_name" {
  type = string
  default = "env0-deployer-role"
  description = "name of the role for IaC deployments"
}

variable "trust_role_arn" {
  type = string
  description = "either node role or pod role arn"
}

variable "managed_policy_arns" {
  type = list
  default = ["arn:aws:iam::aws:policy/PowerUserAccess"] 
  description = "managed policies assigned to role"
}