##################################################################
################### INTEGRAÇÃO HTTP API v2 #######################
##################################################################

# Usa o API Gateway ID do remote state do infra-kubernetes
locals {
  api_gateway_id = data.terraform_remote_state.infra.outputs.api_gateway_id
}

# Data Source - HTTP API v2 existente (criado pelo infra-kubernetes)
data "aws_apigatewayv2_api" "oficina_api" {
  api_id = local.api_gateway_id
}

# Integração Lambda com HTTP API v2
resource "aws_apigatewayv2_integration" "auth_lambda" {
  api_id                 = data.aws_apigatewayv2_api.oficina_api.id
  integration_type       = "AWS_PROXY"
  integration_uri        = module.lambda-datadog.invoke_arn
  integration_method     = "POST"
  payload_format_version = "2.0"
  timeout_milliseconds   = 10000
}

# Rota POST /auth/cpf -> Lambda (autenticação de clientes via CPF)
# Nota: /auth/login continua disponível no auth-service para login com username/password
resource "aws_apigatewayv2_route" "auth_cpf" {
  api_id    = data.aws_apigatewayv2_api.oficina_api.id
  route_key = "POST /auth/cpf"
  target    = "integrations/${aws_apigatewayv2_integration.auth_lambda.id}"
}

# Permissão para API Gateway invocar a Lambda
resource "aws_lambda_permission" "apigw_invoke_auth" {
  statement_id  = "AllowAPIGatewayInvokeAuth"
  action        = "lambda:InvokeFunction"
  function_name = module.lambda-datadog.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${data.aws_apigatewayv2_api.oficina_api.execution_arn}/*/*"
}
