from pydantic import BaseModel

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    role: str

