# Kerberos Protocol Implementation - Portable Installer Creator
# Author: Devesh Kumar
# Copyright: 2025 Devesh Kumar. All rights reserved.

Write-Host "Kerberos Protocol Implementation - Portable Installer Creator" -ForegroundColor Green
Write-Host "Author: Devesh Kumar" -ForegroundColor Cyan
Write-Host "Copyright: 2025 Devesh Kumar. All rights reserved." -ForegroundColor Yellow
Write-Host "===============================================" -ForegroundColor Blue
Write-Host ""

$ErrorActionPreference = "Stop"

# Configuration
$ProductName = "Kerberos Protocol Implementation"
$Version = "1.0.0"
$Author = "Devesh Kumar"
$Copyright = "2025 Devesh Kumar. All rights reserved."

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$BuildDir = Join-Path $ScriptDir "build"
$OutputDir = Join-Path $ScriptDir "output"
$PortableDir = Join-Path $OutputDir "KerberosProtocol_Portable_v$Version"

try {
    Write-Host "Creating portable installer package..." -ForegroundColor Yellow
    
    # Create output directory
    if (Test-Path $PortableDir) {
        Remove-Item $PortableDir -Recurse -Force
    }
    New-Item -ItemType Directory -Path $PortableDir -Force | Out-Null
    
    # Copy application files
    Write-Host "Copying application files..." -ForegroundColor Cyan
    Copy-Item -Path "$BuildDir\app\*" -Destination $PortableDir -Recurse -Force
    
    # Create main installer script
    $InstallerScript = @'
# Kerberos Protocol Implementation Installer
# Author: Devesh Kumar
# Copyright: 2025 Devesh Kumar. All rights reserved.

param(
    [switch]$Install,
    [switch]$Uninstall,
    [switch]$Run,
    [string]$InstallPath = "C:\Program Files\KerberosProtocol"
)

Write-Host "Kerberos Protocol Implementation v1.0.0" -ForegroundColor Green
Write-Host "Author: Devesh Kumar" -ForegroundColor Cyan
Write-Host "Copyright: 2025 Devesh Kumar. All rights reserved." -ForegroundColor Yellow
Write-Host ""

if ($Install) {
    Write-Host "Installing Kerberos Protocol Implementation..." -ForegroundColor Green
    
    # Create installation directory
    if (-not (Test-Path $InstallPath)) {
        New-Item -ItemType Directory -Path $InstallPath -Force | Out-Null
    }
    
    # Copy application files
    $SourcePath = Split-Path -Parent $MyInvocation.MyCommand.Path
    Copy-Item -Path "$SourcePath\*" -Destination $InstallPath -Recurse -Force -Exclude "install.ps1"
    
    # Create desktop shortcut
    $DesktopPath = [Environment]::GetFolderPath("Desktop")
    $ShortcutPath = Join-Path $DesktopPath "Kerberos Protocol Implementation.lnk"
    $WshShell = New-Object -comObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut($ShortcutPath)
    $Shortcut.TargetPath = "powershell.exe"
    $Shortcut.Arguments = "-ExecutionPolicy Bypass -File `"$InstallPath\launch_kerberos.ps1`""
    $Shortcut.WorkingDirectory = $InstallPath
    $Shortcut.Description = "Launch Kerberos Protocol Implementation"
    $Shortcut.Save()
    
    Write-Host "Installation completed!" -ForegroundColor Green
    Write-Host "Installed to: $InstallPath" -ForegroundColor Cyan
    Write-Host "Desktop shortcut created" -ForegroundColor Cyan
}
elseif ($Uninstall) {
    Write-Host "Uninstalling Kerberos Protocol Implementation..." -ForegroundColor Yellow
    
    # Remove shortcuts
    $DesktopShortcut = Join-Path ([Environment]::GetFolderPath("Desktop")) "Kerberos Protocol Implementation.lnk"
    if (Test-Path $DesktopShortcut) { Remove-Item $DesktopShortcut -Force }
    
    # Remove installation directory
    if (Test-Path $InstallPath) {
        Remove-Item $InstallPath -Recurse -Force
    }
    
    Write-Host "Uninstallation completed!" -ForegroundColor Green
}
elseif ($Run) {
    Write-Host "Starting Kerberos Protocol Implementation..." -ForegroundColor Green
    & "$PSScriptRoot\launch_kerberos.ps1"
}
else {
    Write-Host "Usage:" -ForegroundColor Yellow
    Write-Host "  .\install.ps1 -Install                    # Install the application" -ForegroundColor White
    Write-Host "  .\install.ps1 -Uninstall                  # Uninstall the application" -ForegroundColor White
    Write-Host "  .\install.ps1 -Run                        # Run without installing" -ForegroundColor White
    Write-Host ""
    Write-Host "For portable use, just run: .\launch_kerberos.ps1" -ForegroundColor Cyan
}
'@
    
    # Save installer script
    $InstallerScript | Out-File -FilePath (Join-Path $PortableDir "install.ps1") -Encoding UTF8 -Force
    
    # Create README for the installer
    $ReadmeContent = @"
Kerberos Protocol Implementation v1.0.0
Author: Devesh Kumar
Copyright: 2025 Devesh Kumar. All rights reserved.

INSTALLATION OPTIONS

Option 1: Full Installation (Recommended)
1. Right-click on install.ps1 and select "Run with PowerShell"
2. Choose option "-Install" when prompted
3. The application will be installed to C:\Program Files\KerberosProtocol
4. Desktop shortcut will be created

Option 2: Portable Mode (No Installation)
1. Simply run launch_kerberos.ps1 directly from this folder
2. No system changes will be made

REQUIREMENTS
- Windows 10/11
- Python 3.8 or later
- Node.js 14 or later

FEATURES
- Three-headed Kerberos authentication system
- React Native cross-platform frontend
- Python Flask backend with REST API
- Claude AI integration for threat detection
- Pinecone vector database for behavior analysis
- AES-256 encryption
- JWT token authentication

UNINSTALLATION
Run: .\install.ps1 -Uninstall

COPYRIGHT
Copyright 2025 Devesh Kumar. All rights reserved.
"@
    
    $ReadmeContent | Out-File -FilePath (Join-Path $PortableDir "README.txt") -Encoding UTF8 -Force
    
    # Create a batch launcher for easier access
    $BatchLauncher = @'
@echo off
echo Kerberos Protocol Implementation v1.0.0
echo Author: Devesh Kumar
echo Copyright: 2025 Devesh Kumar. All rights reserved.
echo.
echo Choose an option:
echo 1. Install (Full installation with shortcuts)
echo 2. Run portable (No installation required)
echo 3. Uninstall
echo 4. Exit
echo.
set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    powershell.exe -ExecutionPolicy Bypass -File "%~dp0install.ps1" -Install
) else if "%choice%"=="2" (
    powershell.exe -ExecutionPolicy Bypass -File "%~dp0launch_kerberos.ps1"
) else if "%choice%"=="3" (
    powershell.exe -ExecutionPolicy Bypass -File "%~dp0install.ps1" -Uninstall
) else if "%choice%"=="4" (
    exit
) else (
    echo Invalid choice. Please try again.
    pause
    cls
    goto :EOF
)

pause
'@
    
    $BatchLauncher | Out-File -FilePath (Join-Path $PortableDir "Kerberos_Launcher.bat") -Encoding ASCII -Force
    
    Write-Host "Portable installer package created successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Package Location: $PortableDir" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Package Contents:" -ForegroundColor Yellow
    Get-ChildItem $PortableDir | ForEach-Object {
        if ($_.PSIsContainer) {
            Write-Host "   Folder: $($_.Name)" -ForegroundColor Blue
        } else {
            Write-Host "   File: $($_.Name)" -ForegroundColor White
        }
    }
    
    Write-Host ""
    Write-Host "To use the installer:" -ForegroundColor Green
    Write-Host "   1. Copy the entire folder to the target computer" -ForegroundColor White
    Write-Host "   2. Run 'Kerberos_Launcher.bat' for guided installation" -ForegroundColor White
    Write-Host "   3. Or run 'install.ps1 -Install' for direct installation" -ForegroundColor White
    Write-Host "   4. Or run 'launch_kerberos.ps1' for portable mode" -ForegroundColor White
    
} catch {
    Write-Host "Error creating portable installer: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Portable installer creation completed!" -ForegroundColor Green
