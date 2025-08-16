# 🌍 Cross-Platform RFID Application Guide

This guide explains how to package your RFID Python application for Windows, macOS (Intel/Apple Silicon), and Linux with automated GitHub Actions builds.

## 🚀 Quick Start

### Automated Build (All Platforms)
```bash
# Build for all platforms
python build_cross_platform.py

# Build for specific platform
python build_cross_platform.py windows
python build_cross_platform.py macos_intel
python build_cross_platform.py macos_arm64
python build_cross_platform.py linux
```

### GitHub Actions Release
```bash
# Create a new release (triggers automated builds)
python scripts/release.py 1.0.0
```

## 📦 Supported Platforms

| Platform | Architecture | Executable | Package |
|----------|-------------|------------|---------|
| Windows | x64 | `RFIDVault.exe` | `RFIDVault_windows.zip` |
| macOS | Intel (x64) | `RFIDVault` | `RFIDVault_macos_intel.zip` |
| macOS | Apple Silicon (ARM64) | `RFIDVault` | `RFIDVault_macos_arm64.zip` |
| Linux | x64 | `RFIDVault` | `RFIDVault_linux.zip` |

## 🔧 Build Process

### Local Development

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install pyinstaller
   ```

2. **Build for Current Platform**
   ```bash
   python scripts/build_cross_platform.py
   ```

3. **Build for Specific Platform**
   ```bash
   python scripts/build_cross_platform.py windows
   python scripts/build_cross_platform.py macos_intel
   python scripts/build_cross_platform.py macos_arm64
   python scripts/build_cross_platform.py linux
   ```

### GitHub Actions (Automated)

1. **Create Release**
   ```bash
   python scripts/release.py 1.0.0
   ```

2. **Monitor Build**
   - Check GitHub Actions tab
   - Wait for all platforms to complete
   - Review generated release

## 📁 Output Structure

```
dist/
├── RFIDVault.exe          # Windows executable
├── RFIDVault              # macOS/Linux executable
├── rfid_cards.json        # Data file
├── rfid_associations.json # Data file
├── README.md             # Documentation
├── LAUNCH.bat           # Windows launcher
└── LAUNCH.sh            # macOS/Linux launcher
```

## 🎯 Platform-Specific Features

### Windows
- **Executable**: `RFIDVault.exe`
- **Launcher**: `LAUNCH.bat`
- **Features**: Windowed mode, no console
- **Size**: ~8-12 MB

### macOS
- **Executable**: `RFIDVault`
- **Launcher**: `LAUNCH.sh`
- **Features**: Universal binary support
- **Size**: ~10-15 MB
- **Architectures**: Intel (x64), Apple Silicon (ARM64)

### Linux
- **Executable**: `RFIDVault`
- **Launcher**: `LAUNCH.sh`
- **Features**: Console mode
- **Size**: ~8-12 MB
- **Dependencies**: Minimal (glibc)

## 🔄 GitHub Actions Workflow

### Triggers
- **Automatic**: Push tags starting with `v*` (e.g., `v1.0.0`)
- **Manual**: GitHub Actions UI with version input

### Process
1. **Build Matrix**: Parallel builds for all platforms
2. **Dependencies**: Install Python and required packages
3. **Packaging**: Create platform-specific executables
4. **Artifacts**: Upload build artifacts
5. **Release**: Create GitHub release with downloads

### Workflow File
```yaml
# .github/workflows/build.yml
name: Build and Release
on:
  push:
    tags: ['v*']
  workflow_dispatch:
```

## 📋 Release Process

### 1. Prepare Release
```bash
# Ensure all changes are committed
git add .
git commit -m "Prepare for release"

# Create release
python release.py 1.0.0
```

### 2. Automated Build
- GitHub Actions builds for all platforms
- Creates release with download links
- Uploads platform-specific ZIP files

### 3. Manual Review
- Check Actions tab for build status
- Review generated release
- Test downloaded executables

## 🐛 Platform-Specific Issues

### Windows
- **Antivirus Warnings**: Common with PyInstaller
- **DLL Issues**: May need Visual C++ Redistributable
- **Serial Ports**: COM1, COM2, etc.

### macOS
- **Gatekeeper**: May block unsigned executables
- **Architecture**: Ensure correct architecture for your Mac
- **Serial Ports**: `/dev/tty.usbserial-*`

### Linux
- **Permissions**: May need to make executable
- **Dependencies**: Minimal, but check glibc version
- **Serial Ports**: `/dev/ttyUSB*`, `/dev/ttyACM*`

## 🔧 Troubleshooting

### Build Failures
1. **Check Dependencies**: Ensure all requirements installed
2. **Platform Issues**: Build on target platform if possible
3. **PyInstaller Issues**: Update to latest version
4. **Memory Issues**: Increase GitHub Actions memory if needed

### Runtime Issues
1. **Serial Port Access**: Check permissions and drivers
2. **Missing Libraries**: Ensure all dependencies included
3. **Architecture Mismatch**: Use correct platform build

### GitHub Actions Issues
1. **Timeout**: Increase workflow timeout
2. **Memory**: Use larger runners if needed
3. **Permissions**: Check repository permissions

## 📊 Build Statistics

### Typical Build Times
- **Windows**: 3-5 minutes
- **macOS**: 4-6 minutes
- **Linux**: 2-4 minutes

### File Sizes
- **Windows**: 8-12 MB
- **macOS**: 10-15 MB
- **Linux**: 8-12 MB

### Dependencies Included
- `pyserial` - Serial communication
- `pynput` - Keyboard/mouse input
- Python standard library
- Platform-specific libraries

## 🎉 Success Checklist

- [ ] All platforms build successfully
- [ ] Executables run on target platforms
- [ ] Serial communication works
- [ ] All features functional
- [ ] Release created with downloads
- [ ] Documentation updated
- [ ] Users can download and run

## 📞 Support

### For Developers
- Check build logs in GitHub Actions
- Test locally before releasing
- Monitor for platform-specific issues

### For Users
- Download correct platform version
- Check system requirements
- Report issues with platform details

## 🔄 Maintenance

### Regular Tasks
1. **Update Dependencies**: Keep requirements.txt current
2. **Test Builds**: Verify all platforms still work
3. **Monitor Issues**: Track platform-specific problems
4. **Update Documentation**: Keep guides current

### Version Management
```bash
# Major release
python scripts/release.py 2.0.0

# Minor release
python scripts/release.py 1.1.0

# Patch release
python scripts/release.py 1.0.1
```

---

*Built with ❤️ for cross-platform compatibility*
