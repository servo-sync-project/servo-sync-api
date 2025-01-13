from datetime import datetime, timedelta, timezone
import logging
import uuid
import secrets
from fastapi import BackgroundTasks, HTTPException, status
import jwt
from security.domain.persistence.user_repository import UserRepository
from security.domain.model.user import Role, User
from passlib.context import CryptContext 
from core.config import settings
from crosscutting.service.email_service import EmailService

logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

class AuthService:
    def __init__(self, userRepository: UserRepository, emailService: EmailService):
        self.repository = userRepository
        self.emailService = emailService
    
    def register(self, user: User, background_tasks: BackgroundTasks):
        if self.repository.findByEmail(user.email) or self.repository.findByUsername(user.username):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
        
        user.verification_uuid = self.generateUUID()
        user.uuid_expires_at = datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(days=1)

        user.unique_token = self.generateUniqueToken()
        user.token_expires_at = datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(days=30)
    
        saved_user = self.repository.save(user)
        
        # Create the verification link
        verification_url = f"{settings.origin_url}/login?uuid={saved_user.verification_uuid}"
        self.emailService.sendEmailVerification(saved_user.email, "Email Verification", verification_url, background_tasks)
        
        return saved_user
    
    def updateVerificationUUID(self, user: User):
        user.verification_uuid = self.generateUUID()
        user.uuid_expires_at = datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(days=settings.verification_uuid_expire_days)
        return self.repository.save(user)
    
    def updateUniqueToken(self, user: User):
        user.unique_token = self.generateUniqueToken()
        user.token_expires_at = datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(days=settings.unique_token_expire_days)
        return self.repository.save(user)

    def authenticate(self, email: str, password: str):
        user = self.repository.findByEmail(email)
    
        if not user or not self.verifyPassword(password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")
        
        if not user.email_verified_at:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email not verified")
        
        return self.updateUniqueToken(user)

    def createJWToken(self, email: str):
        payload = {
            "email": email,
            "exp": datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
        }
        return jwt.encode(payload=payload, key=settings.secret_key, algorithm=settings.algorithm)

    def validateJWToken(self, token: str):
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
            email: str = payload.get("email")
            logger.info(f"Decoded email: {email}")
            if not email:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
            user = self.repository.findByEmail(email)
            if not user:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
            if not user.email_verified_at:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not verified")
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
    
    def validateUniqueToken(self, uniqueToken: str):
        user = self.repository.findByUniqueToken(uniqueToken)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        
        if user.token_expires_at < datetime.now(timezone.utc).replace(tzinfo=None):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token has expired")
        return user     
        
    def verifyPassword(self, plain_password: str, hashed_password: str):
        return pwd_context.verify(plain_password, hashed_password)
    
    def verifyEmail(self, verificationUuid: str):
        user = self.repository.findByVerificationUuid(verificationUuid)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        if user.email_verified_at:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already verified")
        
        if user.uuid_expires_at < datetime.now(timezone.utc).replace(tzinfo=None):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="UUID expired")
        
        self.updateVerificationUUID(user)
        return True
    
    def sendEmailToResetPassword(self, email: str, background_tasks: BackgroundTasks):
        user = self.repository.findByEmail(email)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        if not user.email_verified_at:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User not verified")
        
        user = self.updateVerificationUUID(user)

        # Create the verification link
        verification_url = f"{settings.origin_url}/reset-password?uuid={user.verification_uuid}"
        self.emailService.sendPasswordReset(user.email, "Email Verification", verification_url, background_tasks)
        
        return True

    def resetPassword(self, verificationUuid: str, newHashedPassword: str):
        user = self.repository.findByVerificationUuid(verificationUuid)
        
        if not user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User not found")
        
        if not user.email_verified_at:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User not verified")
        
        if user.uuid_expires_at < datetime.now(timezone.utc).replace(tzinfo=None):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="UUID expired")
        
        user.hashed_password = newHashedPassword
        self.updateVerificationUUID(user)
        
        return True
    
    def generateUUID(self):
        verificationUuid = str(uuid.uuid4())
        while self.repository.findByVerificationUuid(verificationUuid):
            verificationUuid = str(uuid.uuid4())
        return verificationUuid
    
    def generateUniqueToken(self):
        uniqueToken = secrets.token_urlsafe(32)
        while self.repository.findByUniqueToken(uniqueToken):
            uniqueToken = secrets.token_urlsafe(32)
        return uniqueToken
