"""
MSI Installer Builder for Kerberos Protocol Implementation
Author: Devesh Kumar
Copyright: © 2025 Devesh Kumar. All rights reserved.
Description: Creates MSI installer with desktop shortcut
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
import json
from datetime import datetime

# Configuration
PRODUCT_NAME = "Kerberos Protocol Implementation"
PRODUCT_VERSION = "1.0.0"
MANUFACTURER = "Devesh Kumar"
COPYRIGHT = f"© {datetime.now().year} Devesh Kumar. All rights reserved."
DESCRIPTION = "3-headed dog Kerberos protocol implementation with React Native frontend and Python backend"
INSTALL_DIR = r"C:\Program Files\KerberosProtocol"
DESKTOP_SHORTCUT = True
START_MENU_SHORTCUT = True

class MSIBuilder:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.installer_dir = Path(__file__).parent
        self.build_dir = self.installer_dir / "build"
        self.output_dir = self.installer_dir / "output"
        
    def prepare_build_directory(self):
        """Prepare the build directory with all necessary files"""
        print("🔨 Preparing build directory...")
        
        # Clean and create build directory
        if self.build_dir.exists():
            shutil.rmtree(self.build_dir)
        self.build_dir.mkdir(parents=True, exist_ok=True)
        
        # Create application structure
        app_dir = self.build_dir / "app"
        app_dir.mkdir(exist_ok=True)
        
        # Copy backend files
        backend_dir = app_dir / "backend"
        shutil.copytree(self.project_root / "backend", backend_dir)
        
        # Copy frontend build (in real scenario, you'd build the React Native app first)
        frontend_dir = app_dir / "frontend"
        shutil.copytree(self.project_root / "frontend", frontend_dir)
        
        # Copy documentation
        docs_dir = app_dir / "docs"
        if (self.project_root / "docs").exists():
            shutil.copytree(self.project_root / "docs", docs_dir)
        else:
            docs_dir.mkdir(exist_ok=True)
        
        # Copy shared files
        shared_dir = app_dir / "shared"
        if (self.project_root / "shared").exists():
            shutil.copytree(self.project_root / "shared", shared_dir)
        else:
            shared_dir.mkdir(exist_ok=True)
        
        print("✅ Build directory prepared")
    
    def create_launcher_scripts(self):
        """Create launcher scripts for the application"""
        print("📜 Creating launcher scripts...")
        
        app_dir = self.build_dir / "app"
        
        # Create Windows batch file launcher
        launcher_bat = app_dir / "launch_kerberos.bat"
        with open(launcher_bat, 'w', encoding='utf-8') as f:
            f.write(f"""@echo off
title {PRODUCT_NAME}
echo Starting {PRODUCT_NAME}...
echo Author: {MANUFACTURER}
echo {COPYRIGHT}
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH
    echo Please install Python 3.8 or later
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Node.js is not installed or not in PATH
    echo Please install Node.js 14 or later
    pause
    exit /b 1
)

REM Install Python dependencies
echo Installing Python dependencies...
cd backend
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Failed to install Python dependencies
    pause
    exit /b 1
)

REM Install Node.js dependencies
echo Installing Node.js dependencies...
cd ../frontend
npm install
if %errorlevel% neq 0 (
    echo Failed to install Node.js dependencies
    pause
    exit /b 1
)

REM Start the backend server
echo Starting backend server...
cd ../backend
start "Kerberos Backend" python app.py

REM Wait a moment for backend to start
timeout /t 3 /nobreak >nul

REM Start the frontend (React Native)
echo Starting React Native frontend...
cd ../frontend
start "Kerberos Frontend" npm start

echo.
echo {PRODUCT_NAME} is starting...
echo Backend: http://localhost:8000
echo Frontend: Follow React Native CLI instructions
echo.
echo Press any key to continue...
pause >nul
""")
        
        # Create PowerShell launcher
        launcher_ps1 = app_dir / "launch_kerberos.ps1"
        with open(launcher_ps1, 'w', encoding='utf-8') as f:
            f.write(f"""# {PRODUCT_NAME} PowerShell Launcher
# Author: {MANUFACTURER}
# {COPYRIGHT}

