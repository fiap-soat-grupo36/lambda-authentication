output "auth_resource_id" {
  value       = aws_api_gateway_resource.auth.id
  description = "ID do recurso /auth no API Gateway"
}

output "login_resource_id" {
  value       = aws_api_gateway_resource.login.id
  description = "ID do recurso /auth/login no API Gateway"
}

output "oficina_api_id" {
  value       = data.aws_api_gateway_rest_api.oficina_api.id
  description = "ID do API Gateway oficina-api"
}

output "oficina_api_root_resource_id" {
  value       = data.aws_api_gateway_rest_api.oficina_api.root_resource_id
  description = "Root resource ID do API Gateway oficina-api"
}

output "oficina_api_execution_arn" {
  value       = data.aws_api_gateway_rest_api.oficina_api.execution_arn
  description = "Execution ARN do API Gateway oficina-api"
}
