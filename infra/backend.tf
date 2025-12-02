terraform {
  backend "s3" {
    bucket = "projeto-oficina-terraform"
    key    = "lambda/terraform.tfstate"
    region = "us-east-2"
  }
}
