from pydantic import BaseModel

class LoginUserRequest(BaseModel):
    email: str
    password: str# Permite que el rol se especifique opcionalmente
