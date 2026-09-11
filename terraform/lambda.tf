resource "aws_iam_role" "tfm-wearable-health-lambda-role" {
    name    =   "${var.project_name}-lambda-role"
    assume_role_policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
            {
                Effect = "Allow"
                Principal = {
                    Service = "lambda.amazonaws.com"
                }
                Action = "sts:AssumeRole"
            }
        ]
    })
}

resource "aws_iam_role_policy_attachment" "tfm-wearable-health-lambda-policy" {
    role        =   aws_iam_role.tfm-wearable-health-lambda-role.name
    policy_arn  =   "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_lambda_function" "tfm-wearable-health-lambda" {
    function_name   =   "${var.project_name}-lambda"
    role            =   aws_iam_role.tfm-wearable-health-lambda-role.arn
    package_type    =   "Image"
    image_uri       =   "${aws_ecr_repository.tfm-repository.repository_url}:latest"
    architectures   =   ["arm64"]
    timeout         =   30
    memory_size     =   512

    depends_on      =   [
        aws_iam_role_policy_attachment.tfm-wearable-health-lambda-policy
    ]
}

