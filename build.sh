#!/bin/bash
# Quick build script for SockStock distribution

echo "🔨 Building SockStock distribution..."

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build dist distribution sockstock.spec *.zip

# Build executable
echo "Building standalone executable..."
pyinstaller --onefile --name sockstock --clean main.py

if [ $? -ne 0 ]; then
    echo "❌ Build failed!"
    exit 1
fi

# Create distribution folder
echo "Creating distribution package..."
mkdir -p distribution

# Copy executable
cp dist/sockstock distribution/

# Create README
cat > distribution/README.txt << 'READMEEOF'
===============================================================================
    SOCK FACTORY INVENTORY MANAGEMENT SYSTEM
    Version 1.0
    Roopa Enterprises
===============================================================================

QUICK START
-----------
1. Double-click "sockstock" to run the program
   (Or open Terminal, navigate to this folder, and type: ./sockstock)

2. The program will start automatically - no installation needed!

3. Your inventory data is saved in "inventory.db" in this folder


FEATURES
--------
✓ Add new stock (automatically placed in "Order" stage)
✓ Move stock between production stages
✓ Undo last operation
✓ View all inventory
✓ View summary by stage
✓ Filter stock by Quality, Color, or Size


PRODUCTION STAGES
-----------------
Order → Raw Made → Sent for Press → Ready Stock → Dispatch


TROUBLESHOOTING
---------------
Problem: "Cannot be opened because it is from an unidentified developer"
Solution: Right-click → Open → Open

Problem: Permission denied
Solution: chmod +x sockstock

===============================================================================
© 2025 Roopa Enterprises
===============================================================================
READMEEOF

# Make executable
chmod +x distribution/sockstock

# Create ZIP
echo "Creating ZIP archive..."
cd distribution
zip -r ../SockStock-v1.0-macOS.zip . > /dev/null
cd ..

echo "✅ Build complete!"
echo "📦 Distribution package: SockStock-v1.0-macOS.zip"
ls -lh SockStock-v1.0-macOS.zip

echo ""
echo "Distribution folder contents:"
ls -lh distribution/
