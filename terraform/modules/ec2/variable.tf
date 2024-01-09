variable "ec2_instance_name" {
  type    = string
  default = "flask"
}

variable "ec2_instance_type" {
  type    = string
  default = "t2.micro"
}

variable "ec2_instance_ami" {
  type    = string
  default = "ami-06dd92ecc74fdfb36" # ubuntu
}

variable "subnet_id" {}

variable "vpc_id" {}
