# MSI Installer Instructions
# Author: Devesh Kumar
# Copyright: © 2025 Devesh Kumar. All rights reserved.

## Prerequisites

1. **WiX Toolset v3.11+**
   - Download from: https://wixtoolset.org/releases/
   - Install with default settings
   - Ensure WiX tools are in your PATH

2. **Python 3.8+**
   - Required for the backend application

3. **Node.js 14+**
   - Required for the React Native frontend

## Building the MSI Installer

1. **Run the builder script:**
   ```bash
   python build_msi.py
   ```

2. **Execute the generated build script:**
   ```bash
   build_msi.bat
   ```

3. **The MSI installer will be created in the output directory:**
   ```
   output/KerberosProtocol_v1.0.0.msi
   ```

## Installation Features

✅ **Desktop Shortcut**: Creates a shortcut on the desktop
✅ **Start Menu Entry**: Adds program to Start Menu
✅ **Registry Entries**: Stores installation info and copyright
✅ **Automated Launchers**: Batch and PowerShell scripts included
✅ **Dependency Check**: Verifies Python and Node.js installation
✅ **Complete Package**: All source code and documentation

## Installation Process

1. **Run the MSI installer as Administrator**
2. **Follow the installation wizard**
3. **The application will be installed to:**
   ```
   C:\Program Files\KerberosProtocol\
   ```
4. **Desktop and Start Menu shortcuts will be created**

## Launching the Application

### Option 1: Desktop Shortcut
- Double-click the "Kerberos Protocol Implementation" shortcut

### Option 2: Start Menu
- Go to Start Menu → Kerberos Protocol Implementation

### Option 3: Manual Launch
- Navigate to installation directory
- Run `launch_kerberos.bat` or `launch_kerberos.ps1`

## Post-Installation

The launcher will automatically:
1. Check for Python and Node.js
2. Install required dependencies
3. Start the backend server (http://localhost:8000)
4. Launch the React Native frontend

## Uninstallation

1. **Via Control Panel:**
   - Go to Programs and Features
   - Find "Kerberos Protocol Implementation"
   - Click Uninstall

2. **Via Settings (Windows 10/11):**
   - Go to Settings → Apps
   - Find "Kerberos Protocol Implementation" 
   - Click Uninstall

## Troubleshooting

### Common Issues:

1. **Python not found**
   - Install Python 3.8+ from python.org
   - Ensure Python is added to PATH

2. **Node.js not found**
   - Install Node.js 14+ from nodejs.org
   - Restart command prompt after installation

3. **Permission errors**
   - Run installer as Administrator
   - Check Windows User Account Control settings

4. **WiX build errors**
   - Verify WiX Toolset installation
   - Check that candle.exe and light.exe are in PATH
   - Run build_msi.bat as Administrator

## Technical Details

- **Product Name**: Kerberos Protocol Implementation
- **Version**: 1.0.0
- **Author**: Devesh Kumar
- **Copyright**: © 2025 Devesh Kumar. All rights reserved.
- **Architecture**: Three-headed authentication system
- **Technologies**: React Native, Python Flask, Claude AI, Pinecone

## Support

For technical support or questions:
- Check the documentation in the docs/ folder
- Review the README.md file
- Contact: Devesh Kumar
