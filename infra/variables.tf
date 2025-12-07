variable "lambda_s3_bucket" {
  description = "S3 bucket where the lambda package is uploaded"
  type        = string
}

variable "lambda_s3_key" {
  description = "S3 key (path) for the lambda package"
  type        = string
}

# Datadog settings (optional)
variable "datadog_enabled" {
  description = "Enable Datadog instrumentation for the Lambda"
  type        = bool
  default     = false
}

variable "datadog_layer_arn" {
  description = "ARN of the Datadog Python library layer (optional)"
  type        = string
  default     = ""
}

variable "datadog_extension_arn" {
  description = "ARN of the Datadog Lambda Extension layer (optional)"
  type        = string
  default     = ""
}

variable "datadog_api_key" {
  description = "Datadog API key (prefer to pass via environment or secret)"
  type        = string
  default     = ""
}

variable "environment" {
  description = "Deployment environment name (used for DD_ENV)"
  type        = string
  default     = "production"
}

variable "aws_region" {
  description = "AWS region for the provider and resources"
  type        = string
  default     = "us-east-2"
}
