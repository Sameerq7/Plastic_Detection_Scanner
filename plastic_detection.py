import os
import cv2
import torch
import numpy as np
import time
import pygame
from threading import Event

# Initialize pygame mixer for sound if audio is available
if os.getenv('RENDER') is None:  # assuming 'RENDER' is not set in Render environment
    pygame.mixer.init()

# Load a pre-trained model (YOLOv5 for object detection)
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Define file paths for audio
plastic_detected_audio = 'C:/Users/hp/Desktop/Plastic_detection/audio/Plastic_detected.mp3'
no_plastic_audio = 'C:/Users/hp/Desktop/Plastic_detection/audio/NO_plastic.mp3'

# Define a list of object classes related to plastic
plastic_classes = ['bottle', 'cup', 'cover', 'wrapper', 'bag', 'can', 'container', 'cell phone', 'remote', 'toilet']

# Event for stopping the detection
stop_event = Event()

def detect_plastic():
    cap = cv2.VideoCapture(0)
    last_detection_time = time.time()
    last_plastic_sound_time = time.time()
    print("Detection started")
    
    while not stop_event.is_set():
        ret, frame = cap.read()
        if not ret:
            break

        # Perform object detection
        results = model(frame)

        # Parse results
        boxes = results.xyxy[0].cpu().numpy()
        class_ids = results.names
        scores = results.xyxy[0][:, 4].cpu().numpy()

        plastic_detected = False

        # Draw bounding boxes and labels
        for box, score, class_id in zip(boxes, scores, boxes[:, 5].astype(int)):
            x1, y1, x2, y2, _, _ = box
            label = f'{class_ids[class_id]} {score:.2f}'

            if class_ids[class_id] in plastic_classes:
                # Show just "Plastic Detected" for plastic-related objects
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                cv2.putText(frame, "Plastic Detected", (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                plastic_detected = True
            else:
                # Display non-plastic objects with their label
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)
                cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # Play sound when plastic is detected
        if plastic_detected and time.time() - last_plastic_sound_time >= 5 and os.getenv('RENDER') is None:
            pygame.mixer.music.load(plastic_detected_audio)
            pygame.mixer.music.play()
            last_plastic_sound_time = time.time()

        # Play sound when no plastic is detected for a while
        if not plastic_detected and time.time() - last_detection_time >= 15 and os.getenv('RENDER') is None:
            pygame.mixer.music.load(no_plastic_audio)
            pygame.mixer.music.play()
            last_detection_time = time.time()

        # Display frame
        cv2.imshow("Plastic Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def stop_detection():
    stop_event.set()