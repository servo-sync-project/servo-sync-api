from security.domain.model.user import User
from security.mapping.user_mapper import UserMapper
from security.resource.request.auth_request import RegisterUserRequest
from security.resource.response.auth_response import AuthResponse, AuthResponseForRefresh 
from security.service.auth_service import pwd_context

class AuthMapper:    
    @staticmethod
    def registerRequestToModel(request: RegisterUserRequest) -> User:
        return User(email=request.email, 
                    username=request.username, 
                    hashed_password=pwd_context.hash(request.password.get_secret_value()))
    
    @staticmethod
    def modelToResponseWithTokens(user: User, accessToken: str) -> AuthResponse:
        userResponse = UserMapper.modelToResponse(user)
        return AuthResponse(access_token=accessToken, 
                            unique_token=user.unique_token, 
                            user=userResponse)
    
    @staticmethod
    def modelToResponseWithAccessToken(user: User, accessToken: str) -> AuthResponse:
        userResponse = UserMapper.modelToResponse(user)
        return AuthResponseForRefresh(access_token=accessToken, 
                                      user=userResponse)

