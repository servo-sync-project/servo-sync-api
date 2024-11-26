from typing import Optional
from pydantic import BaseModel
from security.resource.response.user_response import UserResponse

class AuthResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse
