from fastapi import APIRouter, Depends, File, UploadFile
from dependency_injector.wiring import inject, Provide
from device.mapping.robot_mapper import RobotMapper
from device.resource.request.robot_request import CreateRobotRequest, UpdateCurrentPositionRequest, UpdateInitialPositionRequest, UpdateRobotRequest
from device.resource.response.robot_response import RobotResponse, RobotResponseForAll
from device.service.movement_service import MovementService
from device.service.position_service import PositionService
from device.service.robot_service import RobotService
from security.domain.model.user import Role, User
from crosscutting.authorization import authorizeRoles, getAuthenticatedUser
from core.container import Container
from security.service.user_service import UserService

# Definir el router con prefijo y etiqueta
router = APIRouter(
    prefix="/api/v1/robots",
    tags=["robots"]
)

@router.get("/uuid/{uniqueUid}", response_model=RobotResponse, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def getRobotByUniqueUid(uniqueUid: str,
                            authenticatedUser: User = Depends(getAuthenticatedUser), 
                            robotService: RobotService = Depends(Provide[Container.robotService]),
                            userService: UserService = Depends(Provide[Container.userService])):
    robot = robotService.getByUniqueUid(uniqueUid)
    userService.validateRobotAccess(authenticatedUser.id, robot.id)
    return RobotMapper.modelToResponse(robot)

@router.get("/my", response_model=list[RobotResponse], dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def getAllRobotsByMy(authenticatedUser: User = Depends(getAuthenticatedUser), 
                           robotService: RobotService = Depends(Provide[Container.robotService])):
    robots = robotService.getAllByUserId(authenticatedUser.id)
    return [RobotMapper.modelToResponse(robot) for robot in robots]

@router.get("/", response_model=list[RobotResponseForAll], dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def getAllRobotsForAll(robotService: RobotService = Depends(Provide[Container.robotService])):
    robots = robotService.getAll()
    return [RobotMapper.modelToResponseForAll(robot) for robot in robots]

@router.post("/", response_model=RobotResponse, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def createRobot(request: CreateRobotRequest, 
                      authenticatedUser: User = Depends(getAuthenticatedUser), 
                      robotService: RobotService = Depends(Provide[Container.robotService])):
    robot = robotService.create(RobotMapper.createRequestToModel(request, authenticatedUser.id))
    return RobotMapper.modelToResponse(robot)

@router.put("/{robotId}", response_model=RobotResponse, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def updateRobotById(robotId: int, 
                          request: UpdateRobotRequest, 
                          authenticatedUser: User = Depends(getAuthenticatedUser), 
                          robotService: RobotService = Depends(Provide[Container.robotService]),
                          userService: UserService = Depends(Provide[Container.userService])):
    userService.validateRobotAccess(authenticatedUser.id, robotId)
    robot = robotService.update(robotService.getById(robotId), request.botname, request.description)
    return RobotMapper.modelToResponse(robot)

@router.put("/{robotId}/image", response_model=RobotResponse, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def updateImageById(robotId: int, 
                          imageFile: UploadFile,
                          authenticatedUser: User = Depends(getAuthenticatedUser), 
                          robotService: RobotService = Depends(Provide[Container.robotService]),
                          userService: UserService = Depends(Provide[Container.userService])):
    userService.validateRobotAccess(authenticatedUser.id, robotId)
    robot = robotService.updateImage(robotService.getById(robotId), imageFile)
    return RobotMapper.modelToResponse(robot)

@router.put("/{robotId}/config-image", response_model=RobotResponse, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def updateConfigImageById(robotId: int, 
                                configImageFile: UploadFile,
                                authenticatedUser: User = Depends(getAuthenticatedUser), 
                                robotService: RobotService = Depends(Provide[Container.robotService]),
                                userService: UserService = Depends(Provide[Container.userService])):
    userService.validateRobotAccess(authenticatedUser.id, robotId)
    robot = robotService.updateConfigImage(robotService.getById(robotId), configImageFile)
    return RobotMapper.modelToResponse(robot)

@router.delete("/{robotId}", response_model=bool, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def deleteRobotById(robotId: int, 
                          authenticatedUser: User = Depends(getAuthenticatedUser), 
                          robotService: RobotService = Depends(Provide[Container.robotService]),
                          userService: UserService = Depends(Provide[Container.userService])):
    userService.validateRobotAccess(authenticatedUser.id, robotId)
    return robotService.delete(robotService.getById(robotId))

@router.post("/{robotId}/move/initial-position", response_model=bool, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def moveToInitialPositionById(robotId: int,
                                    authenticatedUser: User = Depends(getAuthenticatedUser), 
                                    robotService: RobotService = Depends(Provide[Container.robotService]),
                                    userService: UserService = Depends(Provide[Container.userService])):
    userService.validateRobotAccess(authenticatedUser.id, robotId)
    return robotService.moveToInitialPosition(robotService.getById(robotId))

@router.put("/{robotId}/move/initial-position", response_model=RobotResponse, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def updateAndmoveToInitialPositionById(robotId: int, 
                                             newPosition: UpdateInitialPositionRequest, 
                                             authenticatedUser: User = Depends(getAuthenticatedUser), 
                                             robotService: RobotService = Depends(Provide[Container.robotService]),
                                             userService: UserService = Depends(Provide[Container.userService])):
    userService.validateRobotAccess(authenticatedUser.id, robotId)
    robot = robotService.updateAndmoveToInitialPosition(robotService.getById(robotId), newPosition.initial_position.model_dump_json())
    return RobotMapper.modelToResponse(robot)

@router.put("/{robotId}/move/current-position", response_model=RobotResponse, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def updateAndMoveToCurrentPositionById(robotId: int, 
                                             newPosition: UpdateCurrentPositionRequest, 
                                             authenticatedUser: User = Depends(getAuthenticatedUser), 
                                             robotService: RobotService = Depends(Provide[Container.robotService]),
                                             userService: UserService = Depends(Provide[Container.userService])):
    userService.validateRobotAccess(authenticatedUser.id, robotId)
    robot = robotService.updateAndMoveToCurrentPosition(robotService.getById(robotId), newPosition.current_position.model_dump_json())
    return RobotMapper.modelToResponse(robot)

@router.post("/{robotId}/movements/{movementId}/execute", response_model=bool, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def executeMovementByIdAndYourId(robotId: int, 
                                       movementId: int, 
                                       authenticatedUser: User = Depends(getAuthenticatedUser), 
                                       robotService: RobotService = Depends(Provide[Container.robotService]),
                                       userService: UserService = Depends(Provide[Container.userService])):
    userService.validateRobotAccess(authenticatedUser.id, robotId)
    return robotService.executeMovementById(robotService.validateMovementAccess(robotId, movementId), movementId)

@router.post("/{robotId}/movements/positions/{positionId}/move", response_model=bool, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def moveToPositionByIdAndYourId(robotId: int, 
                                      positionId: int, 
                                      authenticatedUser: User = Depends(getAuthenticatedUser), 
                                      robotService: RobotService = Depends(Provide[Container.robotService]),
                                      userService: UserService = Depends(Provide[Container.userService])):
    userService.validateRobotAccess(authenticatedUser.id, robotId)
    return robotService.moveToPositionById(robotService.validatePositionAccess(robotId, positionId), positionId)

# ---------------- ENDPOINTS TRANSACCIONALES PARA EL ALMACENAMIENTO LOCAL DEL ROBOT-----------------
@router.put("/{robotId}/storage/movements/{movementId}", response_model=bool, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def saveMovementInLocalByIdAndYourId(robotId: int, 
                                  movementId: int,
                                  authenticatedUser: User = Depends(getAuthenticatedUser), 
                                  robotService: RobotService = Depends(Provide[Container.robotService]),
                                  userService: UserService = Depends(Provide[Container.userService])):
    userService.validateRobotAccess(authenticatedUser.id, robotId)
    return robotService.saveMovementInLocal(robotService.validateMovementAccess(robotId, movementId), movementId)

# Eliminar movimiento por ID
@router.delete("/{robotId}/storage/movements/{movementId}", response_model=bool, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def deleteMovementInLocalByIdAndYourId(robotId: int, 
                                    movementId: int,
                                    authenticatedUser: User = Depends(getAuthenticatedUser), 
                                    robotService: RobotService = Depends(Provide[Container.robotService]),
                                    userService: UserService = Depends(Provide[Container.userService])):
    userService.validateRobotAccess(authenticatedUser.id, robotId)
    return robotService.deleteMovementInLocal(robotService.validateMovementAccess(robotId, movementId), movementId)

@router.put("/{robotId}/storage/initial-position", response_model=bool, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def saveInitialPositionInLocalById(robotId: int, 
                                         authenticatedUser: User = Depends(getAuthenticatedUser), 
                                         robotService: RobotService = Depends(Provide[Container.robotService]),
                                         userService: UserService = Depends(Provide[Container.userService])):
    userService.validateRobotAccess(authenticatedUser.id, robotId)
    return robotService.saveInitialPositionInLocal(robotService.getById(robotId))

@router.delete("/{robotId}/storage", response_model=bool, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def clearLocalStorageById(robotId: int, 
                                authenticatedUser: User = Depends(getAuthenticatedUser), 
                                robotService: RobotService = Depends(Provide[Container.robotService]),
                                userService: UserService = Depends(Provide[Container.userService])):
    userService.validateRobotAccess(authenticatedUser.id, robotId)
    return robotService.clearLocalStorage(robotService.getById(robotId))