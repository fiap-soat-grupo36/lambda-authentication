terraform {
  backend "s3" {
    bucket               = "projeto-oficina-terraform"
    workspace_key_prefix = "lambda"
    region               = "us-east-2"
  }
}
