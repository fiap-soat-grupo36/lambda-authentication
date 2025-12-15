terraform {
  backend "s3" {
    bucket = "projeto-oficina-terraform"
    region = "us-east-2"
  }
}
