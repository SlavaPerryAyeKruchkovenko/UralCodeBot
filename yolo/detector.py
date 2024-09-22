import io
import os
from pathlib import Path
import cv2
from matplotlib import pyplot as plt
import numpy as np
from ultralytics import YOLO
from PIL import Image
from aiogram.types import FSInputFile
from bot import send_photo_for_subscribers

project_dir = os.path.dirname(os.path.abspath(__file__))
model = YOLO(os.path.join(project_dir, "best.pt"))
names = {0: "Door", 1: "Helmet", 2: "Human", 3: "Robot"}
helmet_error_count = 0
throatlehelmetCount = 10


async def detect_warning_on_video(video_path: str) -> str:
    project_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(project_dir, "output_video.mp4")
    cap = cv2.VideoCapture(video_path)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(file_path, fourcc, 30.0, (int(cap.get(3)), int(cap.get(4))))
    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        results = model(frame)
        tile = results[0]
        await processing_tile(tile)
        annotated_frame = tile.plot()
        out.write(annotated_frame)
    return file_path


def get_tile_boxes(result):
    all_bounding_boxes = []
    boxes = result.boxes
    for box in boxes:
        x1, y1, x2, y2 = box.xyxy[0]
        class_id = int(box.cls[0])
        confidence = box.conf[0].item()

        # Добавляем информацию в список
        all_bounding_boxes.append(
            {"coords": (x1, y1, x2, y2), "class_id": class_id, "confidence": confidence}
        )
    return all_bounding_boxes


async def precessing_helmet_tile(boxes, result):
    global helmet_error_count
    human_boxes = [
        box for box in boxes if box["class_id"] == 2 and box["confidence"] > 0.5
    ]
    helmet_boxes = [box for box in boxes if box["class_id"] == 1]
    if len(human_boxes) > len(helmet_boxes):
        helmet_error_count += 1
    if helmet_error_count >= throatlehelmetCount:
        helmet_error_count = 0
        img = Image.fromarray(np.uint8(result.plot()))
        file_name = "result_image.png"
        img.save(file_name, format='PNG')
        file_path = Path(file_name).resolve()
        photo = FSInputFile(file_path, filename="result.png")
        await send_photo_for_subscribers(photo,"Обнуружен человек без каски в секции 1")
        os.remove(file_path)


async def processing_tile(result):
    boxes = get_tile_boxes(result)
    await precessing_helmet_tile(boxes, result)
