USB Stealth Screenshot Capture Tool
====================================

This USB drive will automatically capture screenshots when inserted into a computer (Windows-focused).

How it works:
1. Insert USB into target computer
2. autorun.inf -> lunch.bat will run (if AutoRun is enabled)
3. lunch.bat runs stealth_capture.py, which delegates to usb.py
4. usb.py waits briefly, then captures screenshots every 10 seconds (configurable in code)
5. Screenshots are saved to a hidden folder on the USB: .system_cache

Files included (canonical names in this repo):
- autorun.inf        : Windows AutoRun configuration (added to match expected filename)
- lunch.bat          : Main launcher script (batch file)
- stealth_capture.py : Wrapper that imports usb.py and calls usb.main()
- usb.py             : Main Python screenshot capture utility (contains main())
- Plug.py            : Alternate/older implementation with extended features

Requirements:
- Windows computer (AutoRun may be disabled on modern systems)
- Python 3.6+ (or portable Python included)
- Optional internet connection for auto-install of some packages

Notes:
- Some older docs in this repo referenced names like `launcher.bat` or `stealth_capture.py` before it existed; those references have been standardized.
- `installer.bat` is not included in this repository. If you need an installer batch, create one that installs the Python runtime and required packages.

Legal: Use only on computers you own or have permission to monitor.
