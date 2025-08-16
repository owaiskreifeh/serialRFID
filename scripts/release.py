#!/usr/bin/env python3
"""
Release management script for RFID Vault
Handles versioning, tagging, and release preparation
"""

import os
import sys
import subprocess
import re
from pathlib import Path

def get_current_version():
    """Get current version from git tags"""
    try:
        result = subprocess.run(
            ["git", "describe", "--tags", "--abbrev=0"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            version = result.stdout.strip()
            if version.startswith('v'):
                return version[1:]  # Remove 'v' prefix
        return "0.0.0"
    except:
        return "0.0.0"

def validate_version(version):
    """Validate version format (semantic versioning)"""
    pattern = r'^\d+\.\d+\.\d+$'
    if not re.match(pattern, version):
        raise ValueError(f"Invalid version format: {version}. Use format: X.Y.Z")
    return version

def update_version_files(version):
    """Update version in relevant files"""
    print(f"Updating version to {version} in files...")
    
    # Update setup.py if it exists
    setup_py = Path("setup.py")
    if setup_py.exists():
        with open(setup_py, 'r') as f:
            content = f.read()
        
        # Update version in setup.py
        content = re.sub(
            r'version=["\']([^"\']+)["\']',
            f'version="{version}"',
            content
        )
        
        with open(setup_py, 'w') as f:
            f.write(content)
        print("[SUCCESS] Updated setup.py")

def create_release(version):
    """Create a new release"""
    version = validate_version(version)
    
    print(f"Creating release v{version}")
    print("=" * 40)
    
    # Check if working directory is clean
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True
        )
        if result.stdout.strip():
            print("[ERROR] Working directory is not clean. Please commit or stash changes.")
            return False
    except Exception as e:
        print(f"[ERROR] Error checking git status: {e}")
        return False
    
    # Update version files
    update_version_files(version)
    
    # Commit version changes
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", f"Bump version to {version}"], check=True)
        print("[SUCCESS] Committed version changes")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Error committing changes: {e}")
        return False
    
    # Create and push tag
    try:
        subprocess.run(["git", "tag", f"v{version}"], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        subprocess.run(["git", "push", "origin", f"v{version}"], check=True)
        print("[SUCCESS] Created and pushed tag")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Error creating tag: {e}")
        return False
    
    print(f"\n[SUCCESS] Release v{version} created successfully!")
    print("\nNext steps:")
    print("1. GitHub Actions will automatically build and create a release")
    print("2. Check the Actions tab in your GitHub repository")
    print("3. Review and publish the release")
    
    return True

def show_help():
    """Show help information"""
    print("""
RFID Vault Release Manager

Usage:
  python scripts/release.py <version>

Examples:
  python scripts/release.py 1.0.0
  python scripts/release.py 1.2.3

This script will:
1. Validate the version format
2. Update version in relevant files
3. Commit the changes
4. Create and push a git tag
5. Trigger GitHub Actions build

The GitHub Actions workflow will then:
1. Build executables for all platforms
2. Create a GitHub release
3. Upload platform-specific ZIP files
""")

def main():
    """Main function"""
    if len(sys.argv) != 2:
        show_help()
        sys.exit(1)
    
    version = sys.argv[1]
    
    if version in ['-h', '--help', 'help']:
        show_help()
        sys.exit(0)
    
    try:
        success = create_release(version)
        sys.exit(0 if success else 1)
    except ValueError as e:
        print(f"[ERROR] {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n[ERROR] Release cancelled by user")
        sys.exit(1)

if __name__ == "__main__":
    main()
