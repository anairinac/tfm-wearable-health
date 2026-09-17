resource "aws_apigatewayv2_api" "tfm-wearable-health-api" {
    name          = "${var.project_name}-api"
    protocol_type = "HTTP"
}

resource "aws_apigatewayv2_integration" "tfm-wearable-health-integration" {
    api_id             = aws_apigatewayv2_api.tfm-wearable-health-api.id
    integration_type   = "AWS_PROXY"
    integration_uri    = "arn:aws:lambda:${var.aws_region}:${var.aws_account_id}:function:${var.project_name}-lambda-$${stageVariables.env}"
    payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "tfm-wearable-health-route" {
    api_id    = aws_apigatewayv2_api.tfm-wearable-health-api.id
    route_key = "POST /predict"
    target    = "integrations/${aws_apigatewayv2_integration.tfm-wearable-health-integration.id}"
}

resource "aws_apigatewayv2_stage" "tfm-wearable-health-stage" {
    for_each = toset(local.environments)
    api_id      = aws_apigatewayv2_api.tfm-wearable-health-api.id
    name        = each.key
    auto_deploy = true
    stage_variables = {
        env = each.key
    }
}

resource "aws_lambda_permission" "tfm-wearable-health-lambda-permission" {
    for_each     = toset(local.environments)
    statement_id  = "AllowAPIGatewayInvoke"
    action        = "lambda:InvokeFunction"
    function_name = aws_lambda_function.tfm-wearable-health-lambda[each.key].function_name
    principal     = "apigateway.amazonaws.com"
    source_arn    = "${aws_apigatewayv2_api.tfm-wearable-health-api.execution_arn}/*/*"
}