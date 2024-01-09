terraform {
  backend "s3" {
    key    = "terraform.tfstate"
    region = "eu-central-1"
    profile = "techstarter"
  }
}
