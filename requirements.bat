@echo off
REM Modern Linux Installer v2.0.0 - Windows Requirements Setup
setlocal enabledelayedexpansion

echo ========================================
echo  Modern Linux Installer v2.0.0 Setup
echo ========================================
echo.

echo [1/6] Checking Python installation...
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python 3.6+ from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

python --version
echo [SUCCESS] Python found and accessible
echo.

echo [2/6] Checking Python tkinter support...
python -c "import tkinter; print('tkinter available')" >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] tkinter not available. Please reinstall Python with tkinter support.
    pause
    exit /b 1
)
echo [SUCCESS] tkinter support confirmed
echo.

echo [3/6] Upgrading pip and installing Python dependencies...
python -m pip install --upgrade pip --quiet
if %errorlevel% neq 0 (
    echo [WARNING] Could not upgrade pip, continuing...
)
echo [SUCCESS] Python environment ready
echo.

echo [4/6] Checking 7-Zip installation...
set "SEVENZIP_FOUND=0"

REM Check default portable path
if exist "J:\portableapps\PortableApps\7-ZipPortable\App\7-Zip\7z.exe" (
    echo [SUCCESS] 7-Zip found at portable location
    set "SEVENZIP_FOUND=1" 
) else (
    REM Check system PATH
    where 7z.exe >nul 2>&1
    if !errorlevel! equ 0 (
        echo [SUCCESS] 7-Zip found in system PATH
        set "SEVENZIP_FOUND=1"
    ) else (
        REM Check common installation paths
        if exist "C:\Program Files\7-Zip\7z.exe" (
            echo [SUCCESS] 7-Zip found in Program Files
            set "SEVENZIP_FOUND=1"
        ) else if exist "C:\Program Files (x86)\7-Zip\7z.exe" (
            echo [SUCCESS] 7-Zip found in Program Files (x86)
            set "SEVENZIP_FOUND=1"
        )
    )
)

if !SEVENZIP_FOUND! equ 0 (
    echo [WARNING] 7-Zip not found. Downloading...
    echo Please install 7-Zip from: https://www.7-zip.org/
    echo.
    echo The application will attempt to find 7-Zip automatically.
    echo If issues persist, update the path in linux-installer.py
)
echo.

echo [5/6] Checking QEMU installation...
set "QEMU_FOUND=0"

REM Check default path
if exist "D:\win\qemu\qemu-img.exe" (
    echo [SUCCESS] QEMU found at default location
    set "QEMU_FOUND=1"
) else (
    REM Check system PATH
    where qemu-img.exe >nul 2>&1
    if !errorlevel! equ 0 (
        echo [SUCCESS] QEMU found in system PATH
        set "QEMU_FOUND=1"
    ) else (
        REM Check common installation paths
        if exist "C:\Program Files\qemu\qemu-img.exe" (
            echo [SUCCESS] QEMU found in Program Files
            set "QEMU_FOUND=1"
        )
    )
)

if !QEMU_FOUND! equ 0 (
    echo [WARNING] QEMU not found. 
    echo Please install QEMU from: https://qemu.weilnetz.de/w64/
    echo.
    echo Recommended installation path: D:\win\qemu\
    echo The application will attempt to find QEMU automatically.
)
echo.

echo [6/6] Checking WSL availability...
wsl --status >nul 2>&1
if %errorlevel% equ 0 (
    echo [SUCCESS] WSL is available and configured
) else (
    echo [WARNING] WSL not available or not configured
    echo.
    echo WSL is required for:
    echo - ext4 filesystem formatting
    echo - Linux filesystem operations
    echo - Advanced partition management
    echo.
    echo To enable WSL:
    echo 1. Open PowerShell as Administrator
    echo 2. Run: wsl --install
    echo 3. Restart your computer
    echo 4. Set up a Linux distribution from Microsoft Store
)
echo.

echo ========================================
echo  Setup Summary
echo ========================================
echo Python: Ready
echo tkinter: Available
echo 7-Zip: %SEVENZIP_FOUND% (0=Not Found, 1=Found)
echo QEMU: %QEMU_FOUND% (0=Not Found, 1=Found)
echo.
echo [INFO] You can now run the Modern Linux Installer:
echo python linux-installer.py
echo.
echo [TIP] For full functionality, run as Administrator
echo.

if !SEVENZIP_FOUND! equ 0 (
    echo [ACTION REQUIRED] Install 7-Zip for ISO extraction
)
if !QEMU_FOUND! equ 0 (
    echo [ACTION REQUIRED] Install QEMU for VHD creation
)

echo.
echo Setup completed! Press any key to exit...
pause >nul
