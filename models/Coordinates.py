from pydantic import BaseModel

class Point(BaseModel):
    x: float
    y: float
    
class UploadVideoForPredict(BaseModel):
    doorCoors: list[Point]
    sectionCoors: list[Point]
    