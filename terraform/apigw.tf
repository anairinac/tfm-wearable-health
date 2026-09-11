resource "aws_apigatewayv2_api" "tfm-wearable-health-api" {
    name          = "${var.project_name}-api"
    protocol_type = "HTTP"
}

resource "aws_apigatewayv2_integration" "tfm-wearable-health-integration" {
    api_id             = aws_apigatewayv2_api.tfm-wearable-health-api.id
    integration_type   = "AWS_PROXY"
    integration_uri    = aws_lambda_function.tfm-wearable-health-lambda.arn
    payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "tfm-wearable-health-route" {
    api_id    = aws_apigatewayv2_api.tfm-wearable-health-api.id
    route_key = "POST /predict"
    target    = "integrations/${aws_apigatewayv2_integration.tfm-wearable-health-integration.id}"
}

resource "aws_apigatewayv2_stage" "tfm-wearable-health-stage" {
    api_id      = aws_apigatewayv2_api.tfm-wearable-health-api.id
    name        = "prod"
    auto_deploy = true
}

resource "aws_lambda_permission" "tfm-wearable-health-lambda-permission" {
    statement_id  = "AllowAPIGatewayInvoke"
    action        = "lambda:InvokeFunction"
    function_name = aws_lambda_function.tfm-wearable-health-lambda.function_name
    principal     = "apigateway.amazonaws.com"
    source_arn    = "${aws_apigatewayv2_api.tfm-wearable-health-api.execution_arn}/*/*"
}