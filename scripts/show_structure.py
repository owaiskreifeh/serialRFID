#!/usr/bin/env python3
"""
Display the current project structure
"""

import os
from pathlib import Path

def print_tree(directory, prefix="", exclude_dirs=None):
    """Print a tree structure of the directory"""
    if exclude_dirs is None:
        exclude_dirs = {'.git', '__pycache__', 'venv', 'build', 'dist', '.vscode'}
    
    items = sorted(os.listdir(directory))
    
    for i, item in enumerate(items):
        if item in exclude_dirs:
            continue
            
        path = os.path.join(directory, item)
        is_last = i == len(items) - 1
        
        if os.path.isdir(path):
            print(f"{prefix}{'└── ' if is_last else '├── '}{item}/")
            if not is_last:
                print_tree(path, prefix + "│   ", exclude_dirs)
            else:
                print_tree(path, prefix + "    ", exclude_dirs)
        else:
            print(f"{prefix}{'└── ' if is_last else '├── '}{item}")

def main():
    print("📁 serialRFID Project Structure")
    print("=" * 40)
    print()
    
    # Get the project root (assuming this script is in scripts/)
    project_root = Path(__file__).parent.parent
    
    print_tree(project_root)
    
    print()
    print("🔧 Quick Commands:")
    print("  Setup:     scripts/init_env.bat (Windows) or scripts/init_env.sh (Linux/macOS)")
    print("  Run:       scripts/run.bat --port COM3 <command> (Windows)")
    print("  Build:     make build")
    print("  Test:      make test")
    print()
    print("📖 Documentation:")
    print("  Main:      README.md")
    print("  Structure: PROJECT_STRUCTURE.md")
    print("  Guides:    docs/")

if __name__ == "__main__":
    main()
