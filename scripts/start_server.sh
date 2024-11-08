#!/bin/bash
# Install Apache if it’s not already installed
yum install -y httpd
# Start Apache if it’s not running
systemctl start httpd
systemctl enable httpd