Write-Host "{PRODUCT_NAME}" -ForegroundColor Green
Write-Host "Author: {MANUFACTURER}" -ForegroundColor Cyan
Write-Host "{COPYRIGHT}" -ForegroundColor Yellow
Write-Host ""

# Check prerequisites
try {{
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
}} catch {{
    Write-Host "❌ Python not found. Please install Python 3.8 or later." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}}

try {{
    $nodeVersion = node --version 2>&1
    Write-Host "✅ Node.js found: $nodeVersion" -ForegroundColor Green
}} catch {{
    Write-Host "❌ Node.js not found. Please install Node.js 14 or later." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}}

# Install dependencies and start services
Write-Host "🔧 Installing dependencies..." -ForegroundColor Yellow

Set-Location "backend"
python -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {{
    Write-Host "❌ Failed to install Python dependencies" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}}

Set-Location "../frontend"
npm install
if ($LASTEXITCODE -ne 0) {{
    Write-Host "❌ Failed to install Node.js dependencies" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}}

Write-Host "🚀 Starting services..." -ForegroundColor Green

# Start backend
Set-Location "../backend"
Start-Process -FilePath "python" -ArgumentList "app.py" -WindowStyle Normal

Start-Sleep -Seconds 3

# Start frontend
Set-Location "../frontend"
Start-Process -FilePath "npm" -ArgumentList "start" -WindowStyle Normal

Write-Host ""
Write-Host "✅ {PRODUCT_NAME} is starting!" -ForegroundColor Green
Write-Host "🌐 Backend: http://localhost:8000" -ForegroundColor Cyan
Write-Host "📱 Frontend: Follow React Native CLI instructions" -ForegroundColor Cyan
Write-Host ""
Read-Host "Press Enter to continue"
""")
        
        print("✅ Launcher scripts created")
    
    def create_wix_config(self):
        """Create WiX configuration file for MSI generation"""
        print("🛠️ Creating WiX configuration...")
        
        wix_file = self.installer_dir / "kerberos_installer.wxs"
        
        with open(wix_file, 'w', encoding='utf-8') as f:
            f.write(f"""<?xml version="1.0" encoding="UTF-8"?>
