resource "aws_iam_policy" "assume_role_policy" {
  name        = "assume_role_policy"
  description = "Ability to assume other role"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "sts:AssumeRole"
      ],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "attach_assume_role" {
  role       = module.eks.worker_iam_role_name   # this won't work right now, need to modify module to output role name
  policy_arn = aws_iam_policy.assume_role_policy.arn

}
