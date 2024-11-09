#!/bin/bash

echo "Running HTML validation"

# Check if HTML Tidy is installed
if ! command -v tidy &> /dev/null; then
    echo "HTML Tidy is not installed. Installing it now..."
    sudo yum update -y && sudo yum install -y tidy
fi

# Validate HTML files
tidy -errors -q -utf8 index.html > /dev/null
if [ $? -ne 0 ]; then
    echo "HTML validation failed!"
    exit 1
fi

echo "HTML validation passed."


