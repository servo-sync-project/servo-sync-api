from typing import Optional
from pydantic import BaseModel
from security.resource.response.user_response import UserResponse

class AuthResponse(BaseModel):
    access_token: str
    unique_token: str
    user: UserResponse

class AuthResponseForRefresh(BaseModel):
    access_token: str
    user: UserResponse
