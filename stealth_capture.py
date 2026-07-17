"""
stealth_capture.py
Wrapper to provide the filename expected by the existing Windows batch launcher (lunch.bat).
This simply delegates to usb.py's main() so the launcher can call ``stealth_capture.py`` as documented.
"""

import sys

# Ensure the usb module from the repo is importable when run from the repository root
if __name__ == "__main__":
    # Add repository directory to path so usb.py can be imported when launched from USB root
    import os
    repo_root = os.path.dirname(os.path.abspath(__file__))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

    try:
        import usb
    except Exception as e:
        print("❌ Failed to import usb module:", e)
        raise

    # Delegate to usb.main()
    try:
        usb.main()
    except Exception as e:
        print("❌ Error running usb.main():", e)
        raise
