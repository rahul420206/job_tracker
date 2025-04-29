from pydantic import BaseModel

class ApplicationCreate(BaseModel):
    job_id: int
    username: str
