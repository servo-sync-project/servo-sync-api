from fastapi import APIRouter, Depends
from device.mapping.movement_mapper import MovementMapper
from device.resource.request.movement_request import CreateMovementRequest, UpdateMovementRequest
from device.resource.response.movement_response import MovementResponse
from security.domain.model.user import Role
from crosscutting.authorization import authorizeRoles
from core.container import Container

# Inyectar el contenedor
container = Container()
movementService = container.movementService()

# Definir el router con prefijo y etiqueta
router = APIRouter(
    prefix="/api/v1/servo-groups",
    tags=["servo-groups"]
)

# Crear movimiento
@router.post("/", response_model=MovementResponse, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
async def createMovement(request: CreateMovementRequest):
    movement = movementService.create(MovementMapper.createRequestToModel(request))
    return MovementMapper.modelToResponse(movement)

@router.get("/{servoGroupId}", response_model=list[MovementResponse], dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
async def getMovementById(robotId: int):
    movements = movementService.getById(robotId)
    return [MovementMapper.modelToResponse(movement) for movement in movements]

# Actualizar movimiento por ID
@router.put("/{servoGroupId}", response_model=MovementResponse, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
async def updateMovementById(movementId: int, request: UpdateMovementRequest):
    movement = movementService.updateById(movementId, request.name, request.coord_x, request.coord_y)
    return MovementMapper.modelToResponse(movement)

# Eliminar movimiento por ID
@router.delete("/{servoGroupId}", response_model=dict, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
async def deleteMovementById(movementId: int):
    isDeleted = movementService.deleteById(movementId)
    return {"is_deleted": isDeleted}