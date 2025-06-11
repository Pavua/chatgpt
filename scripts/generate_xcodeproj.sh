#!/bin/bash
# Generate an Xcode project for the SwiftUI client
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT/swiftui"
# Use Swift Package Manager if the command is available
if swift package --help | grep -q generate-xcodeproj; then
    swift package generate-xcodeproj
    echo "Xcode project generated at $(pwd)/UserbotApp.xcodeproj"
else
    echo "'swift package generate-xcodeproj' not supported. Open Package.swift directly in Xcode." >&2
fi
