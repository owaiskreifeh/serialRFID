#!/usr/bin/env python3
"""
Build script for creating standalone executable from RFID application
Uses PyInstaller to package the application with all dependencies
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def install_pyinstaller():
    """Install PyInstaller if not already installed"""
    try:
        import PyInstaller
        print("PyInstaller is already installed")
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("PyInstaller installed successfully")

def build_executable():
    """Build the executable using PyInstaller"""
    
    # Main script to package
    main_script = "rfidvault.py"
    
    # Find PyInstaller executable
    try:
        import PyInstaller
        pyinstaller_path = "pyinstaller"
    except ImportError:
        print("PyInstaller not found in Python path")
        return False
    
    # Build PyInstaller command with only existing files
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",  # Create a single executable file
        "--windowed",  # Don't show console window (remove this if you want console)
        "--name=RFIDVault",  # Name of the executable
        "--hidden-import=serial",  # Ensure serial is included
        "--hidden-import=pynput",  # Ensure pynput is included
        "--hidden-import=pynput.keyboard",  # Ensure keyboard module is included
        "--hidden-import=pynput.mouse",  # Ensure mouse module is included
        "--clean",  # Clean cache before building
        main_script
    ]
    
    # Add data files only if they exist
    data_files = ["config/rfid_cards.json", "config/rfid_associations.json"]
    for file in data_files:
        if os.path.exists(file):
            cmd.extend(["--add-data", f"{file};."])
            print(f"Adding data file: {file}")
        else:
            print(f"Warning: Data file {file} not found, skipping...")
    
    print("Building executable...")
    print(f"Command: {' '.join(cmd)}")
    
    try:
        subprocess.check_call(cmd)
        print("\n✅ Build completed successfully!")
        print(f"Executable location: dist/RFIDVault.exe")
        
        # Copy additional files to dist folder
        dist_folder = Path("dist")
        files_to_copy = ["config/rfid_cards.json", "config/rfid_associations.json", "README.md"]
        
        for file in files_to_copy:
            if os.path.exists(file):
                shutil.copy2(file, dist_folder)
                print(f"Copied {file} to dist folder")
            else:
                print(f"Warning: {file} not found, skipping copy...")
        
        print("\n📁 Distribution folder created at: dist/")
        print("You can now distribute the entire 'dist' folder")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return False
    
    return True

def create_distribution_package():
    """Create a complete distribution package"""
    dist_folder = Path("dist")
    
    if not dist_folder.exists():
        print("❌ Dist folder not found. Run build first.")
        return
    
    # Create a zip file of the distribution
    import zipfile
    
    zip_name = "RFIDVault_Standalone.zip"
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in dist_folder.rglob('*'):
            if file_path.is_file():
                arcname = file_path.relative_to(dist_folder)
                zipf.write(file_path, arcname)
    
    print(f"📦 Distribution package created: {zip_name}")

if __name__ == "__main__":
    print("🚀 RFID Application Builder")
    print("=" * 40)
    
    # Install PyInstaller
    install_pyinstaller()
    
    # Build executable
    if build_executable():
        # Create distribution package
        create_distribution_package()
        
        print("\n🎉 Build process completed!")
        print("\nNext steps:")
        print("1. Test the executable: dist/RFIDVault.exe")
        print("2. Distribute the 'dist' folder or the zip file")
        print("3. Users can run RFIDVault.exe without Python installed")
    else:
        print("\n❌ Build process failed!")
        sys.exit(1)
