output "sg_id" {
  value = aws_security_group.sg.id
}

output "ec2_id" {
  value = aws_instance.main.*.id
}

output "instance_public_ips" {
  value = aws_instance.main.*.public_ip
}

output "inventory" {
  value = templatefile("${path.module}/templates/inventory.tftpl", {
    ip_addrs = aws_instance.main.*.public_ip
  })
}

output "private_key" {
  value = tls_private_key.key.private_key_pem
  sensitive = true
}
