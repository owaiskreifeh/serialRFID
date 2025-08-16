# RFID Vault Cross-Platform Build Makefile

.PHONY: help install build build-windows build-macos-intel build-macos-arm64 build-linux build-all clean release test

# Default target
help:
	@echo "RFID Vault Cross-Platform Build System"
	@echo "======================================"
	@echo ""
	@echo "Available targets:"
	@echo "  install        - Install dependencies"
	@echo "  build          - Build for current platform"
	@echo "  build-windows  - Build for Windows"
	@echo "  build-macos-intel - Build for macOS Intel"
	@echo "  build-macos-arm64 - Build for macOS Apple Silicon"
	@echo "  build-linux    - Build for Linux"
	@echo "  build-all      - Build for all platforms"
	@echo "  clean          - Clean build artifacts"
	@echo "  release        - Create a new release"
	@echo "  test           - Test the built executable"
	@echo "  help           - Show this help message"

# Install dependencies
install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt
	pip install pyinstaller

# Build for current platform
build:
	@echo "Building for current platform..."
	python scripts/build_cross_platform.py

# Build for Windows
build-windows:
	@echo "Building for Windows..."
	python scripts/build_cross_platform.py windows

# Build for macOS Intel
build-macos-intel:
	@echo "Building for macOS Intel..."
	python scripts/build_cross_platform.py macos_intel

# Build for macOS Apple Silicon
build-macos-arm64:
	@echo "Building for macOS Apple Silicon..."
	python scripts/build_cross_platform.py macos_arm64

# Build for Linux
build-linux:
	@echo "Building for Linux..."
	python scripts/build_cross_platform.py linux

# Build for all platforms
build-all:
	@echo "Building for all platforms..."
	python scripts/build_cross_platform.py

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	rm -rf build/
	rm -rf dist/
	rm -rf __pycache__/
	rm -rf *.spec
	rm -rf RFIDVault_*.zip

# Create a new release
release:
	@if [ -z "$(VERSION)" ]; then \
		echo "Error: VERSION is required. Use: make release VERSION=1.0.0"; \
		exit 1; \
	fi
	@echo "Creating release $(VERSION)..."
	python scripts/release.py $(VERSION)

# Test the built executable
test:
	@echo "Testing executable..."
	python scripts/test_executable.py

# Quick development build
dev: install build test

# Full release process
full-release: clean install build-all test
	@echo "Full release build completed!"
	@echo "Check the dist/ folder for executables"