<Wix xmlns="http://schemas.microsoft.com/wix/2006/wi">
    <Product Id="*" 
             Name="{PRODUCT_NAME}" 
             Language="1033" 
             Version="{PRODUCT_VERSION}" 
             Manufacturer="{MANUFACTURER}" 
             UpgradeCode="{{12345678-1234-1234-1234-123456789012}}">
        
        <Package InstallerVersion="200" 
                 Compressed="yes" 
                 InstallScope="perMachine"
                 Description="{DESCRIPTION}"
                 Comments="{COPYRIGHT}" />
        
        <MajorUpgrade DowngradeErrorMessage="A newer version of {PRODUCT_NAME} is already installed." />
        <MediaTemplate EmbedCab="yes" />
        
        <Feature Id="ProductFeature" Title="{PRODUCT_NAME}" Level="1">
            <ComponentGroupRef Id="ProductComponents" />
            <ComponentRef Id="DesktopShortcut" />
            <ComponentRef Id="StartMenuShortcut" />
        </Feature>
        
        <!-- Directory structure -->
        <Directory Id="TARGETDIR" Name="SourceDir">
            <Directory Id="ProgramFilesFolder">
                <Directory Id="INSTALLFOLDER" Name="KerberosProtocol" />
            </Directory>
            <Directory Id="ProgramMenuFolder">
                <Directory Id="ApplicationProgramsFolder" Name="{PRODUCT_NAME}" />
            </Directory>
            <Directory Id="DesktopFolder" Name="Desktop" />
        </Directory>
        
        <!-- Components -->
        <ComponentGroup Id="ProductComponents" Directory="INSTALLFOLDER">
            <!-- Main application files -->
            <Component Id="MainExecutable" Guid="{{11111111-1111-1111-1111-111111111111}}">
                <File Id="LauncherBat" Source="build\\app\\launch_kerberos.bat" KeyPath="yes" />
                <File Id="LauncherPs1" Source="build\\app\\launch_kerberos.ps1" />
            </Component>
            
            <!-- Backend files -->
            <Component Id="BackendFiles" Guid="{{22222222-2222-2222-2222-222222222222}}">
                <File Id="AppPy" Source="build\\app\\backend\\app.py" KeyPath="yes" />
                <File Id="RequirementsTxt" Source="build\\app\\backend\\requirements.txt" />
                <File Id="EnvExample" Source="build\\app\\backend\\.env.example" />
            </Component>
            
            <!-- Frontend files -->
            <Component Id="FrontendFiles" Guid="{{33333333-3333-3333-3333-333333333333}}">
                <File Id="AppTsx" Source="build\\app\\frontend\\App.tsx" KeyPath="yes" />
                <File Id="PackageJson" Source="build\\app\\frontend\\package.json" />
                <File Id="AppJson" Source="build\\app\\frontend\\app.json" />
            </Component>
        </ComponentGroup>
        
        <!-- Desktop shortcut -->
        <Component Id="DesktopShortcut" Directory="DesktopFolder" Guid="{{44444444-4444-4444-4444-444444444444}}">
            <Shortcut Id="DesktopShortcut"
                      Name="{PRODUCT_NAME}"
                      Description="{DESCRIPTION}"
                      Target="[INSTALLFOLDER]launch_kerberos.bat"
                      WorkingDirectory="INSTALLFOLDER"
                      Icon="KerberosIcon" />
            <RemoveFolder Id="DesktopFolder" On="uninstall" />
            <RegistryValue Root="HKCU" Key="Software\\{MANUFACTURER}\\{PRODUCT_NAME}" 
                          Name="DesktopShortcut" Type="integer" Value="1" KeyPath="yes" />
        </Component>
        
        <!-- Start menu shortcut -->
        <Component Id="StartMenuShortcut" Directory="ApplicationProgramsFolder" Guid="{{55555555-5555-5555-5555-555555555555}}">
            <Shortcut Id="StartMenuShortcut"
                      Name="{PRODUCT_NAME}"
                      Description="{DESCRIPTION}"
                      Target="[INSTALLFOLDER]launch_kerberos.bat"
                      WorkingDirectory="INSTALLFOLDER"
                      Icon="KerberosIcon" />
            <RemoveFolder Id="ApplicationProgramsFolder" On="uninstall" />
            <RegistryValue Root="HKCU" Key="Software\\{MANUFACTURER}\\{PRODUCT_NAME}" 
                          Name="StartMenuShortcut" Type="integer" Value="1" KeyPath="yes" />
        </Component>
        
        <!-- Icon -->
        <Icon Id="KerberosIcon" SourceFile="kerberos_icon.ico" />
        
        <!-- Registry entries -->
        <Component Id="RegistryEntries" Directory="INSTALLFOLDER" Guid="{{66666666-6666-6666-6666-666666666666}}">
            <RegistryKey Root="HKLM" Key="Software\\{MANUFACTURER}\\{PRODUCT_NAME}">
                <RegistryValue Name="InstallPath" Type="string" Value="[INSTALLFOLDER]" />
                <RegistryValue Name="Version" Type="string" Value="{PRODUCT_VERSION}" />
                <RegistryValue Name="Copyright" Type="string" Value="{COPYRIGHT}" />
            </RegistryKey>
        </Component>
        
    </Product>
</Wix>""")
        
        print("✅ WiX configuration created")
    
    def create_icon(self):
        """Create application icon"""
        print("🎨 Creating application icon...")
        
        # For this demo, we'll create a simple text file as placeholder
        # In a real implementation, you'd use an actual .ico file
        icon_file = self.installer_dir / "kerberos_icon.ico"
        
        # Create a placeholder icon file
        with open(icon_file, 'w', encoding='utf-8') as f:
            f.write("# Placeholder for Kerberos Protocol icon\\n")
            f.write("# Replace with actual .ico file\\n")
        
        print("✅ Icon placeholder created")
    
    def build_msi(self):
        """Build the MSI installer using WiX"""
        print("🔥 Building MSI installer...")
        
        # Create output directory
        self.output_dir.mkdir(exist_ok=True)
        
        wix_file = self.installer_dir / "kerberos_installer.wxs"
        wixobj_file = self.installer_dir / "kerberos_installer.wixobj"
        msi_file = self.output_dir / f"KerberosProtocol_v{PRODUCT_VERSION}.msi"
        
        try:
            # Note: This requires WiX Toolset to be installed
            # For this demo, we'll create a batch file that shows the commands
            
            build_script = self.installer_dir / "build_msi.bat"
            with open(build_script, 'w', encoding='utf-8') as f:
                f.write(f"""@echo off
