locals {
  name        = "terminal-quest"
  environment = "dev"
  region     = "eu-west-1"

  instance_type = "t3.nano"

  vpc_cidr = "10.0.0.0/16"
  azs      = slice(data.aws_availability_zones.available1.names, 0, 3)


  }

module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name = "${local.name}-${local.environment}-${local.region}-vpc"
  cidr = local.vpc_cidr

  azs             = local.azs
  private_subnets = [for k, v in local.azs : cidrsubnet(local.vpc_cidr, 4, k)]
  public_subnets  = [for k, v in local.azs : cidrsubnet(local.vpc_cidr, 8, k + 48)]

}

module "security_group" {
  source  = "terraform-aws-modules/security-group/aws"
  version = "~> 4.0"

  name        = "${local.name}-${local.environment}-${local.region}-linux-sg"
  description = "Security group for ${local.name}-${local.environment} EC2 instance"
  vpc_id      = module.vpc.vpc_id

  ingress_cidr_blocks = ["0.0.0.0/0"]
  ingress_rules       = ["http-80-tcp", "all-icmp", "ssh-tcp"]
  egress_rules        = ["all-all"]

}

module "ec2_instance_root_1" {
  source = "terraform-aws-modules/ec2-instance/aws" # Update the path to your EC2 module

  name = "${local.name}-${local.environment}-${local.region}-linux-1"

  ami                         = data.aws_ami.amazon_linux1.id
  instance_type               = local.instance_type # Choose your instance type
  availability_zone           = element(module.vpc.azs, 0)
  subnet_id                   = element(module.vpc.public_subnets, 0)
  vpc_security_group_ids      = [module.security_group.security_group_id]
  associate_public_ip_address = true
  #user_data_base64            = base64encode(local.user_data)
  #user_data_replace_on_change = true

  cpu_options = {
    core_count       = 2
    threads_per_core = 2
  }
