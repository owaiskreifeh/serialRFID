@echo off
REM RFID Vault Environment Setup Script for Windows
REM This script creates a Python virtual environment and installs required packages

echo === RFID Vault Environment Setup ===

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python and try again
    pause
    exit /b 1
)

REM Check if pip is available
pip --version >nul 2>&1
if errorlevel 1 (
    echo Error: pip is not installed or not in PATH
    echo Please install pip and try again
    pause
    exit /b 1
)

echo Python found: 
python --version
echo pip found:
pip --version

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install required packages
echo Installing required packages...
pip install pyserial pynput

REM Verify installation
echo Verifying installation...
python -c "import serial; print('✓ pyserial installed successfully')"
python -c "import pynput.keyboard; print('✓ pynput installed successfully')"

echo.
echo === Setup Complete ===
echo To activate the environment in the future, run:
echo   venv\Scripts\activate.bat
echo.
echo To run the RFID tool:
echo   python rfidvault.py --port ^<PORT^> ^<COMMAND^>
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
pause
