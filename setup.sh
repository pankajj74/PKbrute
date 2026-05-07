#!/bin/bash
# PKbrute Installer - Developed by Pankaj

echo "========================================="
echo "PKbrute Installation Script"
echo "Developed by Pankaj"
echo "========================================="

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root (use sudo)"
    exit 1
fi

# Update system
apt update

# Install Python3 and pip if not installed
apt install -y python3 python3-pip

# Install required Python packages
pip3 install -r requirements.txt

# Make the script executable
chmod +x pkbrute.py

# Create alias for bash
echo "alias pkbrute='python3 $(pwd)/pkbrute.py'" >> ~/.bashrc

# Create alias for zsh if exists
if [ -f ~/.zshrc ]; then
    echo "alias pkbrute='python3 $(pwd)/pkbrute.py'" >> ~/.zshrc
fi

echo ""
echo "Installation Complete!"
echo "You can now run PKbrute using: python3 pkbrute.py"
echo "Or reload your terminal and type: pkbrute"
