from fastapi import APIRouter, Depends
from device.mapping.position_mapper import PositionMapper
from device.resource.request.position_request import CreatePositionRequest, UpdatePositionRequest
from device.resource.response.position_response import PositionResponse
from security.domain.model.user import Role
from crosscutting.authorization import authorizeRoles
from core.container import Container

# Inyectar el contenedor
container = Container()
positionService = container.positionService()

# Definir el router con prefijo y etiqueta
router = APIRouter(
    prefix="/api/v1/positions",
    tags=["positions"]
)

# Crear posición
@router.post("/", response_model=PositionResponse, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
async def createPosition(request: CreatePositionRequest):
    position = positionService.create(PositionMapper.createRequestToModel(request))
    return PositionMapper.modelToResponse(position)

# @router.get("/all-by-movement/{movementId}", response_model=list[PositionResponse], dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
# async def getAllPositionsByMovementId(movementId: int):
#     positions = positionService.getAllByMovementId(movementId)
#     return [PositionMapper.modelToResponse(position) for position in positions]

# Actualizar posición por ID
@router.put("/{positionId}", response_model=PositionResponse, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
async def updatePositionById(positionId: int, request: UpdatePositionRequest):
    position = positionService.updateById(positionId, PositionMapper.updateRequestToModel(request))
    return PositionMapper.modelToResponse(position)

# Incrementar secuencia de posición por ID
@router.put("/{positionId}/increase", response_model=PositionResponse, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
async def increasePositionSequenceById(positionId: int):
    position = positionService.increaseSequenceById(positionId)
    return PositionMapper.modelToResponse(position)

# Decrementar secuencia de posición por ID
@router.put("/{positionId}/decrease", response_model=PositionResponse, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
async def decreasePositionSequenceById(positionId: int):
    position = positionService.decreaseSequenceById(positionId)
    return PositionMapper.modelToResponse(position)

# Eliminar posición por ID
@router.delete("/{positionId}", response_model=dict, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
async def deletePositionById(positionId: int):
    isDeleted = positionService.deleteById(positionId)
    return {"is_deleted": isDeleted}