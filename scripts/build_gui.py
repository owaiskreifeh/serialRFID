#!/usr/bin/env python3
"""
GUI-based build script using auto-py-to-exe
Provides a user-friendly interface for creating executables
"""

import subprocess
import sys

def install_auto_py_to_exe():
    """Install auto-py-to-exe if not already installed"""
    try:
        import auto_py_to_exe
        print("auto-py-to-exe is already installed")
    except ImportError:
        print("Installing auto-py-to-exe...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "auto-py-to-exe"])
        print("auto-py-to-exe installed successfully")

def launch_gui():
    """Launch the auto-py-to-exe GUI"""
    try:
        subprocess.run([sys.executable, "-m", "auto_py_to_exe"])
    except KeyboardInterrupt:
        print("\nGUI closed by user")
    except Exception as e:
        print(f"Error launching GUI: {e}")

if __name__ == "__main__":
    print("Auto-py-to-exe GUI Builder")
    print("=" * 30)
    print("This will open a GUI where you can:")
    print("1. Select rfidvault.py as your script")
    print("2. Choose 'One File' or 'One Directory'")
    print("3. Add data files (rfid_cards.json, rfid_associations.json)")
    print("4. Configure additional options")
    print("5. Build your executable")
    print()
    
    install_auto_py_to_exe()
    launch_gui()
