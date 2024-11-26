from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from security.domain.model.user import Role, User
from core.container import Container

security = HTTPBearer()

# Configuramos el contenedor
container = Container()
authService = container.authService()

def getAuthenticatedUser(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    user = authService.validateJWToken(token=credentials.credentials)
    return user

def authorizeRoles(roles: list[Role]):
    def wrapper(current_user: User = Depends(getAuthenticatedUser)):
        authService.authorizeRoles(current_user, roles)
        return current_user
    return wrapper
