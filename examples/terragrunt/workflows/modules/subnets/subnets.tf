# subnet(s)
resource "aws_subnet" "subnet_1" {
  vpc_id                  = data.aws_vpc.vpc_1.id
  cidr_block              = "10.10.10.0/24"
  availability_zone       = "eu-north-1a"
  map_public_ip_on_launch = false
  tags = {
    Name = "subnet_1"
  }
}

data "aws_vpc" "vpc_1" {
  filter {
    name   = "tag:Name"
    values = ["vpc_1"]
  }
}