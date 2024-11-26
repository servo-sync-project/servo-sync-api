from security.domain.model.user import User, Role
from security.domain.persistence.user_repository import UserRepository
from security.service.auth_service import pwd_context
from core.config import settings

def defaultData(userRepository: UserRepository):
    if not userRepository.findByUsername(settings.initial_admin_username):
        userRepository.save(User(
            image_url=settings.initial_admin_image_url,
            email=settings.initial_admin_email,
            username=settings.initial_admin_username, 
            full_name=settings.initial_admin_full_name,
            hashed_password=pwd_context.hash(settings.initial_admin_password), 
            enabled=True,
            role=Role.ADMIN))
