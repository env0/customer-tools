# the standard aws role for TF to assume to deploy TF resources
# this is assumed by env0 through the node or pod role
# typically configured in the UI

data "env0_organization" "my_organization" {}

data "aws_iam_policy_document" "assume_role" {
  effect = "Allow"

  principals {
    type        = "AWS"
    identifiers = [var.trust_role_arn]
  }

  actions = ["sts:AssumeRole"]

  condition {
      test     = "StringEquals"
      variable = "sts:ExternalId"
      values = [ data.env0_organization.my_organization.id ]
    }
}

resource "aws_iam_role" "role" {
  name               = var.role_name
  managed_policy_arns = var.managed_policy_arns
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

