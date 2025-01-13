import json
from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide
from device.mapping.position_mapper import PositionMapper
from device.resource.request.position_request import CreatePositionRequest, UpdatePositionRequest
from device.resource.response.position_response import PositionResponse
from device.service.position_service import PositionService
from security.domain.model.user import Role
from crosscutting.authorization import authorizeRoles
from core.container import Container

# Definir el router con prefijo y etiqueta
router = APIRouter(
    prefix="/api/v1/positions",
    tags=["positions"]
)

# Crear posición
@router.post("/", response_model=PositionResponse, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def createPosition(request: CreatePositionRequest,
                         positionService: PositionService = Depends(Provide[Container.positionService])):
    position = positionService.create(PositionMapper.createRequestToModel(request))
    return PositionMapper.modelToResponse(position)

@router.get("/movement/{movementId}", response_model=list[PositionResponse], dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def getAllPositionsByMovementId(movementId: int,
                                      positionService: PositionService = Depends(Provide[Container.positionService])):
    positions = positionService.getAllByMovementId(movementId)
    return [PositionMapper.modelToResponse(position) for position in positions]

# Incrementar secuencia de posición por ID
@router.put("/{positionId}/increase", response_model=PositionResponse, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def increasePositionSequenceById(positionId: int,
                                       positionService: PositionService = Depends(Provide[Container.positionService])):
    position = positionService.increaseSequenceById(positionId)
    return PositionMapper.modelToResponse(position)

# Decrementar secuencia de posición por ID
@router.put("/{positionId}/decrease", response_model=PositionResponse, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def decreasePositionSequenceById(positionId: int,
                                       positionService: PositionService = Depends(Provide[Container.positionService])):
    position = positionService.decreaseSequenceById(positionId)
    return PositionMapper.modelToResponse(position)

# Actualizar posición por ID
@router.put("/{positionId}", response_model=PositionResponse, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def updatePositionById(positionId: int, 
                             request: UpdatePositionRequest,
                             positionService: PositionService = Depends(Provide[Container.positionService])):
    position = positionService.updateById(positionId, request.delay, json.dumps(request.angles))
    return PositionMapper.modelToResponse(position)

# Eliminar posición por ID
@router.delete("/{positionId}", response_model=bool, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def deletePositionById(positionId: int,
                             positionService: PositionService = Depends(Provide[Container.positionService])):
    return positionService.deleteById(positionId)