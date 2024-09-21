from pydantic import BaseModel

class Point(BaseModel):
    x: float
    y: float
    
class SectionCoordinate(BaseModel):
    doorCoors: list[Point]
    sectionCoors: list[Point]
    