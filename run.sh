#!/usr/bin/env bash

# Pixel Pet - One-Click Launcher for Linux & macOS
cd "$(dirname "$0")"

echo "========================================="
echo "   🐱 Pixel Pet Desktop Guardian"
echo "========================================="

# Check Python3
if ! command -v python3 &>/dev/null; then
    echo "Error: python3 is not installed on this system!"
    exit 1
fi

# Install requirements if pillow missing
python3 -c "import PIL" 2>/dev/null || {
    echo "Installing required dependencies..."
    pip install -r requirements.txt --quiet
}

# Launch desktop pet in background without blocking terminal
echo "Launching Pixel Pet in background..."
nohup python3 main.py >/dev/null 2>&1 &

echo "Pixel Pet is now running on your desktop!"

