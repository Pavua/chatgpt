#!/bin/bash
# Build and package the SwiftUI macOS client as a .app zip
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT/swiftui"

# Build release binary
swift build -c release
BIN=".build/release/UserbotApp"

APP_DIR="dist/UserbotApp.app/Contents/MacOS"
mkdir -p "$APP_DIR"
cp "$BIN" "$APP_DIR/"

PLIST="dist/UserbotApp.app/Contents/Info.plist"
cat > "$PLIST" <<'PL'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleName</key>
    <string>UserbotApp</string>
    <key>CFBundleIdentifier</key>
    <string>com.userbot.app</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>CFBundleExecutable</key>
    <string>UserbotApp</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
</dict>
</plist>
PL

# Create zip archive
mkdir -p dist
ZIP_PATH="dist/UserbotApp.zip"
rm -f "$ZIP_PATH"
ditto -c -k --sequesterRsrc --keepParent "dist/UserbotApp.app" "$ZIP_PATH"

echo "Created $ZIP_PATH"
