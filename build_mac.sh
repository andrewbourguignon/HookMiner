#!/bin/bash
set -e

echo "Building HookMiner macOS application..."

# Create a clean build environment
rm -rf build dist
mkdir -p build/dmg

# Bundle the application using PyInstaller
# We use desktop.py as the entry point
# --windowed removes the console window
# --add-data adds the templates and static folders
pyinstaller --noconfirm --log-level=WARN \
    --windowed \
    --name="HookMiner" \
    --add-data="templates:templates" \
    --add-data="static:static" \
    desktop.py

echo "PyInstaller build complete!"
echo "App bundle is in: dist/HookMiner.app"

# Optional: You can create a DMG using hdiutil
echo "Creating DMG..."
hdiutil create dist/HookMiner.dmg -volname "HookMiner Installer" -srcfolder dist/HookMiner.app -ov

echo "Build Process Finished Successfully!"
echo "Your application DMG is available at: dist/HookMiner.dmg"
