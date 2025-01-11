import cv2
import numpy as np
from ultralytics import YOLO

# Create a blank image (dummy image)
dummy_image = np.zeros((640, 640, 3), dtype=np.uint8)
cv2.imwrite('dummy.jpg', dummy_image)

# Load the YOLOv8 model
model = YOLO('yolov8n.pt')

# Run inference on the dummy image
model.predict('dummy.jpg')
