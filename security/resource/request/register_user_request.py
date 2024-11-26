from pydantic import BaseModel

class RegisterUserRequest(BaseModel):
    image_url: str
    email: str
    username: str
    full_name: str
    password: str
