import os
from ultralytics import YOLO

project_dir = os.path.dirname(os.path.abspath(__file__))
model = YOLO(os.path.join(project_dir, 'model/best.pt'))