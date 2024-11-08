#!/bin/bash
# Install Apache if it’s not already installed
yum install -y httpd
# Start Apache if it’s not running
sudo systemctl start httpd
sudo systemctl enable httpd