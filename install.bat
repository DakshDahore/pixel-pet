@echo off
title Pixel Pet Installer
echo =========================================
echo    Pixel Pet Setup for Windows
echo =========================================

python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo Installation complete! Double click run.bat to launch your pet!
pause

