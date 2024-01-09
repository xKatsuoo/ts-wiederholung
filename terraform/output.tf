output "dns_name" {
  description = "The DNS name of the load balancer."
  value       = module.tf_lb.dns_name
}

output "instance_ip" {
  value = module.tf_ec2.instance_public_ips
}

output "inventory" {
  value = module.tf_ec2.inventory
}

output "private_key" {
  value = module.tf_ec2.private_key
  sensitive = true
}
