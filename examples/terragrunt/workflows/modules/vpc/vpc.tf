# vpc
resource "aws_vpc" "vpc_1" {
  cidr_block           = "10.10.0.0/16"
  enable_dns_hostnames = true
  tags = {
    Name = "vpc_1"
  }
}