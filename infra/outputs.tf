output "api_gateway_id" {
  value       = data.aws_apigatewayv2_api.oficina_api.id
  description = "ID do API Gateway HTTP API v2"
}

output "auth_route_id" {
  value       = aws_apigatewayv2_route.auth_cpf.id
  description = "ID da rota POST /auth/cpf"
}

output "lambda_function_name" {
  value       = module.lambda-datadog.function_name
  description = "Nome da função Lambda de autenticação"
}
