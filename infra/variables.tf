variable "lambda_s3_bucket" {
  description = "S3 bucket where the lambda package is uploaded"
  type        = string
}

variable "lambda_s3_key" {
  description = "S3 key (path) for the lambda package"
  type        = string
}

variable "datadog_api_key" {
  description = "Datadog API key (prefer to pass via environment or secret)"
  type        = string
  default     = ""
}

variable "aws_region" {
  description = "AWS region for the provider and resources"
  type        = string
  default     = "us-east-2"
}
