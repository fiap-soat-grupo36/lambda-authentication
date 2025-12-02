locals {
  datadog_layers = concat(
    var.datadog_layer_arn != "" ? [var.datadog_layer_arn] : [],
    var.datadog_extension_arn != "" ? [var.datadog_extension_arn] : []
  )
}

resource "aws_lambda_function" "auth_lambda" {
  s3_bucket     = var.lambda_s3_bucket
  s3_key        = var.lambda_s3_key
  function_name = "fiap-auth-lambda"
  handler       = "handler.lambda_handler"
  runtime       = "python3.12"
  role          = aws_iam_role.lambda_role.arn

  # Attach Datadog layers if provided
  layers = local.datadog_layers

  environment {
    variables = merge(
      {
        # Basic metadata
        DD_ENV   = var.environment
        DD_SERVICE = "fiap-auth-lambda"
        DD_TRACE_ENABLED = "true"
      },
      var.datadog_api_key != "" ? { DD_API_KEY = var.datadog_api_key } : {}
    )
  }

  timeout     = 10
  memory_size = 128
}
