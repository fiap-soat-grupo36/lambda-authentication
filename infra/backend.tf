terraform {
  backend "s3" {
    bucket = "projeto-oficina-terraform"
    key    = "lambda/${terraform.workspace}/terraform.tfstate"
    region = "us-east-2"
  }
}
