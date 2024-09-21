import os
import cv2
from ultralytics import YOLO

project_dir = os.path.dirname(os.path.abspath(__file__))
model = YOLO(os.path.join(project_dir, 'best.pt'))

def detect_warning_on_video(video_path: str) -> str: 
    project_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(project_dir, 'output_video.mp4')
    cap = cv2.VideoCapture(video_path)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(file_path, fourcc, 30.0, (int(cap.get(3)), int(cap.get(4))))
    while cap.isOpened():
        ret, frame = cap.read()
        
        if not ret:
            break

        results = model(frame)
        annotated_frame = results[0].plot()
        out.write(annotated_frame)
    return file_path