import threading
import time
import sys
import os
import webview
from app import app

def start_server():
    # Use a specific port to ensure we can connect, or let Flask find an open one dynamically
    # For simplicity, we stick to 5000 but it's often safer to use a dynamic port in production desktop apps
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)

if __name__ == '__main__':
    # Start the Flask app in a separate thread
    flask_thread = threading.Thread(target=start_server)
    flask_thread.daemon = True
    flask_thread.start()

    # Wait for the server to start (simple sleep to ensure flask is ready)
    time.sleep(1)

    # Create and start the webview window
    window = webview.create_window('HookMiner OS', 'http://127.0.0.1:5000/', width=1200, height=800)
    webview.start()
