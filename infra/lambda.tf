module "lambda-datadog" {
  source  = "DataDog/lambda-datadog/aws"
  version = "4.0.0"

  environment_variables = {
    "DD_API_KEY" : var.datadog_api_key
    "DD_ENV" : var.environment
    "DD_SERVICE" : "fiap-auth-lambda"
    "DD_SITE": "us5.datadoghq.com"
    "DD_TRACE_ENABLED" : "true"
  }

  datadog_extension_layer_version = 86
  datadog_python_layer_version = 119

  s3_bucket     = var.lambda_s3_bucket
  s3_key        = var.lambda_s3_key
  function_name = "fiap-auth-lambda-${var.environment}"
  handler       = "handler.lambda_handler"
  runtime       = "python3.12"
  role          = aws_iam_role.lambda_role.arn

  timeout     = 10
  memory_size = 128
}
