from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from security.domain.model.user import Role, User
from core.container import Container

security = HTTPBearer()

# Configuramos el contenedor
container = Container()
authService = container.authService()

def getAuthenticatedUser(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    current_user = authService.validateJWToken(token=credentials.credentials)
    return current_user

def authorizeRoles(roles: list[Role]):
    def wrapper(current_user: User = Depends(getAuthenticatedUser)):
        return authService.authorizeRoles(current_user, roles)
    return wrapper
