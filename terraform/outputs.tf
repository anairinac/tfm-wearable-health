output "ecr_repository_url" {
    description = "URL of the ECR repository for the Lambda function"
    value = aws_ecr_repository.tfm-repository.repository_url
}

output "apigw_endpoint" {
    description = "API Gateway endpoint for the Lambda function"
    value = aws_apigatewayv2_stage.tfm-wearable-health-stage.invoke_url
}