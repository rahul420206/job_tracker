from pydantic import BaseModel

class JobCreate(BaseModel):
    title: str
    description: str
    location: str
    company: str
