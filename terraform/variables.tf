variable "aws_region"{
    description = "AWS region to deploy tfm infrastructure"
    type        = string
    default     = "us-east-2"
}

variable "project_name"{
    description = "Project name for resource naming"
    type        = string
    default     = "tfm-wearable-health"
}

variable "bucket_name"{
    description = "S3 bucket name for the Terraform state"
    type        = string
    default     = "anairinac1"
}

variable "aws_account_id" {
    description = "AWS account ID"
    type        = string
    default     = "632103768281"
}