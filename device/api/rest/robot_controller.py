from fastapi import APIRouter, Depends, File, UploadFile
from dependency_injector.wiring import inject, Provide
from device.mapping.robot_mapper import RobotMapper
from device.resource.request.robot_request import CreateRobotRequest, UpdateCurrentPositionRequest, UpdateInitialPositionRequest, UpdateRobotRequest
from device.resource.response.robot_response import RobotResponse, RobotResponseForAll
from device.service.robot_service import RobotService
from security.domain.model.user import Role, User
from crosscutting.authorization import authorizeRoles, getAuthenticatedUser
from core.container import Container

# Definir el router con prefijo y etiqueta
router = APIRouter(
    prefix="/api/v1/robots",
    tags=["robots"]
)

@router.get("/uuid/{uniqueUid}", response_model=RobotResponse, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def getRobotByUniqueUid(uniqueUid: str,
                            authenticatedUser: User = Depends(getAuthenticatedUser), 
                            robotService: RobotService = Depends(Provide[Container.robotService])):
    robot = robotService.getByUniqueUid(uniqueUid)
    robotService.validateAccess(authenticatedUser.id, robot.id)
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
                          robotService: RobotService = Depends(Provide[Container.robotService])):
    robotService.validateAccess(authenticatedUser.id, robotId)
    robot = robotService.updateById(robotId, request.botname, request.description)
    return RobotMapper.modelToResponse(robot)

@router.put("/{robotId}/image", response_model=RobotResponse, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def updateImageById(robotId: int, 
                          imageFile: UploadFile,
                          authenticatedUser: User = Depends(getAuthenticatedUser), 
                          robotService: RobotService = Depends(Provide[Container.robotService])):
    robotService.validateAccess(authenticatedUser.id, robotId)
    robot = robotService.updateImageById(robotId, imageFile)
    return RobotMapper.modelToResponse(robot)

@router.put("/{robotId}/config-image", response_model=RobotResponse, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def updateConfigImageById(robotId: int, 
                                configImageFile: UploadFile,
                                authenticatedUser: User = Depends(getAuthenticatedUser), 
                                robotService: RobotService = Depends(Provide[Container.robotService])):
    robotService.validateAccess(authenticatedUser.id, robotId)
    robot = robotService.updateConfigImageById(robotId, configImageFile)
    return RobotMapper.modelToResponse(robot)

@router.delete("/{robotId}", response_model=bool, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def deleteRobotById(robotId: int, 
                          authenticatedUser: User = Depends(getAuthenticatedUser), 
                          robotService: RobotService = Depends(Provide[Container.robotService])):
    robotService.validateAccess(authenticatedUser.id, robotId)
    return robotService.deleteById(robotId)

@router.post("/{robotId}/move/initial-position", response_model=bool, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def moveToInitialPositionById(robotId: int,
                                             authenticatedUser: User = Depends(getAuthenticatedUser), 
                                             robotService: RobotService = Depends(Provide[Container.robotService])):
    robotService.validateAccess(authenticatedUser.id, robotId)
    return robotService.moveToInitialPositionById(robotId)

@router.put("/{robotId}/move/initial-position", response_model=RobotResponse, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def updateAndmoveToInitialPositionById(robotId: int, 
                                             newPosition: UpdateInitialPositionRequest, 
                                             authenticatedUser: User = Depends(getAuthenticatedUser), 
                                             robotService: RobotService = Depends(Provide[Container.robotService])):
    robotService.validateAccess(authenticatedUser.id, robotId)
    robot = robotService.updateAndmoveToInitialPositionById(robotId, newPosition.initial_position.model_dump_json())
    return RobotMapper.modelToResponse(robot)

@router.put("/{robotId}/move/current-position", response_model=RobotResponse, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def updateAndMoveToCurrentPositionById(robotId: int, 
                                             newPosition: UpdateCurrentPositionRequest, 
                                             authenticatedUser: User = Depends(getAuthenticatedUser), 
                                             robotService: RobotService = Depends(Provide[Container.robotService])):
    robotService.validateAccess(authenticatedUser.id, robotId)
    robot = robotService.updateAndMoveToCurrentPositionById(robotId, newPosition.current_position.model_dump_json())
    return RobotMapper.modelToResponse(robot)

@router.post("/{robotId}/movements/{movementId}/execute", response_model=bool, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def executeMovementByIdAndYourId(robotId: int, 
                                       movementId: int, 
                                       authenticatedUser: User = Depends(getAuthenticatedUser), 
                                       robotService: RobotService = Depends(Provide[Container.robotService])):
    robotService.validateAccess(authenticatedUser.id, robotId)
    return robotService.executeMovementByIdAndYourId(robotId, movementId)

@router.post("/{robotId}/movements/positions/{positionId}/move", response_model=bool, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def moveToPositionByIdAndYourId(robotId: int, 
                                      positionId: int, 
                                      authenticatedUser: User = Depends(getAuthenticatedUser), 
                                      robotService: RobotService = Depends(Provide[Container.robotService])):
    robotService.validateAccess(authenticatedUser.id, robotId)
    return robotService.moveToPositionByIdAndYourId(robotId, positionId)

# ---------------- ENDPOINTS TRANSACCIONALES PARA EL ALMACENAMIENTO LOCAL DEL ROBOT-----------------
@router.put("/{robotId}/storage/initial-position", response_model=bool, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def saveInitialPositionInLocalById(robotId: int, 
                                         authenticatedUser: User = Depends(getAuthenticatedUser), 
                                         robotService: RobotService = Depends(Provide[Container.robotService])):
    robotService.validateAccess(authenticatedUser.id, robotId)
    return robotService.saveInitialPositionInLocalById(robotId)

@router.delete("/{robotId}/storage", response_model=bool, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def clearLocalStorageById(robotId: int, 
                                authenticatedUser: User = Depends(getAuthenticatedUser), 
                                robotService: RobotService = Depends(Provide[Container.robotService])):
    robotService.validateAccess(authenticatedUser.id, robotId)
    return robotService.clearLocalStorageById(robotId)