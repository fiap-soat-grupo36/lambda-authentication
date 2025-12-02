resource "aws_s3_bucket" "lambda_code" {
  bucket_prefix = "fiap-lambda-code-"
  force_destroy = true
}

resource "aws_s3_bucket_acl" "lambda_code_acl" {
  bucket = aws_s3_bucket.lambda_code.id
  acl    = "private"
}

resource "aws_s3_bucket_public_access_block" "block" {
  bucket = aws_s3_bucket.lambda_code.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_versioning" "lambda_code_versioning" {
  bucket = aws_s3_bucket.lambda_code.id

  versioning_configuration {
    status = "Enabled"
  }
}
