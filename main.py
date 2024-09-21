from typing import Union
from fastapi import FastAPI, File, Form, UploadFile
from starlette.responses import JSONResponse
from pydantic import BaseModel
import nest_asyncio
import asyncio

import uvicorn
from bot import init_bot
from models.Coordinates import UploadVideoForPredict

app = FastAPI()

@app.get("/test")
async def upload_video():
    return JSONResponse({"suck":"cock"})

@app.post("/upload")
async def upload_video(
    coordinates: UploadVideoForPredict,
    file: UploadFile 
):
    contents = await file.read()
    return JSONResponse(content={
        "message": "Файл и координаты успешно загружены",
        "coordinates": coordinates.dict()
    })

async def start_fastapi():
    import uvicorn
    # Запускаем FastAPI
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

async def main():
    # Запускаем бота и FastAPI параллельно
    await asyncio.gather(init_bot(), start_fastapi())

if __name__ == "__main__":
    nest_asyncio.apply()
    asyncio.run(main())
