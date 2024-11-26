import json
from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide
from device.mapping.robot_mapper import RobotMapper
from device.mapping.servo_group_mapper import ServoGroupMapper
from device.resource.request.robot_request import CreateRobotRequest, UpdateInitialPositionRequest, UpdateRobotRequest
from device.resource.response.robot_response import RobotResponse, RobotResponseForAll
from device.service.robot_service import RobotService
from device.service.servo_group_service import ServoGroupService
from security.domain.model.user import Role, User
from crosscutting.authorization import authorizeRoles, getAuthenticatedUser
from core.container import Container

# Definir el router con prefijo y etiqueta
router = APIRouter(
    prefix="/api/v1/robots",
    tags=["robots"]
)

@router.get("/botname/{botname}", response_model=RobotResponse, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def getRobotByBotname(botname: str,
                            authenticatedUser: User = Depends(getAuthenticatedUser), 
                            robotService: RobotService = Depends(Provide[Container.robotService])):
    robot = robotService.getByBotname(botname)
    robotService.validateAccess(authenticatedUser.id, robot.id)
    return RobotMapper.modelToResponse(robot)

@router.get("/my", response_model=list[RobotResponse], dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def getAllRobotsByMy(authenticatedUser: User = Depends(getAuthenticatedUser), 
                           robotService: RobotService = Depends(Provide[Container.robotService])):
    robots = robotService.getAllByUserId(authenticatedUser.id)
    return [RobotMapper.modelToResponse(robot) for robot in robots]

@router.post("/", response_model=RobotResponse, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def createRobot(request: CreateRobotRequest, 
                      authenticatedUser: User = Depends(getAuthenticatedUser), 
                      robotService: RobotService = Depends(Provide[Container.robotService])):
    robot, servoGroups = RobotMapper.createRequestToModel(request, authenticatedUser.id)
    robot = robotService.create(robot, servoGroups)
    return RobotMapper.modelToResponse(robot)

@router.get("/", response_model=list[RobotResponseForAll], dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def getAllRobotsWithoutPositions(robotService: RobotService = Depends(Provide[Container.robotService])):
    robots = robotService.getAll()
    return [RobotMapper.modelToResponseForAll(robot) for robot in robots]

@router.get("/{robotId}", response_model=RobotResponse, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def getRobotById(robotId: int,
                       authenticatedUser: User = Depends(getAuthenticatedUser), 
                       robotService: RobotService = Depends(Provide[Container.robotService])):
    robotService.validateAccess(authenticatedUser.id, robotId)
    robot = robotService.getById(robotId)
    return RobotMapper.modelToResponse(robot)

@router.put("/{robotId}", response_model=RobotResponse, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def updateRobotById(robotId: int, 
                          request: UpdateRobotRequest, 
                          authenticatedUser: User = Depends(getAuthenticatedUser), 
                          robotService: RobotService = Depends(Provide[Container.robotService])):
    robotService.validateAccess(authenticatedUser.id, robotId)
    robot = robotService.updateById(robotId, request.botname, request.image_url, request.description)
    return RobotMapper.modelToResponse(robot)

@router.put("/{robotId}/initial-position", response_model=RobotResponse, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def updateInitialPositionById(robotId: int, 
                                    newPosition: UpdateInitialPositionRequest, 
                                    authenticatedUser: User = Depends(getAuthenticatedUser), 
                                    robotService: RobotService = Depends(Provide[Container.robotService])):
    robotService.validateAccess(authenticatedUser.id, robotId)
    robot = robotService.updateInitialPositionById(robotId, json.dumps(newPosition.initial_position.model_dump()))
    return RobotMapper.modelToResponse(robot)

@router.delete("/{robotId}", response_model=bool, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def deleteRobotById(robotId: int, 
                          authenticatedUser: User = Depends(getAuthenticatedUser), 
                          robotService: RobotService = Depends(Provide[Container.robotService])):
    robotService.validateAccess(authenticatedUser.id, robotId)
    return robotService.deleteById(robotId)

@router.put("/{robotId}/move-initial-position", response_model=bool, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def moveToInitialPositionById(robotId: int, 
                                    authenticatedUser: User = Depends(getAuthenticatedUser), 
                                    robotService: RobotService = Depends(Provide[Container.robotService])):
    robotService.validateAccess(authenticatedUser.id, robotId)
    return robotService.moveToInitialPositionById(robotId)

# @router.put("/{robotId}/move-current-position", response_model=bool, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
# @inject
# async def updateAndMoveToCurrentPositionById(robotId: int, 
#                                              newPosition: UpdateCurrentPositionRequest, 
#                                              authenticatedUser: User = Depends(getAuthenticatedUser), 
#                                              robotService: RobotService = Depends(Provide[Container.robotService])):
#     robotService.validateAccess(authenticatedUser.id, robotId)
#     return robotService.updateAndMoveToCurrentPositionById(robotId, json.dumps(newPosition.current_position.model_dump()))

@router.put("/{robotId}/movements/name/{movementName}/execute", response_model=bool, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def executeByIdAndMovementName(robotId: int, 
                                      movementName: str, 
                                      authenticatedUser: User = Depends(getAuthenticatedUser), 
                                      robotService: RobotService = Depends(Provide[Container.robotService])):
    robotService.validateAccess(authenticatedUser.id, robotId)
    return robotService.executeByIdAndMovementName(robotId, movementName)

@router.put("/{robotId}/movements/name/{movementName}/save-data", response_model=bool, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def saveDataByIdAndMovementName(robotId: int, 
                                 movementName: str,
                                 authenticatedUser: User = Depends(getAuthenticatedUser), 
                                 robotService: RobotService = Depends(Provide[Container.robotService])):
    robotService.validateAccess(authenticatedUser.id, robotId)
    return robotService.saveDataByIdAndMovementName(robotId, movementName)
