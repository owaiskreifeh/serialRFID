# Project Structure

This document describes the organized structure of the serialRFID project.

## Root Directory

The root directory contains the main application files and core project structure:

```
serialRFID/
├── rfidvault.py          # Main Python CLI application
├── serialRFID.ino        # Arduino firmware for RFID reader/writer
├── requirements.txt      # Python dependencies
├── Makefile             # Build automation
├── README.md            # Project documentation
├── .gitignore           # Git ignore rules
├── .github/             # GitHub workflows and templates
├── .vscode/             # VS Code configuration
├── venv/                # Python virtual environment
├── build/               # Build artifacts (auto-generated)
├── dist/                # Distribution files (auto-generated)
├── scripts/             # Build and utility scripts
├── config/              # Configuration files
├── docs/                # Documentation files
└── tests/               # Test files
```

## Directory Details

### `/scripts/` - Build and Utility Scripts
Contains all build scripts, automation tools, and utility scripts:

- `build_cross_platform.py` - Cross-platform executable builder
- `build_exe.py` - Windows executable builder
- `build_gui.py` - GUI application builder
- `build_all.bat` - Windows batch build script
- `setup_cxfreeze.py` - cx_Freeze configuration
- `release.py` - Release automation script
- `init_env.bat` - Windows environment setup
- `init_env.sh` - Linux/macOS environment setup
- `run.bat` - Windows run script
- `run.sh` - Linux/macOS run script

### `/config/` - Configuration Files
Contains application configuration and specification files:

- `rfid_cards.json` - RFID card database
- `RFIDVault.spec` - PyInstaller specification file

### `/docs/` - Documentation
Contains project documentation and guides:

- `CROSS_PLATFORM_GUIDE.md` - Cross-platform build guide
- `CROSS_PLATFORM_SUMMARY.md` - Cross-platform build summary
- `EXECUTABLE_SUMMARY.md` - Executable build summary
- `PACKAGING_GUIDE.md` - Packaging and distribution guide

### `/tests/` - Test Files
Contains test scripts and test data:

- Test files for application functionality
- Unit tests and integration tests

### `/build/` - Build Artifacts
Auto-generated directory containing build outputs and temporary files.

### `/dist/` - Distribution Files
Auto-generated directory containing final distribution packages.

## Main Application Files

### `rfidvault.py`
The main Python CLI application that provides:
- RFID card reading and writing functionality
- Serial communication with Arduino
- Card database management
- Keyboard output simulation

### `serialRFID.ino`
The Arduino firmware that:
- Interfaces with MFRC522 RFID reader/writer
- Handles card reading and writing operations
- Communicates with Python application via serial
- Supports both read and write modes

## Development Workflow

1. **Setup**: Use scripts in `/scripts/` to initialize the environment
2. **Development**: Work with main files in root directory
3. **Testing**: Use test files in `/tests/` directory
4. **Building**: Use build scripts in `/scripts/` directory
5. **Documentation**: Update docs in `/docs/` directory

## Benefits of This Structure

- **Clean Root**: Main application files remain easily accessible
- **Logical Organization**: Related files grouped by purpose
- **Maintainability**: Clear separation of concerns
- **Scalability**: Easy to add new scripts, configs, or docs
- **Developer Experience**: Intuitive file locations
