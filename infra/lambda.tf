resource "aws_lambda_function" "auth_lambda" {
  s3_bucket     = var.lambda_s3_bucket
  s3_key        = var.lambda_s3_key
  function_name = "fiap-auth-lambda"
  handler       = "handler.lambda_handler"
  runtime       = "python3.12"
  role          = aws_iam_role.lambda_role.arn

  timeout     = 10
  memory_size = 128
}
