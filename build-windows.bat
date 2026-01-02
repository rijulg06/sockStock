@echo off
REM Build script for SockStock distribution (Windows)

echo Building SockStock distribution for Windows...

REM Clean previous builds
echo Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist distribution rmdir /s /q distribution
if exist sockstock.spec del sockstock.spec
if exist SockStock-v1.0-Windows.zip del SockStock-v1.0-Windows.zip

REM Build executable
echo Building standalone executable...
pyinstaller --onefile --name sockstock --clean main.py

if %ERRORLEVEL% NEQ 0 (
    echo Build failed!
    exit /b 1
)

REM Create distribution folder
echo Creating distribution package...
mkdir distribution

REM Copy executable
copy dist\sockstock.exe distribution\

REM Create README
(
echo ===============================================================================
echo     SOCK FACTORY INVENTORY MANAGEMENT SYSTEM
echo     Version 1.0
echo     Roopa Enterprises
echo ===============================================================================
echo.
echo QUICK START
echo -----------
echo 1. Double-click "sockstock.exe" to run the program
echo.
echo 2. The program will start automatically - no installation needed!
echo.
echo 3. Your inventory data is saved in "inventory.db" in this folder
echo.
echo.
echo FEATURES
echo --------
echo - Add new stock ^(automatically placed in "Order" stage^)
echo - Move stock between production stages
echo - Undo last operation
echo - View all inventory
echo - View summary by stage
echo - Filter stock by Quality, Color, or Size
echo.
echo.
echo PRODUCTION STAGES
echo -----------------
echo Order -^> Raw Made -^> Sent for Press -^> Ready Stock -^> Dispatch
echo.
echo.
echo TROUBLESHOOTING
echo ---------------
echo Problem: "Windows protected your PC" warning
echo Solution: Click "More info" then "Run anyway"
echo.
echo Problem: Program won't start
echo Solution: Right-click sockstock.exe -^> Properties -^> Unblock
echo.
echo ===============================================================================
echo © 2025 Roopa Enterprises
echo ===============================================================================
) > distribution\README.txt

REM Create ZIP
echo Creating ZIP archive...
cd distribution
powershell -Command "Compress-Archive -Path * -DestinationPath ..\SockStock-v1.0-Windows.zip -Force"
cd ..

echo.
echo ========================================
echo Build complete!
echo ========================================
echo Distribution package: SockStock-v1.0-Windows.zip
dir SockStock-v1.0-Windows.zip

echo.
echo Distribution folder contents:
dir distribution
