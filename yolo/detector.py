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
from models.Coordinates import Point, SectionCoordinate

project_dir = os.path.dirname(os.path.abspath(__file__))
model = YOLO(os.path.join(project_dir, "best.pt"))
names = {0: "door", 1: "helmet", 2: "person", 3: "robot"}
helmet_error_count = 0
throatlehelmetCount = 50
throatleDoorCount = 5
door_is_open_send = False
door_error_count = 0
door_max_luft = (20, 10)


async def detect_warning_on_video(
    video_path: str, s_coordinates: SectionCoordinate
) -> str:
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
        await processing_tile(tile, s_coordinates)
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


async def precessing_door_tile(boxes, doorCoors: list[Point], result):
    global door_is_open_send
    global door_error_count
    if doorCoors != None:
        is_open = door_is_open(boxes, doorCoors)
        if is_open:
            if door_is_open_send or door_error_count < throatleDoorCount:
                door_error_count += 1
            else:
                img = Image.fromarray(np.uint8(result.plot()))
                file_name = "result_image.png"
                img.save(file_name, format="PNG")
                file_path = Path(file_name).resolve()
                photo = FSInputFile(file_path, filename="result.png")
                await send_photo_for_subscribers(
                    photo, "Обнуружена октрытая дверь в секции 1"
                )
                os.remove(file_path)
                door_is_open_send = True
                door_error_count = 0


def door_is_open(boxes, doorCoors: list[Point]) -> bool:
    door_boxes = [
        box for box in boxes if box["class_id"] == 0 and box["confidence"] > 0.5
    ]
    if len(door_boxes) > 0:
        box = door_boxes[0]
        x1 = box['coords'][0]
        y1 = box['coords'][1]
        left_bottom = find_left_bottom_corner(doorCoors)
        return (
            x1 > left_bottom.x + door_max_luft[0]
            and y1 < left_bottom.y - door_max_luft[1]
        )
    return False


def find_left_bottom_corner(doorCoors: list[Point]) -> Point:
    if not doorCoors:
        return None
    left_bottom_corner = doorCoors[0]
    for point in doorCoors:
        x = point.x
        y = point.y
        if (x < left_bottom_corner.x) or (
            x == left_bottom_corner.x and y > left_bottom_corner.y
        ):
            left_bottom_corner = point

    return left_bottom_corner


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
        img.save(file_name, format="PNG")
        file_path = Path(file_name).resolve()
        photo = FSInputFile(file_path, filename="result.png")
        await send_photo_for_subscribers(
            photo, "Обнуружен человек без каски в секции 1"
        )
        os.remove(file_path)


async def processing_tile(result, coordinate: SectionCoordinate):
    boxes = get_tile_boxes(result)
    await precessing_helmet_tile(boxes, result)
    await precessing_door_tile(boxes, coordinate.doorCoors, result)
