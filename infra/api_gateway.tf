
# API Gateway

resource "aws_api_gateway_rest_api" "auth_api" {
  name        = "oficina-auth-api"
  description = "API de autenticação de clientes via CPF"
}


# Recursos (/auth/login)

resource "aws_api_gateway_resource" "auth" {
  rest_api_id = aws_api_gateway_rest_api.auth_api.id
  parent_id   = aws_api_gateway_rest_api.auth_api.root_resource_id
  path_part   = "auth"
}

resource "aws_api_gateway_resource" "login" {
  rest_api_id = aws_api_gateway_rest_api.auth_api.id
  parent_id   = aws_api_gateway_resource.auth.id
  path_part   = "login"
}


# POST

resource "aws_api_gateway_method" "login_post" {
  rest_api_id   = aws_api_gateway_rest_api.auth_api.id
  resource_id   = aws_api_gateway_resource.login.id
  http_method   = "POST"
  authorization = "NONE"
}


# Integração Lambda

resource "aws_api_gateway_integration" "login_lambda" {
  rest_api_id = aws_api_gateway_rest_api.auth_api.id
  resource_id = aws_api_gateway_resource.login.id
  http_method = aws_api_gateway_method.login_post.http_method

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function
}


# Permissão Lambda

resource "aws_lambda_permission" "apigw_invoke_auth" {
  statement_id  = "AllowAPIGatewayInvokeAuth"
  action        = "lambda:InvokeFunction"
  function_name = ""
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_api_gateway_rest_api.auth_api.execution_arn}/*/*"
}


# Deploy e Stage

resource "aws_api_gateway_deployment" "auth_api_deploy" {
  rest_api_id = aws_api_gateway_rest_api.auth_api.id

  depends_on = [
    aws_api_gateway_integration.login_lambda
  ]
}

resource "aws_api_gateway_stage" "dev" {
  deployment_id = aws_api_gateway_deployment.auth_api_deploy.id
  rest_api_id   = aws_api_gateway_rest_api.auth_api.id
  stage_name    = "dev"
}

# Output

output "auth_api_invoke_url" {
  value = "https://${aws_api_gateway_rest_api.auth_api.id}.execute-api.${var.aws_region}.amazonaws.com/dev/auth/login"
}
