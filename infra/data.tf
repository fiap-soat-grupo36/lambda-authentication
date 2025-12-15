data "aws_vpc" "main" {
  filter {
    name   = "tag:Name"
    values = ["fiap-oficina-mecanica"]
  }
}

data "aws_subnets" "private" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.main.id]
  }

  filter {
    name   = "tag:Name"
    values = ["*private*"]
  }
}