import sys
import threading
import os
import time
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 600, 400)
        self.setWindowTitle('Hot Reload Example')

        self.btn_reload = QPushButton('Reload', self)
        self.btn_reload.setGeometry(600, 250, 100, 100)
        self.btn_reload.clicked.connect(self.reloadApp)
        self.showMaximized()

    def reloadApp(self):
        print("Reloading application...")
        # Your reload logic here
        pass

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, app):
        super().__init__()
        self.app = app

    def on_any_event(self, event):
        if event.is_directory or not event.src_path.endswith('.py'):
            return
        print("File change detected:", event.src_path)
        self.app.reloadApp()

def run_watchdog():
    observer = Observer()
    observer.schedule(FileChangeHandler(app), '.', recursive=True)
    observer.start()

def watch_file_changes():
    while True:
        time.sleep(1)
        # Check if the main Python file has been modified
        if os.path.getmtime(__file__) > last_modified:
            print("Changes detected in main file. Reloading...")
            os.execv(sys.executable, ['python'] + sys.argv)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    # Start watchdog to monitor file changes
    threading.Thread(target=run_watchdog, daemon=True).start()

    # Get the last modified time of the main file
    last_modified = os.path.getmtime(__file__)

    # Start watching file changes in a separate thread
    threading.Thread(target=watch_file_changes, daemon=True).start()

    sys.exit(app.exec())
