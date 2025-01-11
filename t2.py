from ultralytics import YOLO

# Replace with your model's path or use the default 'yolov8n.pt'
model = YOLO('yolov8n.pt')

# Debugging line to print model details
print(f"Model details: {model}")  # Print the whole model to inspect attributes

# Run a dummy inference to ensure it downloads the model and caches it
model.predict("dummy.jpeg")  # Replace with an actual image path or use a dummy image
