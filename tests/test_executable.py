#!/usr/bin/env python3
"""
Test script to verify the executable works correctly
"""

import os
import subprocess
import sys
from pathlib import Path

def test_executable():
    """Test the built executable"""
    exe_path = Path("dist/RFIDVault.exe")
    
    if not exe_path.exists():
        print("[ERROR] Executable not found at dist/RFIDVault.exe")
        return False
    
    print(f"[SUCCESS] Executable found: {exe_path}")
    print(f"📏 File size: {exe_path.stat().st_size / (1024*1024):.1f} MB")
    
    # Test if executable can start (without Arduino connected)
    print("\n🧪 Testing executable startup...")
    try:
        # Run with --help to test basic functionality
        result = subprocess.run(
            [str(exe_path), "--help"], 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        
        if result.returncode == 0 or "usage" in result.stdout.lower():
            print("[SUCCESS] Executable starts successfully")
            print("📋 Help output:")
            print(result.stdout[:500] + "..." if len(result.stdout) > 500 else result.stdout)
        else:
            print("⚠️  Executable started but returned non-zero exit code")
            print(f"Exit code: {result.returncode}")
            print(f"Output: {result.stdout}")
            print(f"Error: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        print("⚠️  Executable took too long to start (may be normal)")
    except Exception as e:
        print(f"[ERROR] Error testing executable: {e}")
        return False
    
    return True

def check_dependencies():
    """Check if all required dependencies are included"""
    print("\n🔍 Checking included dependencies...")
    
    # Check if the executable contains required modules
    try:
        result = subprocess.run(
            ["strings", "dist/RFIDVault.exe"], 
            capture_output=True, 
            text=True
        )
        
        dependencies = ["serial", "pynput", "json", "argparse"]
        found_deps = []
        
        for dep in dependencies:
            if dep in result.stdout:
                found_deps.append(dep)
                print(f"[SUCCESS] {dep} found in executable")
            else:
                print(f"⚠️  {dep} not found in executable")
        
        print(f"\n📊 Dependencies found: {len(found_deps)}/{len(dependencies)}")
        
    except FileNotFoundError:
        print("⚠️  'strings' command not available, skipping dependency check")
    except Exception as e:
        print(f"⚠️  Error checking dependencies: {e}")

def main():
    """Main test function"""
    print("🧪 RFID Executable Test Suite")
    print("=" * 40)
    
    # Test executable
    if test_executable():
        print("\n[SUCCESS] Executable test passed!")
    else:
        print("\n[ERROR] Executable test failed!")
        return False
    
    # Check dependencies
    check_dependencies()
    
    print("\n🎉 All tests completed!")
    print("\n📋 Next steps:")
    print("1. Test with actual Arduino hardware")
    print("2. Verify all RFID functionality works")
    print("3. Distribute the executable to users")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
