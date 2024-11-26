from datetime import datetime, timedelta
from fastapi import HTTPException, status
import jwt
from security.domain.persistence.user_repository import UserRepository
from security.domain.model.user import Role, User
from passlib.context import CryptContext 
from core.config import settings

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

class AuthService:
    def __init__(self, userRepository: UserRepository):
        self.repository = userRepository
    
    def register(self, user: User):
        if self.repository.findByUsername(user.username):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
        
        if self.repository.findByEmail(user.email):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
        
        return self.repository.save(user)
    
    def authenticate(self, email: str, password: str):
        authenticatedUser = self.repository.findByEmail(email)
        
        if not authenticatedUser or not self.verifyPassword(password, authenticatedUser.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        
        return authenticatedUser
    
    def createJWToken(self, email: str):
        payload = {
            "email": email,
            "exp": datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
        }
        return jwt.encode(payload=payload, key=settings.secret_key, algorithm=settings.algorithm)

    def validateJWToken(self, token: str):
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
            email: str = payload.get("email")
            print(f"Decoded email: {email}")
            if email is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
            user = self.repository.findByEmail(email)
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
            return user
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    def authorizeRoles(self, user: User, roles: list[Role]):
        if user.role not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
        return True
    
    def hashPassword(self, password: str):
        return pwd_context.hash(password)

    def verifyPassword(self, plain_password: str, hashed_password: str):
        return pwd_context.verify(plain_password, hashed_password)
    