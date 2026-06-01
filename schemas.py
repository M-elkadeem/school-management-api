from pydantic import BaseModel

class AnnouncementCreate(BaseModel):
    class_id: str
    title: str
    content: str