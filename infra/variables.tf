variable "lambda_s3_bucket" {
  description = "S3 bucket where the lambda package is uploaded"
  type        = string
}

variable "lambda_s3_key" {
  description = "S3 key (path) for the lambda package"
  type        = string
}
