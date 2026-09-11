output "ecr_repository_url" {
    description = "URL of the ECR repository for the Lambda function"
    value = aws_ecr_repository.tfm-repository.repository_url
}