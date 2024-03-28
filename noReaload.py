import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ChangeHandler(FileSystemEventHandler):
    """Restart the Kivy app upon file changes."""
    def on_modified(self, event):
        print(f'Event detected: {event}')  # Check if any event is detected
        print(f'File changed: {event.src_path}')
        
        # Terminate the previous instance of the app
        if hasattr(self, 'app_process') and self.app_process:
            self.app_process.terminate()
        # Start a new instance of the app
        self.app_process = subprocess.Popen(['python', 'beta.py'])

handler = ChangeHandler()
observer = Observer()
observer.schedule(handler, path='.', recursive=True)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()
