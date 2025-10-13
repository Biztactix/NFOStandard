#!/bin/bash
# Build script for NFO Standard Emby Plugin

echo "Building NFO Standard plugin for Emby..."

# Clean previous builds
dotnet clean

# Restore packages
dotnet restore

# Build in Release mode
dotnet build -c Release

echo "Build complete!"
echo "DLL location: ./bin/Release/net6.0/NFOStandard.dll"
echo ""
echo "To install:"
echo "1. Copy NFOStandard.dll to your Emby plugins folder"
echo "2. Restart Emby Server"