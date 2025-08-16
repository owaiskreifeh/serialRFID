# RFID Vault

A Python CLI tool for interfacing with Arduino RFID Reader/Writer devices.

## Features

- Read and save RFID card data
- Write data to RFID cards
- Associate UUIDs with custom text
- Output card data or associated text as keyboard input
- Persistent storage of cards and associations

## Setup

### Prerequisites

- Python 3.6 or higher
- pip (Python package installer)
- Arduino with RFID module and appropriate firmware

### Quick Setup

#### Windows
```batch
init_env.bat
```

#### Linux/macOS
```bash
chmod +x init_env.sh
./init_env.sh
```

### Manual Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:
   - Windows: `venv\Scripts\activate.bat`
   - Linux/macOS: `source venv/bin/activate`

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Commands

```bash
# Monitor for card reads
python rfidvault.py --port COM3 monitor

# Monitor with keyboard output
python rfidvault.py --port COM3 monitor --keyboard

# Write data to card
python rfidvault.py --port COM3 write "Hello World"

# List saved cards
python rfidvault.py --port COM3 list-cards

# List associations
python rfidvault.py --port COM3 list-associations

# Associate UUID with text
python rfidvault.py --port COM3 associate "12345678" "My Card"

# Delete saved card
python rfidvault.py --port COM3 delete-card "12345678"

# Delete association
python rfidvault.py --port COM3 delete-association "12345678"
```

### Port Configuration

- **Windows**: Use `COM3`, `COM4`, etc.
- **Linux**: Use `/dev/ttyUSB0`, `/dev/ttyACM0`, etc.
- **macOS**: Use `/dev/tty.usbserial-*`, `/dev/tty.usbmodem*`, etc.

### Keyboard Output

When using the `--keyboard` flag with the monitor command, the tool will:
1. Automatically type the associated text for known cards
2. Type the card data for unknown cards (if data is not "EMPTY")
3. Use pynput library for keyboard simulation

## Data Storage

The tool creates two JSON files for persistent storage:
- `rfid_cards.json`: Stores card UUIDs, data, timestamps, and read counts
- `rfid_associations.json`: Stores UUID-to-text associations

## Arduino Requirements

Your Arduino should be programmed to:
- Send card data in format: `START_CARD-{UUID}_CARRIED-{DATA}`
- Respond to `START_WRITE` command for writing mode
- Accept data strings for writing to cards
- Send success/failure messages for write operations

## Troubleshooting

1. **Permission denied on Linux/macOS**: Add your user to the `dialout` group
2. **Port not found**: Check device manager (Windows) or `ls /dev/tty*` (Linux/macOS)
3. **Keyboard output not working**: Ensure pynput is installed and you have appropriate permissions
