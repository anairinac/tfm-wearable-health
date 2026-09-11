terraform {
  required_version = "~> 1.6"

  backend "s3" {
    bucket  =   "${var.bucket_name}"
    key     =   "${var.project_name}/terraform.tfstate"
    region  =   "${var.aws_region}"
    dynamodb_table = "${var.project_name}-tflock"
    encrypt = true
  }

  required_providers {
    aws = {
        source  = "hashicorp/aws"
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
            description     =   "Keep the last 3 docker images"
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