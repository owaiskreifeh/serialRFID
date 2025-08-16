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
python scripts/release.py 1.0.0
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

## Arduino Setup and Installation

### Hardware Requirements

- **Microcontroller Board**: 
  - **Arduino**: Uno, Nano, Mega, or compatible board
  - **ESP32**: Any ESP32 development board (DOIT DEVKIT V1, NodeMCU-32S, etc.)
  - **ESP8266**: NodeMCU or compatible board
- **RFID Module**: MFRC522 RFID Reader/Writer module
- **RFID Cards**: MIFARE Classic 1K cards (or compatible)
- **Breadboard and Jumper Wires**: For prototyping

#### Pin Connections

**For Arduino Boards:**
- VCC → 3.3V
- GND → GND
- SDA/SS → Digital Pin 5
- SCK → Digital Pin 13
- MOSI → Digital Pin 11
- MISO → Digital Pin 12
- RST → Digital Pin 9 (or any available digital pin)

**For ESP32 Boards:**
- VCC → 3.3V
- GND → GND
- SDA/SS → GPIO 5
- SCK → GPIO 18
- MOSI → GPIO 23
- MISO → GPIO 19
- RST → GPIO 21

**For ESP8266 Boards:**
- VCC → 3.3V
- GND → GND
- SDA/SS → D4 (GPIO 2)
- SCK → D5 (GPIO 14)
- MOSI → D7 (GPIO 13)
- MISO → D6 (GPIO 12)
- RST → D3 (GPIO 0)

### Arduino IDE Installation

1. **Download Arduino IDE**: Visit [arduino.cc](https://www.arduino.cc/en/software) and download the latest version
2. **Install Arduino IDE**: Follow the installation instructions for your operating system
3. **Install Board Support** (for ESP32/ESP8266):
   - **ESP32**: Go to `File → Preferences` and add `https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json` to Additional Board Manager URLs
   - **ESP8266**: Go to `File → Preferences` and add `http://arduino.esp8266.com/stable/package_esp8266com_index.json` to Additional Board Manager URLs
   - Install ESP32/ESP8266 board support via `Tools → Board → Boards Manager`
4. **Install Required Libraries**: Open Arduino IDE and go to `Tools → Manage Libraries`:
   - Search for "MFRC522v2" and install the latest version by GithubCommunity
   - Search for "MFRC522" and install the latest version (backup option)

### Uploading the Firmware

1. **Connect Board**: Connect your microcontroller board to your computer via USB
2. **Select Board**: In Arduino IDE, go to `Tools → Board` and select your board:
   - **Arduino**: Select your specific Arduino board (Uno, Nano, Mega, etc.)
   - **ESP32**: Select your ESP32 board (DOIT DEVKIT V1, NodeMCU-32S, etc.)
   - **ESP8266**: Select your ESP8266 board (NodeMCU 1.0, etc.)
3. **Select Port**: Go to `Tools → Port` and select the correct port:
   - **Windows**: COM3, COM4, etc.
   - **Linux/macOS**: `/dev/ttyUSB0`, `/dev/ttyACM0`, etc.
4. **Open Sketch**: Open the `serialRFID.ino` file in Arduino IDE
5. **Upload**: Click the upload button (→) or press `Ctrl+U` (Windows/Linux) / `Cmd+U` (macOS)

**Note**: For ESP32/ESP8266, you may need to hold the BOOT button during upload if it fails initially.

### Firmware Features

The Arduino firmware provides:

- **Read Mode**: Automatically reads RFID cards and sends data via serial
- **Write Mode**: Accepts commands to write data to RFID cards
- **Serial Communication**: Uses 115200 baud rate for fast data transfer
- **Error Handling**: Provides authentication and read/write error messages
- **Mode Switching**: Responds to `START_WRITE` command to switch modes

### Communication Protocol

The Arduino communicates with the Python application using a specific protocol:

#### Read Mode (Default)
- **Card Detection**: Automatically detects when a card is placed on the reader
- **Data Format**: `START_CARD-{UUID}_CARRIED-{DATA}`
  - UUID: 8-byte card identifier in hex format (e.g., `04:A3:B6:2E:1F:8C:9D:7A`)
  - DATA: 16-character string stored on the card (or "EMPTY" if no data)

#### Write Mode
- **Enter Write Mode**: Send `START_WRITE` command
- **Send Data**: Send the text string to write (max 16 characters)
- **Write to Card**: Place card on reader to write the data
- **Status Messages**: 
  - `Data written successfully to card`
  - `Failed to write data to card`

### Troubleshooting Arduino Issues

1. **Port Not Found**:
   - Check USB connection
   - Install Arduino drivers if needed
   - Try different USB cable
   - **ESP32/ESP8266**: Install CP210x or CH340 drivers if needed

2. **Upload Fails**:
   - Verify correct board selection
   - Check port selection
   - Ensure no other program is using the port
   - **ESP32/ESP8266**: Hold BOOT button during upload if it fails

3. **RFID Module Not Working**:
   - Verify wiring connections
   - Check power supply (3.3V required)
   - Ensure proper library installation
   - **ESP32**: Verify SPI pins are correctly assigned
   - **ESP8266**: Check that pins don't conflict with boot mode

4. **Communication Errors**:
   - Verify baud rate is set to 115200
   - Check serial monitor settings
   - Ensure no conflicting serial communication
   - **ESP32/ESP8266**: Check that pins aren't used by other functions

5. **Library Compatibility Issues**:
   - Use MFRC522v2 library for best compatibility
   - Check library version compatibility with your board
   - Refer to [Random Nerd Tutorials ESP32 MFRC522 Guide](https://randomnerdtutorials.com/esp32-mfrc522-rfid-reader-arduino/) for detailed setup

### Testing the Arduino Setup

1. **Open Serial Monitor**: In Arduino IDE, go to `Tools → Serial Monitor`
2. **Set Baud Rate**: Ensure it's set to 115200
3. **Test Read**: Place an RFID card on the reader - you should see output like:
   ```
   START_CARD-04:A3:B6:2E:1F:8C:9D:7A_CARRIED-EMPTY
   ```
4. **Test Write**: Type `START_WRITE` in serial monitor, then send test data, and place a card

### Arduino Requirements Summary

Your microcontroller must be programmed to:
- Send card data in format: `START_CARD-{UUID}_CARRIED-{DATA}`
- Respond to `START_WRITE` command for writing mode
- Accept data strings for writing to cards
- Send success/failure messages for write operations
- Use 115200 baud rate for serial communication

### Additional Resources

- **[Random Nerd Tutorials ESP32 MFRC522 Guide](https://randomnerdtutorials.com/esp32-mfrc522-rfid-reader-arduino/)**: Comprehensive guide for ESP32 with MFRC522
- **[Arduino MFRC522 Library Documentation](https://github.com/OSSLibraries/Arduino_MFRC522v2)**: Official library documentation
- **[ESP32 Arduino Core Documentation](https://docs.espressif.com/projects/arduino-esp32/en/latest/)**: ESP32 board support documentation

## Troubleshooting

1. **Permission denied on Linux/macOS**: Add your user to the `dialout` group
2. **Port not found**: Check device manager (Windows) or `ls /dev/tty*` (Linux/macOS)
3. **Keyboard output not working**: Ensure pynput is installed and you have appropriate permissions
