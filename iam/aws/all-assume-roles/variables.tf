### VARIABLES

variable "region" {
  type    = string
  default = "us-east-1"
}

variable "cost_assume_role_name" {
  type        = string
  default     = "env0-cost-role"
  description = "name used for both env0 and AWS"
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

variable "isRunningInEnv0" {
  type        = bool
  default     = false
  description = "is this code being executed within env0?"
}

variable "org_id" {
  type        = string
  default     = ""
  description = "supply this value if you're not running in env0"
}