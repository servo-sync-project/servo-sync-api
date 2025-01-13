import json
from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide
from device.mapping.servo_group_mapper import ServoGroupMapper
from device.resource.request.servo_group_request import CreateServoGroupRequest, UpdateServoGroupNameRequest, UpdateServoGroupNumServosRequest
from device.resource.response.servo_group_response import ServoGroupResponse
from device.service.servo_group_service import ServoGroupService
from security.domain.model.user import Role
from crosscutting.authorization import authorizeRoles
from core.container import Container

# Definir el router con prefijo y etiqueta
router = APIRouter(
    prefix="/api/v1/servo-groups",
    tags=["servo-groups"]
)

@router.post("/", response_model=ServoGroupResponse, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def createServoGroup(request: CreateServoGroupRequest,
                           servoGroupService: ServoGroupService = Depends(Provide[Container.servoGroupService])):
    servoGroup = servoGroupService.create(ServoGroupMapper.createRequestToModel(request))
    return ServoGroupMapper.modelToResponse(servoGroup)

@router.get("/robot/{robotId}", response_model=list[ServoGroupResponse], dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def getAllServoGroupsByRobotId(robotId: int,
                            servoGroupService: ServoGroupService = Depends(Provide[Container.servoGroupService])):
    servoGroups = servoGroupService.getAllByRobotId(robotId)
    return [ServoGroupMapper.modelToResponse(servoGroup) for servoGroup in servoGroups]

@router.get("/{servoGroupId}", response_model=ServoGroupResponse, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def getServoGroupById(servoGroupId: int,
                            servoGroupService: ServoGroupService = Depends(Provide[Container.servoGroupService])):
    servoGroup = servoGroupService.getById(servoGroupId)
    return ServoGroupMapper.modelToResponse(servoGroup)

@router.put("/{servoGroupId}/increase", response_model=ServoGroupResponse, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def increaseServoGroupSequenceById(servoGroupId: int,
                                         servoGroupService: ServoGroupService = Depends(Provide[Container.servoGroupService])):
    servoGroup = servoGroupService.increaseSequenceById(servoGroupId)
    return ServoGroupMapper.modelToResponse(servoGroup)

@router.put("/{servoGroupId}/decrease", response_model=ServoGroupResponse, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def decreaseServoGroupSequenceById(servoGroupId: int,
                                         servoGroupService: ServoGroupService = Depends(Provide[Container.servoGroupService])):
    servoGroup = servoGroupService.decreaseSequenceById(servoGroupId)
    return ServoGroupMapper.modelToResponse(servoGroup)

@router.put("/{servoGroupId}/name", response_model=ServoGroupResponse, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def updateServoGroupNameById(servoGroupId: int, 
                                   request: UpdateServoGroupNameRequest,
                                   servoGroupService: ServoGroupService = Depends(Provide[Container.servoGroupService])):
    servoGroup = servoGroupService.updateNameById(servoGroupId, request.name)
    return ServoGroupMapper.modelToResponse(servoGroup)

@router.put("/{servoGroupId}/num-servos", response_model=ServoGroupResponse, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def updateServoGroupNumServosById(servoGroupId: int, 
                               request: UpdateServoGroupNumServosRequest,
                               servoGroupService: ServoGroupService = Depends(Provide[Container.servoGroupService])):
    servoGroup = servoGroupService.updateNumServosById(servoGroupId, request.num_servos)
    return ServoGroupMapper.modelToResponse(servoGroup)

@router.delete("/{servoGroupId}", response_model=bool, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def deleteServoGroupById(servoGroupId: int,
                               servoGroupService: ServoGroupService = Depends(Provide[Container.servoGroupService])):
    return servoGroupService.deleteById(servoGroupId)