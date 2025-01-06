from flask import Flask, request, jsonify, render_template
from threading import Thread
import plastic_detection
from werkzeug.utils import secure_filename
import analyse
from flask import send_from_directory
import os
import json
import time

app = Flask(__name__)

# Thread variable
scan_thread = None

app.config['UPLOAD_FOLDER'] = 'uploads'
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}

@app.route('/')
def index():
    # Render the HTML interface
    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('upload.html', error="No file part in the request.")

        file = request.files['file']
        if file.filename == '':
            return render_template('upload.html', error="No file selected.")

        if file and allowed_file(file.filename):
            # Save the file with a timestamp to avoid overwrites
            filename = secure_filename(file.filename)
            filename = f"{int(time.time())}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            try:
                # Call the external function to analyze the image
                result = analyse.analyze_image(filepath)

                # Save the result and user details to JSON file
                user_details = {
                    "filename": filename,
                    "result": result
                }
                with open('user_data.json', 'a') as json_file:
                    json.dump(user_details, json_file)
                    json_file.write('\n')

                # Return the analysis result
                return render_template('upload.html', result=result, filename=filename)

            except Exception as e:
                # Handle errors in image analysis
                return render_template('upload.html', error=f"Error during analysis: {str(e)}")

        return render_template('upload.html', error="File type not allowed. Only PNG, JPG, and JPEG are supported.")

    return render_template('upload.html')

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
