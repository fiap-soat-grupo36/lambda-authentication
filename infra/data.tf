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

data "aws_iam_policy_document" "lambda_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

data "aws_rds_cluster" "cluster" {
  cluster_identifier = "fiap-rds"
}

data "aws_secretsmanager_secret" "db_password" {
  arn = data.aws_rds_cluster.cluster.master_user_secret[0].secret_arn
}

data "aws_secretsmanager_secret_version" "db_password" {
  secret_id = data.aws_secretsmanager_secret.db_password.id
}

data "aws_security_group" "database" {
  filter {
    name   = "tag:Name"
    values = ["fiap-rds-sg"]
  }

  vpc_id = data.aws_vpc.main.id
}

data "aws_secretsmanager_secret" "jwt_secret" {
  name = var.jwt_secret_name
}

data "aws_secretsmanager_secret_version" "jwt_secret" {
  secret_id = data.aws_secretsmanager_secret.jwt_secret.id
}