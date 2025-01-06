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
