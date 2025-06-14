@echo off
REM === Python requirements for Custom Linux Installer ===

REM pip update
python -m pip install --upgrade pip

python -m pip install tk

echo.
echo All required Python modules are installed!
pause