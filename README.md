# PlugOn

USB stealth screenshot capture utility (Windows-focused). Use only with explicit permission — this tool can capture screenshots and monitor activity on a host system.

## Quickstart

1) Install dependencies (recommended):

```bash
python -m pip install --user pillow pyautogui pywin32 requests
# On Linux you may also need:
sudo apt update && sudo apt install -y scrot python3-tk python3-dev
```

2) From the repository root run the launcher or Python script:

```bash
# Run the wrapper expected by lunch.bat
python stealth_capture.py
# Or run the core script directly
python usb.py
```

3) On Windows, if AutoRun is enabled and the drive is configured, `autorun.inf` -> `lunch.bat` will start the wrapper.

## Files
- `usb.py`      : Main screenshot capture script with `main()` entrypoint
- `stealth_capture.py` : Wrapper that delegates to `usb.py` (added for compatibility with `lunch.bat`)
- `lunch.bat`   : Batch launcher (minimizes window and runs `stealth_capture.py`)
- `autorun.inf` : AutoRun configuration (Windows)
- `Plug.py`     : Larger alternate version of the tool (contains more features)
- `ReadMe.txt`/`ReadMe1.txt` : Usage and installation notes

## Security & ethics
This repository's behavior can be used for covert monitoring. Only deploy or run it where you have permission. Consider adding explicit consent checks, safe-mode flags, or disabling autorun for ethical distribution.

## Next recommended changes
- (Optional) Add an `installer.bat` or packaging script if this is to be distributed to other machines with a portable Python setup.
- (Optional) Add tests or a dry-run mode that writes captures to a local dev folder rather than a hidden device folder.
