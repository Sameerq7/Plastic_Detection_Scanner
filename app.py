from flask import Flask, jsonify,render_template
from threading import Thread
import plastic_detection
import os

app = Flask(__name__)

# Thread variable
scan_thread = None

@app.route('/')
def index():
    # Render the HTML interface
    return render_template('index.html')

@app.route('/start_scan', methods=['GET'])
def start_scan():
    global scan_thread
    if scan_thread is None or not scan_thread.is_alive():
        plastic_detection.stop_event.clear()
        scan_thread = Thread(target=plastic_detection.detect_plastic)
        scan_thread.start()
        return jsonify({"status": "Scanning started."})
    return jsonify({"status": "Scan already in progress."})

@app.route('/stop_scan', methods=['GET'])
def stop_scan():
    global scan_thread
    if scan_thread and scan_thread.is_alive():
        plastic_detection.stop_detection()
        scan_thread.join()
        return jsonify({"status": "Scanning stopped."})
    return jsonify({"status": "No scan in progress."})


if __name__ == '__main__':
    # Use the port provided by Render, or default to 5000
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

