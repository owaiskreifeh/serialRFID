@echo off
REM RFID Vault Run Script for Windows
REM This script activates the virtual environment and runs the RFID tool

echo === RFID Vault Runner ===

REM Check if virtual environment exists
if not exist "venv" (
    echo Error: Virtual environment not found!
    echo Please run the setup script first:
    echo   init_env.bat
    pause
    exit /b 1
)

REM Check if rfidvault.py exists
if not exist "rfidvault.py" (
    echo Error: rfidvault.py not found!
    echo Please ensure you're in the correct directory.
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if required packages are installed
echo Checking required packages...
python -c "import serial" 2>nul
if errorlevel 1 (
    echo Error: pyserial not installed!
    echo Please run: pip install pyserial
    pause
    exit /b 1
)

python -c "import pynput.keyboard" 2>nul
if errorlevel 1 (
    echo Error: pynput not installed!
    echo Please run: pip install pynput
    pause
    exit /b 1
)

echo ✓ All packages verified

REM Check if arguments were provided
if "%~1"=="" (
    echo.
    echo Usage: %0 --port ^<PORT^> ^<COMMAND^> [OPTIONS]
    echo.
    echo Examples:
    echo   %0 --port COM3 monitor
    echo   %0 --port COM3 monitor --keyboard
    echo   %0 --port COM3 write "Hello World"
    echo   %0 --port COM3 list-cards
    echo   %0 --port COM3 list-associations
    echo   %0 --port COM3 associate "12345678" "My Card"
    echo.
    echo Available commands:
    echo   monitor - Monitor for card reads
    echo   write ^<data^> - Write data to card
    echo   list-cards - List all saved cards
    echo   list-associations - List all UUID associations
    echo   associate ^<uuid^> ^<text^> - Associate UUID with text
    echo   delete-card ^<uuid^> - Delete saved card
    echo   delete-association ^<uuid^> - Delete UUID association
    echo.
    echo Port examples:
    echo   Windows: COM3, COM4, etc.
    echo   Linux: /dev/ttyUSB0, /dev/ttyACM0, etc.
    echo   macOS: /dev/tty.usbserial-*, /dev/tty.usbmodem*, etc.
    pause
    exit /b 1
)

REM Run the RFID tool
echo Running RFID tool...
python rfidvault.py %*
