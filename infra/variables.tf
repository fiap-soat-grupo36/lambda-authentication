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

variable "db_secret_name" {
  description = "Secrets Manager secret name or ARN for DB credentials (populate in CI or a secure tfvars)"
  type        = string
  sensitive   = true
  default     = ""
}

variable "db_name" {
  description = "Nome do database no RDS"
  type        = string
  default     = "oficina"
}