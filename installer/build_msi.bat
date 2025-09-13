@echo off
echo Building Kerberos Protocol Implementation MSI Installer
echo Author: Devesh Kumar
echo © 2025 Devesh Kumar. All rights reserved.
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
candle.exe "C:\Users\0123975\kerberos\installer\kerberos_installer.wxs" -out "C:\Users\0123975\kerberos\installer\kerberos_installer.wixobj"
if %errorlevel% neq 0 (
    echo Failed to compile WiX source
    pause
    exit /b 1
)

echo Linking MSI package...
light.exe "C:\Users\0123975\kerberos\installer\kerberos_installer.wixobj" -out "C:\Users\0123975\kerberos\installer\output\KerberosProtocol_v1.0.0.msi"
if %errorlevel% neq 0 (
    echo Failed to link MSI package
    pause
    exit /b 1
)

echo.
echo ✅ MSI installer created successfully!
echo 📦 Location: C:\Users\0123975\kerberos\installer\output\KerberosProtocol_v1.0.0.msi
echo.
pause
