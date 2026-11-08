#!/usr/bin/env bash

# Pixel Pet - One-Click Installer for Linux & macOS
cd "$(dirname "$0")"

echo "========================================="
echo "   🐱 Pixel Pet Setup & Installation"
echo "========================================="

python3 -m pip install --upgrade pip
pip install -r requirements.txt

chmod +x run.sh
chmod +x web_server.py

echo ""
echo "Installation complete!"
echo "To run your pet, execute: ./run.sh or python3 main.py"
