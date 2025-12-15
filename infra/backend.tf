terraform {
  backend "s3" {
    bucket               = "projeto-oficina-terraform"
    key                  = "terraform.tfstate"
    workspace_key_prefix = "lambda"
    region               = "us-east-2"
  }
}
