# Kerberos Protocol Implementation - Portable Installer Creator
# Author: Devesh Kumar
# © 2025 Devesh Kumar. All rights reserved.

Write-Host "🐕‍🦺 Kerberos Protocol Implementation - Portable Installer Creator" -ForegroundColor Green
Write-Host "Author: Devesh Kumar" -ForegroundColor Cyan
Write-Host "© 2025 Devesh Kumar. All rights reserved." -ForegroundColor Yellow
Write-Host "===============================================" -ForegroundColor Blue
Write-Host ""

$ErrorActionPreference = "Stop"

# Configuration
$ProductName = "Kerberos Protocol Implementation"
$Version = "1.0.0"
$Author = "Devesh Kumar"
$Copyright = "© 2025 Devesh Kumar. All rights reserved."

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir
$BuildDir = Join-Path $ScriptDir "build"
$OutputDir = Join-Path $ScriptDir "output"
$PortableDir = Join-Path $OutputDir "KerberosProtocol_Portable_v$Version"

try {
    Write-Host "🔨 Creating portable installer package..." -ForegroundColor Yellow
    
    # Create output directory
    if (Test-Path $PortableDir) {
        Remove-Item $PortableDir -Recurse -Force
    }
    New-Item -ItemType Directory -Path $PortableDir -Force | Out-Null
    
    # Copy application files
    Write-Host "📁 Copying application files..." -ForegroundColor Cyan
    Copy-Item -Path "$BuildDir\app\*" -Destination $PortableDir -Recurse -Force
    
    # Create main installer script
    $InstallerScript = @"
# Kerberos Protocol Implementation Installer
# Author: $Author
# $Copyright

param(
    [switch]`$Install,
    [switch]`$Uninstall,
    [switch]`$Run,
    [string]`$InstallPath = "C:\Program Files\KerberosProtocol"
)

Write-Host "$ProductName v$Version" -ForegroundColor Green
Write-Host "Author: $Author" -ForegroundColor Cyan
Write-Host "$Copyright" -ForegroundColor Yellow
Write-Host ""

if (`$Install) {
    Write-Host "🚀 Installing $ProductName..." -ForegroundColor Green
    
    # Create installation directory
    if (-not (Test-Path `$InstallPath)) {
        New-Item -ItemType Directory -Path `$InstallPath -Force | Out-Null
    }
    
    # Copy application files
    `$SourcePath = Split-Path -Parent `$MyInvocation.MyCommand.Path
    Copy-Item -Path "`$SourcePath\*" -Destination `$InstallPath -Recurse -Force -Exclude "install.ps1"
    
    # Create desktop shortcut
    `$DesktopPath = [Environment]::GetFolderPath("Desktop")
    `$ShortcutPath = Join-Path `$DesktopPath "$ProductName.lnk"
    `$WshShell = New-Object -comObject WScript.Shell
    `$Shortcut = `$WshShell.CreateShortcut(`$ShortcutPath)
    `$Shortcut.TargetPath = "powershell.exe"
    `$Shortcut.Arguments = "-ExecutionPolicy Bypass -File `"`$InstallPath\launch_kerberos.ps1`""
    `$Shortcut.WorkingDirectory = `$InstallPath
    `$Shortcut.IconLocation = "`$InstallPath\kerberos_icon.ico"
    `$Shortcut.Description = "Launch $ProductName"
    `$Shortcut.Save()
    
    # Create Start Menu shortcut
    `$StartMenuPath = [Environment]::GetFolderPath("StartMenu")
    `$StartMenuShortcut = Join-Path `$StartMenuPath "Programs\$ProductName.lnk"
    `$StartShortcut = `$WshShell.CreateShortcut(`$StartMenuShortcut)
    `$StartShortcut.TargetPath = "powershell.exe"
    `$StartShortcut.Arguments = "-ExecutionPolicy Bypass -File `"`$InstallPath\launch_kerberos.ps1`""
    `$StartShortcut.WorkingDirectory = `$InstallPath
    `$StartShortcut.IconLocation = "`$InstallPath\kerberos_icon.ico"
    `$StartShortcut.Description = "Launch $ProductName"
    `$StartShortcut.Save()
    
    # Add to Programs and Features
    `$RegPath = "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\KerberosProtocol"
    New-Item -Path `$RegPath -Force | Out-Null
    Set-ItemProperty -Path `$RegPath -Name "DisplayName" -Value "$ProductName"
    Set-ItemProperty -Path `$RegPath -Name "DisplayVersion" -Value "$Version"
    Set-ItemProperty -Path `$RegPath -Name "Publisher" -Value "$Author"
    Set-ItemProperty -Path `$RegPath -Name "InstallLocation" -Value `$InstallPath
    Set-ItemProperty -Path `$RegPath -Name "UninstallString" -Value "powershell.exe -ExecutionPolicy Bypass -File `"`$InstallPath\install.ps1`" -Uninstall"
    Set-ItemProperty -Path `$RegPath -Name "DisplayIcon" -Value "`$InstallPath\kerberos_icon.ico"
    
    Write-Host "✅ Installation completed!" -ForegroundColor Green
    Write-Host "📍 Installed to: `$InstallPath" -ForegroundColor Cyan
    Write-Host "🖥️ Desktop shortcut created" -ForegroundColor Cyan
    Write-Host "📋 Start menu shortcut created" -ForegroundColor Cyan
}
elseif (`$Uninstall) {
    Write-Host "🗑️ Uninstalling $ProductName..." -ForegroundColor Yellow
    
    # Remove shortcuts
    `$DesktopShortcut = Join-Path ([Environment]::GetFolderPath("Desktop")) "$ProductName.lnk"
    if (Test-Path `$DesktopShortcut) { Remove-Item `$DesktopShortcut -Force }
    
    `$StartMenuShortcut = Join-Path ([Environment]::GetFolderPath("StartMenu")) "Programs\$ProductName.lnk"
    if (Test-Path `$StartMenuShortcut) { Remove-Item `$StartMenuShortcut -Force }
    
    # Remove registry entries
    `$RegPath = "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\KerberosProtocol"
    if (Test-Path `$RegPath) { Remove-Item `$RegPath -Force }
    
    # Remove installation directory
    if (Test-Path `$InstallPath) {
        Remove-Item `$InstallPath -Recurse -Force
    }
    
    Write-Host "✅ Uninstallation completed!" -ForegroundColor Green
}
elseif (`$Run) {
    Write-Host "🚀 Starting $ProductName..." -ForegroundColor Green
    & "`$PSScriptRoot\launch_kerberos.ps1"
}
else {
    Write-Host "Usage:" -ForegroundColor Yellow
    Write-Host "  .\install.ps1 -Install                    # Install the application" -ForegroundColor White
    Write-Host "  .\install.ps1 -Install -InstallPath `"C:\MyPath`"   # Install to custom path" -ForegroundColor White
    Write-Host "  .\install.ps1 -Uninstall                  # Uninstall the application" -ForegroundColor White
    Write-Host "  .\install.ps1 -Run                        # Run without installing" -ForegroundColor White
    Write-Host ""
    Write-Host "For portable use, just run: .\launch_kerberos.ps1" -ForegroundColor Cyan
}
"@
    
    # Save installer script
    $InstallerScript | Out-File -FilePath (Join-Path $PortableDir "install.ps1") -Encoding UTF8 -Force
    
    # Create README for the installer
    $ReadmeContent = @"
# $ProductName v$Version
Author: $Author
$Copyright

## Installation Options

### Option 1: Full Installation (Recommended)
1. Right-click on `install.ps1` and select "Run with PowerShell"
2. Choose option "-Install" when prompted
3. The application will be installed to `C:\Program Files\KerberosProtocol`
4. Desktop and Start Menu shortcuts will be created

### Option 2: Custom Installation Path
1. Open PowerShell as Administrator
2. Navigate to this folder
3. Run: `.\install.ps1 -Install -InstallPath "C:\YourCustomPath"`

### Option 3: Portable Mode (No Installation)
1. Simply run `launch_kerberos.ps1` directly from this folder
2. No system changes will be made

## Requirements
- Windows 10/11
- Python 3.8 or later
- Node.js 14 or later

## Features
- Three-headed Kerberos authentication system
- React Native cross-platform frontend
- Python Flask backend with REST API
- Claude AI integration for threat detection
- Pinecone vector database for behavior analysis
- AES-256 encryption
- JWT token authentication
- Desktop and Start Menu shortcuts
- Automatic dependency installation

## Uninstallation
Run: `.\install.ps1 -Uninstall`

## Support
For support and documentation, visit the docs folder.

## Copyright
$Copyright
All rights reserved.
"@
    
    $ReadmeContent | Out-File -FilePath (Join-Path $PortableDir "README.txt") -Encoding UTF8 -Force
    
    # Create a batch launcher for easier access
    $BatchLauncher = @"
@echo off
echo $ProductName v$Version
echo Author: $Author
echo $Copyright
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
    goto :start
)

pause
"@
    
    $BatchLauncher | Out-File -FilePath (Join-Path $PortableDir "Kerberos_Launcher.bat") -Encoding ASCII -Force
    
    # Create final package info
    $PackageInfo = @{
        product_name = $ProductName
        version = $Version
        author = $Author
        copyright = $Copyright
        package_type = "Portable Installer"
        build_date = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
        installation_methods = @(
            "Full installation with registry entries and shortcuts",
            "Portable mode - run directly without installation",
            "Custom path installation"
        )
        features = @(
            "Desktop and Start Menu shortcuts",
            "Registry integration for Programs & Features",
            "Automatic dependency checking",
            "One-click launcher",
            "Clean uninstallation"
        )
    }
    
    $PackageInfo | ConvertTo-Json -Depth 3 | Out-File -FilePath (Join-Path $PortableDir "package_info.json") -Encoding UTF8 -Force
    
    Write-Host "✅ Portable installer package created successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📦 Package Location: $PortableDir" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "📋 Package Contents:" -ForegroundColor Yellow
    Get-ChildItem $PortableDir | ForEach-Object {
        if ($_.PSIsContainer) {
            Write-Host "   📁 $($_.Name)/" -ForegroundColor Blue
        } else {
            Write-Host "   📄 $($_.Name)" -ForegroundColor White
        }
    }
    
    Write-Host ""
    Write-Host "🚀 To use the installer:" -ForegroundColor Green
    Write-Host "   1. Copy the entire folder to the target computer" -ForegroundColor White
    Write-Host "   2. Run 'Kerberos_Launcher.bat' for guided installation" -ForegroundColor White
    Write-Host "   3. Or run 'install.ps1 -Install' for direct installation" -ForegroundColor White
    Write-Host "   4. Or run 'launch_kerberos.ps1' for portable mode" -ForegroundColor White
    
} catch {
    Write-Host "❌ Error creating portable installer: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🎉 Portable installer creation completed!" -ForegroundColor Green
