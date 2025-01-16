from fastapi import APIRouter, BackgroundTasks, Depends
from dependency_injector.wiring import inject, Provide
from security.resource.request.auth_request import EmailVerificationRequest, LoginUserRequest, PasswordResetRequest, RefreshTokenRequest, RegisterUserRequest, SendEmailRequest
from security.resource.response.auth_response import AuthResponse, AuthResponseForRefresh, AuthResponseForVerify
from security.mapping.auth_mapper import AuthMapper
from security.service.auth_service import AuthService
from security.service.auth_service import pwd_context
from core.container import Container
from security.service.user_service import UserService

# Definir el router con prefijo y etiqueta
router = APIRouter(
    prefix="/api/v1/auth",  # Prefijo para todas las rutas de autenticación
    tags=["auth"]  # Etiqueta que agrupa las rutas bajo "auth"
)

@router.post("/register", response_model=AuthResponseForVerify)
@inject
async def registerUser(request: RegisterUserRequest,
                       authService: AuthService = Depends(Provide[Container.authService])):
    user = authService.register(AuthMapper.registerRequestToModel(request))
    return AuthMapper.modelToResponseForVerify(user)

@router.post("/login", response_model=AuthResponse)
@inject
async def loginUser(request: LoginUserRequest,
                    authService: AuthService = Depends(Provide[Container.authService])):
    user = authService.authenticate(request.email, request.password.get_secret_value())
    token = authService.createJWToken(user.email)
    return AuthMapper.modelToResponse(user, token)

@router.post("/refresh-token", response_model=AuthResponseForRefresh)
@inject
async def refreshToken(request: RefreshTokenRequest,
                    authService: AuthService = Depends(Provide[Container.authService]),
                    userService: UserService = Depends(Provide[Container.userService])):
    user = authService.validateUniqueToken(userService.getByUniqueToken(request.unique_token))
    token = authService.createJWToken(user.email)
    return AuthMapper.modelToResponseForRefresh(user, token)

@router.post("/verify-email/send-email", response_model=bool)
@inject
async def sendEmailToVerifyEmail(request: SendEmailRequest,
                                   backgroundTasks: BackgroundTasks,
                                   authService: AuthService = Depends(Provide[Container.authService]),
                                   userService: UserService = Depends(Provide[Container.userService])):
    return authService.sendEmailToVerifyEmail(userService.getByEmail(request.email), backgroundTasks)

@router.post("/verify-email", response_model=bool)
@inject
async def verifyEmail(request: EmailVerificationRequest,
                    authService: AuthService = Depends(Provide[Container.authService]),
                    userService: UserService = Depends(Provide[Container.userService])):
    return authService.verifyEmail(userService.getByVerificationUUID(request.verification_uuid))

@router.post("/forgot-password/send-email", response_model=bool)
@inject
async def sendEmailToResetPassword(request: SendEmailRequest,
                                   backgroundTasks: BackgroundTasks,
                                   authService: AuthService = Depends(Provide[Container.authService]),
                                   userService: UserService = Depends(Provide[Container.userService])):
    return authService.sendEmailToResetPassword(userService.getByEmail(request.email), backgroundTasks)

@router.post("/forgot-password/reset-password", response_model=bool)
@inject
async def resetPassword(request: PasswordResetRequest,
                    authService: AuthService = Depends(Provide[Container.authService]),
                    userService: UserService = Depends(Provide[Container.userService])):
    return authService.resetPassword(userService.getByVerificationUUID(request.verification_uuid), pwd_context.hash(request.password.get_secret_value()))


