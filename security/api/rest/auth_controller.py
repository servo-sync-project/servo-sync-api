from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide
from security.resource.request.register_user_request import RegisterUserRequest
from security.resource.request.login_user_request import LoginUserRequest
from security.resource.response.auth_response import AuthResponse
from security.mapping.auth_mapper import AuthMapper
from security.service.auth_service import AuthService
from core.container import Container

# Definir el router con prefijo y etiqueta
router = APIRouter(
    prefix="/api/v1/auth",  # Prefijo para todas las rutas de autenticación
    tags=["auth"]  # Etiqueta que agrupa las rutas bajo "auth"
)

# Registro de usuario
@router.post("/register", response_model=AuthResponse)
@inject
async def registerUser(request: RegisterUserRequest,
                        authService: AuthService = Depends(Provide[Container.authService])):
    user = authService.register(AuthMapper.registerRequestToModel(request))
    token = authService.createJWToken(user.email)
    return AuthMapper.ModelToResponseWithToken(user, token)

# Inicio de sesión
@router.post("/login", response_model=AuthResponse)
@inject
async def loginUser(request: LoginUserRequest,
                    authService: AuthService = Depends(Provide[Container.authService])):
    user = authService.authenticate(request.email, request.password)
    token = authService.createJWToken(user.email)
    return AuthMapper.ModelToResponseWithToken(user, token)

