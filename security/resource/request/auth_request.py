from pydantic import BaseModel, EmailStr, SecretStr

class RefreshTokenRequest(BaseModel):
    unique_token: str

class RegisterUserRequest(BaseModel):
    email: EmailStr
    username: str
    password: SecretStr

class LoginUserRequest(BaseModel):
    email: EmailStr
    password: SecretStr

class SendEmailRequest(BaseModel):
    email: EmailStr

class EmailVerificationRequest(BaseModel):
    verification_uuid: str

class PasswordResetRequest(BaseModel):
    verification_uuid: str
    password: SecretStr