echo Building {PRODUCT_NAME} MSI Installer
echo Author: {MANUFACTURER}
echo {COPYRIGHT}
echo.

REM Check if WiX is installed
where candle.exe >nul 2>&1
if %errorlevel% neq 0 (
    echo WiX Toolset not found in PATH
    echo Please install WiX Toolset v3.11 or later
    echo Download from: https://wixtoolset.org/releases/
    pause
    exit /b 1
)

echo Compiling WiX source...
candle.exe "{wix_file}" -out "{wixobj_file}"
if %errorlevel% neq 0 (
    echo Failed to compile WiX source
    pause
    exit /b 1
)

echo Linking MSI package...
light.exe "{wixobj_file}" -out "{msi_file}"
if %errorlevel% neq 0 (
    echo Failed to link MSI package
    pause
    exit /b 1
)

echo.
echo ✅ MSI installer created successfully!
echo 📦 Location: {msi_file}
echo.
pause
""")
            
            print(f"✅ Build script created: {build_script}")
            print(f"📦 Run the build script to create: {msi_file}")
            
        except Exception as e:
            print(f"❌ Error building MSI: {str(e)}")
    
    def create_installer_info(self):
        """Create installer information file"""
        print("📋 Creating installer information...")
        
        # Create output directory if it doesn't exist
        self.output_dir.mkdir(exist_ok=True)
        
        info_file = self.output_dir / "installer_info.json"
        
        info = {
            "product_name": PRODUCT_NAME,
            "version": PRODUCT_VERSION,
            "manufacturer": MANUFACTURER,
            "copyright": COPYRIGHT,
            "description": DESCRIPTION,
            "install_directory": INSTALL_DIR,
            "desktop_shortcut": DESKTOP_SHORTCUT,
            "start_menu_shortcut": START_MENU_SHORTCUT,
            "build_date": datetime.now().isoformat(),
            "requirements": {
                "python": "3.8+",
                "nodejs": "14+",
                "operating_system": "Windows 10/11"
            },
            "features": [
                "Three-headed Kerberos authentication",
                "React Native mobile frontend", 
                "Python Flask backend",
                "Claude AI integration",
                "Pinecone vector database",
                "Desktop and Start menu shortcuts",
                "Automated dependency installation"
            ]
        }
        
        with open(info_file, 'w', encoding='utf-8') as f:
            json.dump(info, f, indent=2)
        
        print("✅ Installer information created")
    
    def build(self):
        """Build the complete installer package"""
        print(f"""
🐕‍🦺 {PRODUCT_NAME} MSI Installer Builder
Author: {MANUFACTURER}
{COPYRIGHT}
=====================================
""")
        
        try:
            self.prepare_build_directory()
            self.create_launcher_scripts()
            self.create_wix_config()
            self.create_icon()
            self.create_installer_info()
            self.build_msi()
            
            print(f"""
✅ Installer build process completed!

📦 Output files:
   - MSI Installer: {self.output_dir}/KerberosProtocol_v{PRODUCT_VERSION}.msi
   - Build Script: {self.installer_dir}/build_msi.bat
   - Info File: {self.output_dir}/installer_info.json

🔧 To complete the build:
   1. Install WiX Toolset v3.11+ from https://wixtoolset.org/releases/
   2. Run the build_msi.bat script
   3. The MSI installer will be created in the output directory

🎯 Installation Features:
   ✅ Desktop shortcut creation
   ✅ Start menu shortcut
   ✅ Registry entries with copyright info
   ✅ Automated launcher scripts
   ✅ Complete application package
""")
            
        except Exception as e:
            print(f"❌ Build failed: {str(e)}")
            return False
        
        return True

if __name__ == "__main__":
    builder = MSIBuilder()
    builder.build()
