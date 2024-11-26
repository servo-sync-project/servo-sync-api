from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from dependency_injector.wiring import inject, Provide
from security.domain.model.user import Role, User
from security.resource.request.update_password_request import UpdatePasswordRequest
from security.resource.request.update_user_request import UpdateUserRequest
from crosscutting.authorization import authorizeRoles, getAuthenticatedUser
from security.resource.response.user_response import UserResponse
from security.mapping.user_mapper import UserMapper
from security.service.user_service import UserService
from core.container import Container

# Definir el router con prefijo y etiqueta
router = APIRouter(
    prefix="/api/v1/users",
    tags=["users"]
)

# 1. Métodos estáticos o específicos
@router.get("/username/{username}", response_model=UserResponse, dependencies=[Depends(authorizeRoles([Role.ADMIN]))])
@inject
async def getUserBySearch(username: str, 
                          userService: UserService = Depends(Provide[Container.userService])):
    user = userService.getByUsername(username)
    return UserMapper.modelToResponse(user)

@router.get("/me", response_model=UserResponse, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def getMyUser(authenticatedUser: User = Depends(getAuthenticatedUser)):
    return UserMapper.modelToResponse(authenticatedUser)

@router.put("/me", response_model=UserResponse, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def updateMyUser(request: UpdateUserRequest, 
                       authenticatedUser: User = Depends(getAuthenticatedUser), 
                       userService: UserService = Depends(Provide[Container.userService])):
    user = userService.updateById(authenticatedUser.id, request.username, request.full_name)
    return UserMapper.modelToResponse(user)

@router.put("/me/password", response_model=UserResponse, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def updateMyPassword(request: UpdatePasswordRequest, 
                           authenticatedUser: User = Depends(getAuthenticatedUser), 
                           userService: UserService = Depends(Provide[Container.userService])):
    user = userService.updatePasswordById(authenticatedUser.id, request.password)
    return UserMapper.modelToResponse(user)

@router.delete("/me", response_model=bool, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def deleteMyUser(authenticatedUser: User = Depends(getAuthenticatedUser), 
                       userService: UserService = Depends(Provide[Container.userService])):
    return userService.deleteById(authenticatedUser.id)


# 2. Métodos dinámicos
@router.get("/{userId}", response_model=UserResponse, dependencies=[Depends(authorizeRoles([Role.ADMIN]))])
@inject
async def getUserById(userId: int, 
                      userService: UserService = Depends(Provide[Container.userService])):
    user = userService.getById(userId)
    return UserMapper.modelToResponse(user)
    
# Actualizar usuario por ID (solo accesible por ADMIN)
@router.put("/{userId}", response_model=UserResponse, dependencies=[Depends(authorizeRoles([Role.ADMIN]))])
@inject
async def updateUserById(userId: int, 
                         request: UpdateUserRequest, 
                         userService: UserService = Depends(Provide[Container.userService])):
    user = userService.updateById(userId, request.username, request.full_name)
    return UserMapper.modelToResponse(user)

# Eliminar usuario por ID (solo accesible por ADMIN)
@router.delete("/{userId}", response_model=dict, dependencies=[Depends(authorizeRoles([Role.ADMIN]))])
@inject
async def deleteUserById(userId: int, 
                         userService: UserService = Depends(Provide[Container.userService])):
    return userService.deleteById(userId)

# 3. Rutas generales
@router.get("/", response_model=list[UserResponse], dependencies=[Depends(authorizeRoles([Role.ADMIN]))])
@inject
async def getAllUsers(userService: UserService = Depends(Provide[Container.userService])):
    users = userService.getAll()
    return [UserMapper.modelToResponse(user) for user in users]
