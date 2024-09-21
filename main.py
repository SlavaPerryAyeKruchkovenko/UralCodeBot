import os
from typing import Union
import uuid
from fastapi import FastAPI, File, Form, UploadFile
from starlette.responses import JSONResponse
from pydantic import BaseModel
import nest_asyncio
import asyncio

import uvicorn
from bot import init_bot
from models.Coordinates import SectionCoordinate
from yolo.detector import detect_warning_on_video

app = FastAPI(
    title="Мой API",
    description="Api for ural code hackaton",
    version="1.0.0",
)
s_coordinates: SectionCoordinate = None

@app.get("/ready")
async def upload_video():
    return JSONResponse(True)

@app.post("/coordinate")
async def create_coordinate(coordinates: SectionCoordinate):
    s_coordinates = coordinates
    print(coordinates)
    return JSONResponse({"succes":True})

@app.post("/upload")
async def upload_video(
    file: UploadFile 
):
    try:
        bytes_io = await file.read()
        filename = f"{file.filename}_{uuid.uuid4()}.{file.content_type.split('/')[1]}"
        project_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(project_dir, filename)
        with open(file_path, "wb") as f:
            f.write(bytes_io)
        detect_warning_on_video(file_path)
        os.remove(file_path)
        return JSONResponse(content={
            "succes": True,
        })
    except Exception as e:
        return {"error": str(e)}

async def start_fastapi():
    import uvicorn
    # Запускаем FastAPI
    config = uvicorn.Config(app, host="0.0.0.0", port=8080, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

async def main():
    # Запускаем бота и FastAPI параллельно
    await asyncio.gather(init_bot(), start_fastapi())

if __name__ == "__main__":
    nest_asyncio.apply()
    asyncio.run(main())
