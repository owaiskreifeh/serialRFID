#!/bin/bash

# RFID Vault Environment Setup Script
# This script creates a Python virtual environment and installs required packages

echo "=== RFID Vault Environment Setup ==="

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    echo "Please install Python 3 and try again"
    exit 1
fi

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 is not installed or not in PATH"
    echo "Please install pip3 and try again"
    exit 1
fi

echo "Python 3 found: $(python3 --version)"
echo "pip3 found: $(pip3 --version)"

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install required packages
echo "Installing required packages..."
pip install pyserial pynput

# Verify installation
echo "Verifying installation..."
python -c "import serial; print('✓ pyserial installed successfully')"
python -c "import pynput.keyboard; print('✓ pynput installed successfully')"

echo ""
echo "=== Setup Complete ==="
echo "To activate the environment in the future, run:"
echo "  source venv/bin/activate"
echo ""
echo "To run the RFID tool:"
echo "  python rfidvault.py --port <PORT> <COMMAND>"
echo ""
echo "Available commands:"
echo "  monitor - Monitor for card reads"
echo "  write <data> - Write data to card"
echo "  list-cards - List all saved cards"
echo "  list-associations - List all UUID associations"
echo "  associate <uuid> <text> - Associate UUID with text"
echo "  delete-card <uuid> - Delete saved card"
echo "  delete-association <uuid> - Delete UUID association"
