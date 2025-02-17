# Pyrolysis Material Analyzer

A web application that analyzes uploaded images to determine whether the material is suitable for pyrolysis. This project uses **YOLOv5** for object detection and identifies specific plastic-related objects to assess suitability.

---

## Features

- Upload images and detect objects for pyrolysis suitability.
- Displays results with celebratory emojis for suitable materials or red flags for unsuitable ones.
- Built with **Flask**, **YOLOv5**, and **HTML/CSS** for a seamless interface.

---

## Technologies Used

- **Backend**: Flask, Python
- **Frontend**: HTML, CSS, Bootstrap
- **Object Detection**: YOLOv5 (pretrained on COCO dataset)
- **Dependencies**: Torch, PIL, NumPy

---

## Installation and Setup

### Prerequisites
- Python 3.8 or later
- pip (Python package manager)

### Steps to Run the Project
1. **Clone the repository**:
   ```bash
   git clone https://github.com/Sameerq7/Plastic_Detection_Scanner.git
   cd Plastic_Detection_Scanner
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Open your browser and navigate to**:
   ```
   http://127.0.0.1:5000
   ```

---

## Project Structure
```
<Plastic_Detection_Scanner>/
│
├── app.py               # Main Flask application
├── analyse.py           # Image analysis logic using YOLOv5
├── plastic_detection.py # Additional logic for plastic detection
├── requirements.txt     # Python dependencies
├── templates/           # HTML templates
│   └── index.html       # Main HTML page
├── static/              # Static files (CSS, JS, images)
│   ├── images/          # Favicon and other images
│   └── styles.css       # Custom styling
├── uploads/             # Directory to store uploaded files
├── audio/               # Audio-related files (if any)
├── reports/             # Directory for generated reports
├── yolov5s.pt           # Pretrained YOLOv5 model
├── test.py              # Testing script for the application
├── user_data.json       # User-related data (if required)
├── plastic-env/         # Virtual environment for dependencies
├── .gitignore           # Git ignore file
├── __pycache__/         # Compiled Python files
├── report.py            # Report generation logic
├── t2.py                # Another Python script
├── t3.py                # Another Python script
└── README.md            # Project documentation
```
---

## API Details

### Upload Endpoint
- **URL**: `/upload`
- **Method**: `POST`
- **Description**: Accepts an image file, analyzes it, and returns the result.

---

## Example Output

### 1. Suitable for Pyrolysis
🎉🎉 This material is suitable for pyrolysis! 🎉🎉

### 2. Not Suitable for Pyrolysis
🚩 This material is NOT suitable for pyrolysis. 🚩

---

## Contributing
Feel free to fork this repository, make improvements, and submit pull requests. Contributions are always welcome!

---

## License
This project is licensed under the [MIT License](LICENSE).

