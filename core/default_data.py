from datetime import datetime, timedelta, timezone
import secrets
import uuid
from security.domain.model.user import User, Role
from security.domain.persistence.user_repository import UserRepository
from security.service.auth_service import pwd_context
from core.config import settings

def defaultData(userRepository: UserRepository):
    if not userRepository.findByEmail(settings.initial_admin_email):
        userRepository.save(User(
            verification_uuid=str(uuid.uuid4()),
            unique_token=secrets.token_urlsafe(32),
            email=settings.initial_admin_email,
            username=settings.initial_admin_username, 
            hashed_password=pwd_context.hash(settings.initial_admin_password), 
            email_verified_at=datetime.now(timezone.utc),
            uuid_expires_at=datetime.now(timezone.utc) + timedelta(days=1),
            token_expires_at=datetime.now(timezone.utc) + timedelta(days=30),
            role=Role.ADMIN))
