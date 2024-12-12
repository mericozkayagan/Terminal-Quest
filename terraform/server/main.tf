provider "aws" {
  region = "us-west-2"
}

module "ec2_instance" {
  source  = "terraform-aws-modules/ec2-instance/aws"
  version = "~> 3.0"

  name = "terminal-quest-server"
  instance_type = "t2.micro"
  key_name = "your-key-name"

  ami = "ami-0c55b159cbfafe1f0" # Amazon Linux 2 AMI

  vpc_security_group_ids = ["sg-12345678"]
  subnet_id              = "subnet-12345678"

  tags = {
    Name = "terminal-quest-server"
  }

  user_data = <<-EOF
              #!/bin/bash
              yum update -y
              yum install -y python3 git
              amazon-linux-extras install postgresql10 -y
              git clone https://github.com/yourusername/terminal-quest.git /home/ec2-user/terminal-quest
              cd /home/ec2-user/terminal-quest
              pip3 install -r requirements.txt
              echo "export OPENAI_API_KEY=your_key_here" >> /home/ec2-user/.bashrc
              echo "export DATABASE_URL=your_postgresql_database_url" >> /home/ec2-user/.bashrc
              source /home/ec2-user/.bashrc
              python3 main.py
              EOF
}

output "instance_id" {
  description = "The ID of the EC2 instance"
  value       = module.ec2_instance.id
}

output "public_ip" {
  description = "The public IP address of the EC2 instance"
  value       = module.ec2_instance.public_ip
}
