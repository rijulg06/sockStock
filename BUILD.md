# Building SockStock Executable

This guide explains how to build standalone executables for the Sock Factory Inventory Management System.

## Important Note About Cross-Platform Building

**PyInstaller creates executables for the platform it runs on:**
- Building on Windows → Creates `.exe` for Windows
- Building on macOS → Creates macOS executable
- Building on Linux → Creates Linux executable

**You cannot create a Windows .exe on macOS!** You need to build on a Windows machine.

## Prerequisites

### On Windows

1. **Install Python 3.8 or higher**
   - Download from [python.org](https://www.python.org/downloads/)
   - During installation, check "Add Python to PATH"

2. **Install dependencies**
   ```cmd
   pip install -r requirements.txt
   ```

### On macOS/Linux

1. **Python is usually pre-installed**, or install via:
   ```bash
   # macOS
   brew install python3

   # Linux
   sudo apt install python3 python3-pip
   ```

2. **Install dependencies**
   ```bash
   pip3 install -r requirements.txt
   ```

## Building the Executable

### Windows

1. Open Command Prompt in the project directory
2. Run the build script:
   ```cmd
   build-windows.bat
   ```

3. The build creates:
   - `SockStock-v1.0-Windows.zip` - Distribution package
   - `distribution/` folder with executable and README

### macOS

1. Open Terminal in the project directory
2. Make the script executable:
   ```bash
   chmod +x build.sh
   ```
3. Run the build script:
   ```bash
   ./build.sh
   ```

4. The build creates:
   - `SockStock-v1.0-macOS.zip` - Distribution package
   - `distribution/` folder with executable and README

### Linux

Use the same script as macOS:
```bash
chmod +x build.sh
./build.sh
```

## What Gets Built

The build process:

1. **Cleans** previous build artifacts
2. **Bundles** Python interpreter + your code + dependencies into a single executable
3. **Creates** a distribution folder with:
   - The executable file (`sockstock.exe` or `sockstock`)
   - README.txt with user instructions
4. **Packages** everything into a ZIP file for easy distribution

## How It Works

### PyInstaller Process

PyInstaller analyzes your Python code and:
- Identifies all imports and dependencies (including `tabulate`, `sqlite3`)
- Bundles the Python interpreter
- Creates a self-contained executable
- Users don't need Python installed to run it!

### Database Handling

The `config.py` file has special logic to detect if running as an executable:

```python
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    DB_PATH = os.path.join(os.path.dirname(sys.executable), 'inventory.db')
else:
    # Running as script
    DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'inventory.db')
```

This ensures the database file is created in the same folder as the executable, not buried in temp folders.

## Distributing Your Application

### Send to Users

1. Share the `.zip` file (e.g., `SockStock-v1.0-Windows.zip`)
2. Users extract and double-click `sockstock.exe`
3. No installation needed!

### First-Time Windows Users May See

**"Windows protected your PC" warning**
- This is normal for unsigned executables
- Users can click "More info" → "Run anyway"
- Alternative: Code-sign the executable (requires certificate, costs money)

## Troubleshooting

### Build fails with "command not found: pyinstaller"

Install dependencies:
```bash
pip install -r requirements.txt
```

### Windows: "pip is not recognized"

Python wasn't added to PATH. Either:
1. Reinstall Python with "Add to PATH" checked
2. Use full path: `C:\Python311\Scripts\pip.exe install -r requirements.txt`

### macOS: Permission denied

Make the script executable:
```bash
chmod +x build.sh
```

### Executable won't run

- Windows: Right-click → Properties → Unblock
- macOS: Right-click → Open (first time only)
- Linux: `chmod +x sockstock`

## Advanced: GitHub Actions (Optional)

To build Windows executables from macOS automatically, you can use GitHub Actions:

1. Create `.github/workflows/build.yml`
2. GitHub will build on Windows/macOS/Linux automatically
3. Download executables from the Actions tab

Would you like me to set this up?

## File Structure After Build

```
sockStock/
├── main.py                           # Source code
├── database.py
├── config.py
├── requirements.txt
├── build-windows.bat                 # Windows build script
├── build.sh                          # macOS/Linux build script
├── build/                           # Temporary build files (gitignored)
├── dist/                            # Raw executable (gitignored)
├── distribution/                    # Clean distribution folder
│   ├── sockstock.exe (or sockstock)
│   └── README.txt
└── SockStock-v1.0-Windows.zip       # Final package
```

## Testing Your Executable

### Before Distributing

1. Test on a clean Windows machine (no Python installed)
2. Try all features:
   - Add stock
   - Move stock between stages
   - View inventory
   - Filter stock
   - Undo operations
3. Verify `inventory.db` is created in the same folder
4. Close and reopen - data should persist

---

**Questions?** Check the main README.md or open an issue.
