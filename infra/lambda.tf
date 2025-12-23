# Gera uma chave aleatória e segura para JWT
resource "random_password" "jwt_secret" {
  length  = 64
  special = true
  override_special = "!@#$%^&*()_+-=[]{}|;:,.<>?"
}

resource "aws_security_group" "lambda_sg" {
  name        = "fiap-auth-lambda-sg-${local.environment}"
  description = "Security group para Lambda de autenticacao"
  vpc_id      = data.aws_vpc.main.id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow all outbound traffic"
  }

  tags = {
    Name        = "fiap-auth-lambda-sg-${local.environment}"
    Environment = local.environment
    ManagedBy   = "Terraform"
  }
}


module "lambda-datadog" {
  source  = "DataDog/lambda-datadog/aws"
  version = "4.0.0"

  environment_variables = {
    "DD_API_KEY" : var.datadog_api_key
    "DD_ENV" : local.environment
    "DD_SERVICE" : "fiap-auth-lambda-${local.environment}"
    "DD_SITE": "us5.datadoghq.com"
    "DD_TRACE_ENABLED" : "true"
    "DB_SECRET_NAME" : data.aws_secretsmanager_secret.db_password.name
    "JWT_SECRET_KEY" : random_password.jwt_secret.result
  }

  datadog_extension_layer_version = 86
  datadog_python_layer_version = 119

  s3_bucket     = var.lambda_s3_bucket
  s3_key        = var.lambda_s3_key
  function_name = "fiap-auth-lambda-${local.environment}"
  handler       = "handler.lambda_handler"
  runtime       = "python3.12"
  role          = aws_iam_role.lambda_role.arn

  timeout     = 10
  memory_size = 128

  vpc_config_subnet_ids         = toset(data.aws_subnets.private.ids)
  vpc_config_security_group_ids = toset([aws_security_group.lambda_sg.id])
}
