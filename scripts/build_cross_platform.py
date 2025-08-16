#!/usr/bin/env python3
"""
Cross-platform build script for creating standalone executables
Supports Windows, macOS (Intel/Apple Silicon), and Linux
"""

import os
import sys
import subprocess
import shutil
import platform
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

def get_platform_info():
    """Get current platform information"""
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    if system == "darwin":
        if machine in ["arm64", "aarch64"]:
            return "macos_arm64"
        else:
            return "macos_intel"
    elif system == "linux":
        return "linux"
    elif system == "windows":
        return "windows"
    else:
        return "unknown"

def get_executable_name():
    """Get the appropriate executable name for the platform"""
    platform_name = get_platform_info()
    
    if platform_name == "windows":
        return "RFIDVault.exe"
    else:
        return "RFIDVault"

def get_data_file_separator():
    """Get the appropriate separator for data files based on platform"""
    platform_name = get_platform_info()
    
    if platform_name == "windows":
        return ";"
    else:
        return ":"

def build_for_platform(target_platform=None):
    """Build executable for specific platform"""
    
    # Use current platform if none specified
    if target_platform is None:
        target_platform = get_platform_info()
    
    print(f"Building for platform: {target_platform}")
    
    # Main script to package
    main_script = "rfidvault.py"
    
    # Get platform-specific settings
    data_sep = get_data_file_separator()
    exe_name = get_executable_name()
    
    # Base PyInstaller command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",  # Create a single executable file
        "--name=RFIDVault",  # Name of the executable
        "--hidden-import=serial",  # Ensure serial is included
        "--hidden-import=pynput",  # Ensure pynput is included
        "--hidden-import=pynput.keyboard",  # Ensure keyboard module is included
        "--hidden-import=pynput.mouse",  # Ensure mouse module is included
        "--clean",  # Clean cache before building
    ]
    
    # Platform-specific options
    if target_platform == "windows":
        cmd.append("--windowed")  # Don't show console window on Windows
    elif target_platform.startswith("macos"):
        # macOS specific options
        cmd.extend([
            "--target-architecture", "universal2" if target_platform == "macos_universal" else "x86_64" if target_platform == "macos_intel" else "arm64",
            "--codesign-identity", "-"  # Ad-hoc signing
        ])
    
    # Add data files only if they exist
    data_files = ["config/rfid_cards.json", "config/rfid_associations.json"]
    for file in data_files:
        if os.path.exists(file):
            cmd.extend(["--add-data", f"{file}{data_sep}."])
            print(f"Adding data file: {file}")
        else:
            print(f"Warning: Data file {file} not found, skipping...")
    
    cmd.append(main_script)
    
    print("Building executable...")
    print(f"Command: {' '.join(cmd)}")
    
    try:
        subprocess.check_call(cmd)
        print(f"\n✅ Build completed successfully for {target_platform}!")
        
        # Copy additional files to dist folder
        dist_folder = Path("dist")
        files_to_copy = ["config/rfid_cards.json", "config/rfid_associations.json", "README.md"]
        
        for file in files_to_copy:
            if os.path.exists(file):
                shutil.copy2(file, dist_folder)
                print(f"Copied {file} to dist folder")
            else:
                print(f"Warning: {file} not found, skipping copy...")
        
        # Create platform-specific launcher
        create_platform_launcher(target_platform, dist_folder)
        
        print(f"\n📁 Distribution folder created at: dist/")
        print(f"Executable: dist/{exe_name}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed for {target_platform}: {e}")
        return False

def create_platform_launcher(platform_name, dist_folder):
    """Create platform-specific launcher script"""
    
    if platform_name == "windows":
        # Windows batch file
        launcher_content = """@echo off
echo ========================================
echo    RFID Vault - Arduino RFID Tool
echo ========================================
echo.
echo Starting RFID application...
echo.

REM Run the executable
RFIDVault.exe

REM If the executable exits, pause to show any error messages
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Application exited with error code: %ERRORLEVEL%
    echo.
    pause
)
"""
        launcher_path = dist_folder / "LAUNCH.bat"
        
    else:
        # Unix shell script (macOS/Linux)
        launcher_content = """#!/bin/bash
echo "========================================"
echo "   RFID Vault - Arduino RFID Tool"
echo "========================================"
echo ""
echo "Starting RFID application..."
echo ""

# Run the executable
./RFIDVault

# If the executable exits, show any error messages
if [ $? -ne 0 ]; then
    echo ""
    echo "Application exited with error code: $?"
    echo ""
    read -p "Press Enter to continue..."
fi
"""
        launcher_path = dist_folder / "LAUNCH.sh"
        
        # Make executable on Unix systems
        try:
            os.chmod(launcher_path, 0o755)
        except:
            pass
    
    with open(launcher_path, 'w') as f:
        f.write(launcher_content)
    
    print(f"Created launcher: {launcher_path}")

def create_distribution_package(platform_name):
    """Create a complete distribution package for the platform"""
    dist_folder = Path("dist")
    
    if not dist_folder.exists():
        print("❌ Dist folder not found. Run build first.")
        return
    
    # Create a zip file of the distribution
    import zipfile
    
    zip_name = f"RFIDVault_{platform_name}.zip"
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in dist_folder.rglob('*'):
            if file_path.is_file():
                arcname = file_path.relative_to(dist_folder)
                zipf.write(file_path, arcname)
    
    print(f"📦 Distribution package created: {zip_name}")

def build_all_platforms():
    """Build for all supported platforms"""
    platforms = ["windows", "macos_intel", "macos_arm64", "linux"]
    current_platform = get_platform_info()
    
    print("🚀 Cross-Platform RFID Application Builder")
    print("=" * 50)
    print(f"Current platform: {current_platform}")
    print()
    
    # Install PyInstaller
    install_pyinstaller()
    
    success_count = 0
    
    for platform_name in platforms:
        print(f"\n{'='*20} Building for {platform_name} {'='*20}")
        
        # Clean previous builds
        if os.path.exists("dist"):
            shutil.rmtree("dist")
        if os.path.exists("build"):
            shutil.rmtree("build")
        
        # Build for this platform
        if build_for_platform(platform_name):
            create_distribution_package(platform_name)
            success_count += 1
        else:
            print(f"❌ Failed to build for {platform_name}")
    
    print(f"\n{'='*50}")
    print(f"Build Summary: {success_count}/{len(platforms)} platforms successful")
    
    if success_count == len(platforms):
        print("🎉 All platforms built successfully!")
    else:
        print("⚠️  Some platforms failed to build")
    
    return success_count == len(platforms)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target = sys.argv[1]
        
        # Handle help argument
        if target in ['-h', '--help', 'help']:
            print("""
Cross-Platform RFID Application Builder

Usage:
  python build_cross_platform.py [platform]

Platforms:
  windows      - Build for Windows
  macos_intel  - Build for macOS Intel
  macos_arm64  - Build for macOS Apple Silicon
  linux        - Build for Linux
  (no args)    - Build for all platforms

Examples:
  python build_cross_platform.py windows
  python build_cross_platform.py macos_intel
  python build_cross_platform.py
""")
            sys.exit(0)
        
        # Build for specific platform
        install_pyinstaller()
        success = build_for_platform(target)
        if success:
            create_distribution_package(target)
        sys.exit(0 if success else 1)
    else:
        # Build for all platforms
        success = build_all_platforms()
        sys.exit(0 if success else 1)
