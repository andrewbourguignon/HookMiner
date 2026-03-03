import os
import sys
import queue
import threading
from flask import Flask, render_template, request, Response, send_file, jsonify
from main import run_pipeline
import platform
import subprocess

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hookminer_secret'

# Store logs to be streamed to the client
log_queue = queue.Queue()

class StreamLogger:
    def write(self, msg):
        # We only want to send non-empty and non-whitespace-only messages
        if msg:
            log_queue.put(msg)
        sys.__stdout__.write(msg)
    def flush(self):
        sys.__stdout__.flush()

def background_task(apify_token, gemini_key, target_handles, target_videos, min_views, scan_limit):
    # Temporarily redirect stdout to our custom logger
    original_stdout = sys.stdout
    sys.stdout = StreamLogger()
    
    try:
        run_pipeline(apify_token, gemini_key, target_handles, target_videos, min_views, scan_limit)
    except Exception as e:
        print(f"\n[ERROR] HookMiner encountered an error: {e}")
    finally:
        sys.stdout = original_stdout
        log_queue.put("___DONE___")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run_hookminer():
    data = request.json
    
    apify_token = data.get('apify_token', '').strip()
    gemini_key = data.get('gemini_key', '').strip()
    
    # Process strings into lists
    handles_str = data.get('handles', '')
    target_handles = [h.strip() for h in handles_str.split('\n') if h.strip()]
    
    videos_str = data.get('videos', '')
    target_videos = [v.strip() for v in videos_str.split('\n') if v.strip()]
    
    min_views_str = data.get('min_views', '1000000')
    try:
        min_views = int(min_views_str)
    except ValueError:
        min_views = 1000000

    scan_limit_str = data.get('scan_limit', '10')
    try:
        scan_limit = int(scan_limit_str)
    except ValueError:
        scan_limit = 10

    if not apify_token or not gemini_key:
        return jsonify({"error": "Both Apify and Gemini API keys are required."}), 400

    if not target_handles and not target_videos:
        return jsonify({"error": "Please provide at least one Target Handle or Target Video."}), 400

    # Clear the queue before starting
    while not log_queue.empty():
        log_queue.get()

    # Start the pipeline in a background thread
    thread = threading.Thread(target=background_task, args=(apify_token, gemini_key, target_handles, target_videos, min_views, scan_limit))
    thread.daemon = True
    thread.start()
    
    return jsonify({"status": "started"})

@app.route('/stream')
def stream():
    def event_stream():
        while True:
            try:
                # Wait for a log message
                msg = log_queue.get(timeout=30)
                if msg == "___DONE___":
                    yield "data: ___DONE___\n\n"
                    break
                
                # Format for SSE
                yield f"data: {msg}\n\n"
            except queue.Empty:
                # Keep-alive
                yield "data: \n\n"
                
    return Response(event_stream(), mimetype="text/event-stream")

@app.route('/download')
def download():
    documents_dir = os.path.expanduser("~/Documents/HookMiner/data")
    file_path = os.path.join(documents_dir, 'proven_hooks.csv')
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return "No CSV file generated yet.", 404

@app.route('/open_data')
def open_data():
    documents_dir = os.path.expanduser("~/Documents/HookMiner/data")
    if os.path.exists(documents_dir):
        if platform.system() == "Darwin":
            subprocess.run(["open", documents_dir])
        elif platform.system() == "Windows":
            os.startfile(documents_dir)
        else:
            subprocess.run(["xdg-open", documents_dir])
        return jsonify({"status": "opened"})
    return jsonify({"error": "Data directory does not exist yet.", "status": "error"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
