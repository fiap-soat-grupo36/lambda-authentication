output "lambda_function_name" {
  value = aws_lambda_function.auth_lambda.function_name
}

output "lambda_bucket_name" {
  value = aws_s3_bucket.lambda_code.bucket
}
