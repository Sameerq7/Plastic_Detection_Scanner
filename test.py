import cv2
import torch
import numpy as np
import time
import pygame

# Initialize pygame mixer for sound
pygame.mixer.init()

# Load a pre-trained model (YOLOv5 for object detection)
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Initialize webcam (or use an image/video)
cap = cv2.VideoCapture(0)

# Define file paths for audio
plastic_detected_audio = 'C:/Users/hp/Desktop/Plastic_detection/audio/Plastic_detected.mp3'
no_plastic_audio = 'C:/Users/hp/Desktop/Plastic_detection/audio/NO_plastic.mp3'

# Define a list of object classes related to plastic
plastic_classes = ['bottle', 'cup', 'cover', 'wrapper', 'bag', 'can', 'container']

# Variables to track the last time plastic was detected
last_detection_time = time.time()
last_plastic_sound_time = time.time()  # Track the last time the plastic sound was played

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Perform object detection on the frame
    results = model(frame)

    # Parse the results
    boxes = results.xyxy[0].cpu().numpy()  # Bounding boxes [x1, y1, x2, y2, confidence, class_id]
    class_ids = results.names  # Class names
    scores = results.xyxy[0][:, 4].cpu().numpy()  # Confidence scores

    # Flag to check if plastic is detected
    plastic_detected = False

    # Draw bounding boxes and labels
    for box, score, class_id in zip(boxes, scores, boxes[:, 5].astype(int)):  # Last column is the class_id
        x1, y1, x2, y2, _, _ = box  # Unpack the box, we only care about coordinates
        label = f'{class_ids[class_id]} {score:.2f}'

        # Check if the detected object belongs to plastic-related classes
        if class_ids[class_id] in plastic_classes:
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)  # Green box for plastic
            cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            plastic_detected = True
        else:
            # For non-plastic objects, draw a red box
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)  # Red box for non-plastic
            cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # Play the plastic detected sound every 5 seconds when plastic is detected
    if plastic_detected and time.time() - last_plastic_sound_time >= 5:
        pygame.mixer.music.load(plastic_detected_audio)  # Load the sound for plastic detection
        pygame.mixer.music.play()  # Play the sound
        last_plastic_sound_time = time.time()  # Update the last time the plastic sound was played

    # If no plastic detected for 15 seconds, play the "No Plastic" sound
    if not plastic_detected and time.time() - last_detection_time >= 15:
        pygame.mixer.music.load(no_plastic_audio)  # Load the sound for no plastic detection
        pygame.mixer.music.play()  # Play the sound
        last_detection_time = time.time()  # Reset the timer

    # Display the frame
    cv2.imshow("Plastic Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Exit on 'q'
        break

cap.release()
cv2.destroyAllWindows()
