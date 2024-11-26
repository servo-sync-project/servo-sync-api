from typing import Optional
from pydantic import BaseModel

class UserResponse(BaseModel):
    id: int
    image_url: str
    email: str
    username: str
    full_name: str
    enabled: bool
    role: str

