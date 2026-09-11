terraform {
  required_version = "= 1.5"

  required_providers {
    aws = {
        source  = "hasicorp/aws",
        version = "~> 5.0"
    }
  }
}

provider "aws" {
    region = var.aws_region
}

resource "aws_ecr_repository" "tfm-repository" {
    name                    =   "${var.project_name}-lambda"
    image_tag_mutability    =   "MUTABLE"
    image_scanning_configuration {
        scan_on_push = true
    }
}

resource "aws_ecr_lifecycle_policy" "tfm-repository-policy" {
    repository = aws_ecr_repository.tfm-repository.name

    policy = jsonencode({
        rules = [{
            rulePriority    =   1
            description     =   "Keep the last 3 dockeri mages"
            selection       =   {
                tagStatus   =   "any"
                countType   =   "imageCountMoreThan"
                countNumber =   3
            }
            action  =   {
                type    =   "expire"
            }
        }]
    })
}