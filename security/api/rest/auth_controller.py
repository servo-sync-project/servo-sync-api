from fastapi import APIRouter, BackgroundTasks, Depends
from dependency_injector.wiring import inject, Provide
from security.resource.request.auth_request import EmailVerificationRequest, LoginUserRequest, PasswordResetRequest, PasswordResetRequestByEmail, RefreshTokenRequest, RegisterUserRequest
from security.resource.response.auth_response import AuthResponse, AuthResponseForRefresh
from security.mapping.auth_mapper import AuthMapper
from security.service.auth_service import AuthService
from security.service.auth_service import pwd_context
from core.container import Container

# Definir el router con prefijo y etiqueta
router = APIRouter(
    prefix="/api/v1/auth",  # Prefijo para todas las rutas de autenticación
    tags=["auth"]  # Etiqueta que agrupa las rutas bajo "auth"
)

@router.post("/register", response_model=AuthResponse)
@inject
async def registerUser(request: RegisterUserRequest,
                       backgroundTasks: BackgroundTasks,
                       authService: AuthService = Depends(Provide[Container.authService])):
    user = authService.register(AuthMapper.registerRequestToModel(request), backgroundTasks)
    token = authService.createJWToken(user.email)
    return AuthMapper.modelToResponseWithTokens(user, token)

@router.post("/login", response_model=AuthResponse)
@inject
async def loginUser(request: LoginUserRequest,
                    authService: AuthService = Depends(Provide[Container.authService])):
    user = authService.authenticate(request.email, request.password.get_secret_value())
    token = authService.createJWToken(user.email)
    return AuthMapper.modelToResponseWithTokens(user, token)

@router.post("/refresh-token", response_model=AuthResponseForRefresh)
@inject
async def refreshToken(request: RefreshTokenRequest,
                    authService: AuthService = Depends(Provide[Container.authService])):
    user = authService.validateUniqueToken(request.unique_token)
    token = authService.createJWToken(user.email)
    return AuthMapper.modelToResponseWithAccessToken(user, token)

@router.post("/verify-email", response_model=bool)
@inject
async def verifyEmail(request: EmailVerificationRequest,
                    authService: AuthService = Depends(Provide[Container.authService])):
    return authService.verifyEmail(request.verification_uuid)

@router.post("/forgot-password/send-email", response_model=bool)
@inject
async def sendEmailToResetPassword(request: PasswordResetRequestByEmail,
                    backgroundTasks: BackgroundTasks,
                    authService: AuthService = Depends(Provide[Container.authService])):
    return authService.sendEmailToResetPassword(request.email, backgroundTasks)

@router.post("/forgot-password/reset-password", response_model=bool)
@inject
async def resetPassword(request: PasswordResetRequest,
                    authService: AuthService = Depends(Provide[Container.authService])):
    return authService.resetPassword(request.verification_uuid, pwd_context.hash(request.password.get_secret_value()))


