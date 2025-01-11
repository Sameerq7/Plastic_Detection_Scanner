import os
import torch
from PIL import Image
import numpy as np

# Load YOLOv5 model (pretrained on COCO dataset)
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Define plastic-related classes
plastic_classes = ['bottle', 'cup', 'cover', 'wrapper', 'bag', 'can', 'container', 'cell phone', 'remote', 'toilet','polythene']

def analyze_image(filepath):
    """
    Analyze the uploaded image to detect plastic-related objects.
    :param filepath: Path to the uploaded image file.
    :return: A result string indicating the analysis outcome.
    """
    try:
        # Load the image using PIL
        img = Image.open(filepath).convert("RGB")

        # Perform inference using YOLOv5
        results = model(img)

        # Extract detected object names and confidence scores
        detected_objects = results.pandas().xyxy[0]  # Get pandas DataFrame
        detected_classes = detected_objects['name'].tolist()

        # Check if any detected object matches a plastic-related class
        if any(obj in plastic_classes for obj in detected_classes):
            return "The material is likely suitable for pyrolysis and can be passed to pyrolysis chamber for combustion chamber"
        else:
            return "The material might not be suitable for pyrolysis,so please pass it to conversion chamber to make it suitable for pyrolysis"

    except Exception as e:
        # Handle errors during image analysis
        raise RuntimeError(f"Error analyzing image: {str(e)}")
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def generate_pdf(results, image_name):
    pdf_filename = f"reports/{image_name}_analysis_report.pdf"
    os.makedirs(os.path.dirname(pdf_filename), exist_ok=True)

    c = canvas.Canvas(pdf_filename, pagesize=letter)
    c.setFont("Helvetica", 12)

    c.drawString(100, 750, f"Analysis Report for {image_name}")
    c.drawString(100, 730, f"Detected Objects and Confidence Scores:")

    y_position = 710
    for _, row in results.iterrows():
        label = row['name']
        confidence = row['confidence']
        c.drawString(100, y_position, f"{label}: {confidence:.2f}")
        y_position -= 20

    c.save()

    return pdf_filename


def analyze_image_report(image_path):
    """
    Analyze the image using YOLOv5 and extract object details such as type, shape, and color.
    Returns a dictionary containing the analysis results.
    """
    # Load image
    img = Image.open(image_path)
    
    # Perform inference using YOLOv5
    results = model(img)
    
    # Results inference
    labels = results.names  # Get object class labels
    predictions = results.pred[0]  # The predicted bounding boxes, class labels, and confidence scores
    
    object_details = []
    for prediction in predictions:
        # Each prediction contains the following [x1, y1, x2, y2, confidence, class]
        x1, y1, x2, y2, confidence, class_idx = prediction.tolist()
        
        # Get object label (type)
        object_type = labels[int(class_idx)]
        
        # Object shape can be described by the aspect ratio (width / height) of the bounding box
        width = x2 - x1
        height = y2 - y1
        aspect_ratio = width / height if height != 0 else 0
        
        # Color (could be inferred from the average color inside the bounding box)
        img_array = np.array(img)
        cropped_img = img_array[int(y1):int(y2), int(x1):int(x2)]
        avg_color = np.mean(cropped_img, axis=(0, 1))  # Average color in RGB
        
        # Add object details to list
        object_details.append({
            "type": object_type,
            "shape": "aspect ratio: {:.2f}".format(aspect_ratio),
            "color": f"RGB: {avg_color.astype(int)}",
            "confidence": confidence
        })

    # Return the analysis result as a dictionary
    result = {
        "description": f"Detected {len(object_details)} objects",
        "objects": object_details
    }

    return result
