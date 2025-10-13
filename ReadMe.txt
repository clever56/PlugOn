This tool is provided for educational and legitimate monitoring purposes only.
Users are solely responsible for complying with local laws and regulations.
Always obtain proper consent before monitoring any system.

# Install all required packages
pip install psutil pyautogui opencv-python Pillow pynput pyaudio

# Or install individually:
pip install psutil        # System information and process utilities
pip install pyautogui     # Screenshot and screen recording
pip install opencv-python # Video processing and recording
pip install Pillow        # Image processing and compression
pip install pynput        # Keyboard and mouse input monitoring
pip install pyaudio       # Audio recording capabilities

Optional Packages:
pip install requests      # Enhanced internet connectivity checking
pip install numpy         # Advanced array processing (usually included with OpenCV)


# For pyaudio on Windows, you might need:
pip install pipwin
pipwin install pyaudio

# For pyaudio on macOS, first install portaudio:
brew install portaudio
pip install pyaudio

# Install system dependencies first
sudo apt update
sudo apt install python3-dev portaudio19-dev libffi-dev libssl-dev
pip install pyaudio

# For screenshots on Linux, you might need:
sudo apt install scrot python3-tk python3-dev