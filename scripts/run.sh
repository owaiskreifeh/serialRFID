#!/bin/bash

# RFID Vault Run Script
# This script activates the virtual environment and runs the RFID tool

echo "=== RFID Vault Runner ==="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found!"
    echo "Please run the setup script first:"
    echo "  ./init_env.sh"
    exit 1
fi

# Check if rfidvault.py exists
if [ ! -f "rfidvault.py" ]; then
    echo "Error: rfidvault.py not found!"
    echo "Please ensure you're in the correct directory."
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if required packages are installed
echo "Checking required packages..."
python -c "import serial" 2>/dev/null || {
    echo "Error: pyserial not installed!"
    echo "Please run: pip install pyserial"
    exit 1
}

python -c "import pynput.keyboard" 2>/dev/null || {
    echo "Error: pynput not installed!"
    echo "Please run: pip install pynput"
    exit 1
}

echo "✓ All packages verified"

# Check if arguments were provided
if [ $# -eq 0 ]; then
    echo ""
    echo "Usage: $0 --port <PORT> <COMMAND> [OPTIONS]"
    echo ""
    echo "Examples:"
    echo "  $0 --port COM3 monitor"
    echo "  $0 --port COM3 monitor --keyboard"
    echo "  $0 --port COM3 write \"Hello World\""
    echo "  $0 --port COM3 list-cards"
    echo "  $0 --port COM3 list-associations"
    echo "  $0 --port COM3 associate \"12345678\" \"My Card\""
    echo ""
    echo "Available commands:"
    echo "  monitor - Monitor for card reads"
    echo "  write <data> - Write data to card"
    echo "  list-cards - List all saved cards"
    echo "  list-associations - List all UUID associations"
    echo "  associate <uuid> <text> - Associate UUID with text"
    echo "  delete-card <uuid> - Delete saved card"
    echo "  delete-association <uuid> - Delete UUID association"
    echo ""
    echo "Port examples:"
    echo "  Windows: COM3, COM4, etc."
    echo "  Linux: /dev/ttyUSB0, /dev/ttyACM0, etc."
    echo "  macOS: /dev/tty.usbserial-*, /dev/tty.usbmodem*, etc."
    exit 1
fi

# Run the RFID tool
echo "Running RFID tool..."
python rfidvault.py "$@"
