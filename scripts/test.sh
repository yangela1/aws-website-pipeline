#!/bin/bash

echo "Running HTML validation and link checking..."

# Check if HTML Tidy is installed
if ! command -v tidy &> /dev/null; then
    echo "HTML Tidy is not installed. Installing it now..."
    sudo apt-get update && sudo apt-get install -y tidy
fi

# Validate HTML files
tidy -errors -q -utf8 index.html > /dev/null
if [ $? -ne 0 ]; then
    echo "HTML validation failed!"
    exit 1
fi

echo "HTML validation passed."

# Check links (change 'index.html' to the main file if different)
if ! wget --spider -r -nd -nv -l 1 -o link-check.log index.html; then
    echo "Link check failed! See link-check.log for details."
    exit 1
fi

echo "Link check passed."
