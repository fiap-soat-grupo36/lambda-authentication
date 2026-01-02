
# Data Source - API Gateway existente
data "aws_api_gateway_rest_api" "oficina_api" {
  name = "oficina-api"
}

# Recursos (/auth/login)

resource "aws_api_gateway_resource" "auth" {
  rest_api_id = data.aws_api_gateway_rest_api.oficina_api.id
  parent_id   = data.aws_api_gateway_rest_api.oficina_api.root_resource_id
  path_part   = "auth"
}

resource "aws_api_gateway_resource" "login" {
  rest_api_id = data.aws_api_gateway_rest_api.oficina_api.id
  parent_id   = aws_api_gateway_resource.auth.id
  path_part   = "login"
}


# POST

resource "aws_api_gateway_method" "login_post" {
  rest_api_id   = data.aws_api_gateway_rest_api.oficina_api.id
  resource_id   = aws_api_gateway_resource.login.id
  http_method   = "POST"
  authorization = "NONE"
}


# Integração Lambda

resource "aws_api_gateway_integration" "login_lambda" {
  rest_api_id = data.aws_api_gateway_rest_api.oficina_api.id
  resource_id = aws_api_gateway_resource.login.id
  http_method = aws_api_gateway_method.login_post.http_method

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = module.lambda-datadog.invoke_arn
}


# Permissão Lambda

resource "aws_lambda_permission" "apigw_invoke_auth" {
  statement_id  = "AllowAPIGatewayInvokeAuth"
  action        = "lambda:InvokeFunction"
  function_name = module.lambda-datadog.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${data.aws_api_gateway_rest_api.oficina_api.execution_arn}/*/*"
}