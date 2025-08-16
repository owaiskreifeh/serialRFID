# RFID Vault

A cross-platform Python CLI tool for interfacing with Arduino RFID Reader/Writer devices.

## Features

- Read and save RFID card data
- Write data to RFID cards
- Associate UUIDs with custom text
- Output card data or associated text as keyboard input
- Persistent storage of cards and associations
- **Cross-platform support**: Windows, macOS (Intel/Apple Silicon), Linux
- **Standalone executables**: No Python installation required for end users

## Setup

### For End Users (Standalone Executables)

Download the appropriate executable for your platform from the [Releases](https://github.com/yourusername/serialRFID/releases) page:

- **Windows**: `RFIDVault_windows.zip`
- **macOS Intel**: `RFIDVault_macos_intel.zip`
- **macOS Apple Silicon**: `RFIDVault_macos_arm64.zip`
- **Linux**: `RFIDVault_linux.zip`

1. Extract the ZIP file
2. Run the launcher:
   - Windows: Double-click `LAUNCH.bat`
   - macOS/Linux: Run `./LAUNCH.sh`

### For Developers

#### Prerequisites

- Python 3.6 or higher
- pip (Python package installer)
- Arduino with RFID module and appropriate firmware

### Quick Setup

#### Windows
```batch
scripts/init_env.bat
```

#### Linux/macOS
```bash
chmod +x scripts/init_env.sh
./scripts/init_env.sh
```

### Running the Tool

#### Windows
```batch
scripts/run.bat --port COM3 <COMMAND>
```

#### Linux/macOS
```bash
chmod +x scripts/run.sh
./scripts/run.sh --port /dev/ttyUSB0 <COMMAND>
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

## Building and Releasing

### Quick Build

```bash
# Build for current platform
make build

# Build for all platforms
make build-all

# Build for specific platform
make build-windows
make build-macos-intel
make build-macos-arm64
make build-linux
```

### Creating a Release

```bash
# Create a new release (triggers GitHub Actions)
make release VERSION=1.0.0

# Or use the Python script directly
python release.py 1.0.0
```

### GitHub Actions

The project includes automated GitHub Actions that:
- Build executables for all platforms
- Create GitHub releases with downloads
- Upload platform-specific ZIP files

Trigger by pushing a version tag: `git tag v1.0.0 && git push origin v1.0.0`

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

### Cross-Platform Compatibility

The application works on:
- **Windows 10/11** (x64)
- **macOS 10.15+** (Intel x64 and Apple Silicon ARM64)
- **Linux** (x64, glibc-based distributions)

Standalone executables are available for all platforms and don't require Python installation.

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
