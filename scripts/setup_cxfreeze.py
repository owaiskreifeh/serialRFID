#!/usr/bin/env python3
"""
cx_Freeze setup script for creating standalone executable
Alternative to PyInstaller with different advantages
"""

from cx_Freeze import setup, Executable
import sys
import os

# Dependencies that cx_Freeze might miss
build_exe_options = {
    "packages": [
        "serial", 
        "pynput", 
        "pynput.keyboard", 
        "pynput.mouse",
        "json",
        "os",
        "time",
        "threading",
        "argparse",
        "datetime"
    ],
    "excludes": [],
    "include_files": [
        "config/rfid_cards.json",
        "config/rfid_associations.json",
        "README.md"
    ],
    "optimize": 2,
}

# Base for Windows systems
base = None
if sys.platform == "win32":
    base = "Win32GUI"  # Use "Console" if you want console window

# Executable definition
executables = [
    Executable(
        "rfidvault.py",
        base=base,
        target_name="RFIDVault.exe",
        icon=None,  # Add icon file path here if you have one
    )
]

# Setup configuration
setup(
    name="RFIDVault",
    version="1.0.0",
    description="RFID CLI Tool for Arduino RFID Reader/Writer",
    options={"build_exe": build_exe_options},
    executables=executables,
    author="Your Name",
    author_email="your.email@example.com",
)
