resource "aws_lambda_function" "auth_lambda" {
  filename         = "${path.module}/../app/lambda.zip"
  function_name    = "fiap-auth-lambda"
  handler          = "handler.lambda_handler"
  runtime          = "python3.12"
  role             = aws_iam_role.lambda_role.arn
  source_code_hash = filebase64sha256("${path.module}/../app/lambda.zip")

  timeout     = 10
  memory_size = 128
}
