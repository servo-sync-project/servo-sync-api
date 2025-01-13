from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide
from device.mapping.movement_mapper import MovementMapper
from device.resource.request.movement_request import CreateMovementRequest, UpdateMovementRequest
from device.resource.response.movement_response import MovementResponse
from device.service.movement_service import MovementService
from security.domain.model.user import Role
from crosscutting.authorization import authorizeRoles
from core.container import Container

# Definir el router con prefijo y etiqueta
router = APIRouter(
    prefix="/api/v1/movements",
    tags=["movements"]
)

# Crear movimiento
@router.post("/", response_model=MovementResponse, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def createMovement(request: CreateMovementRequest,
                         movementService: MovementService = Depends(Provide[Container.movementService])):
    movement = movementService.create(MovementMapper.createRequestToModel(request))
    return MovementMapper.modelToResponse(movement)

@router.get("/robot/{robotId}", response_model=list[MovementResponse], dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def getAllMovementsByRobotId(robotId: int,
                                   movementService: MovementService = Depends(Provide[Container.movementService])):
    movements = movementService.getAllByRobotId(robotId)
    return [MovementMapper.modelToResponse(movement) for movement in movements]

# Actualizar movimiento por ID
@router.put("/{movementId}", response_model=MovementResponse, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def updateMovementById(movementId: int, 
                             request: UpdateMovementRequest,
                             movementService: MovementService = Depends(Provide[Container.movementService])):
    movement = movementService.updateById(movementId, request.name, request.coordinates and request.coordinates.model_dump_json())
    return MovementMapper.modelToResponse(movement)

# Eliminar movimiento por ID
@router.delete("/{movementId}", response_model=bool, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def deleteMovementById(movementId: int,
                             movementService: MovementService = Depends(Provide[Container.movementService])):
    return movementService.deleteById(movementId)

# ---------------- ENDPOINTS TRANSACCIONALES PARA EL ALMACENAMIENTO LOCAL DEL ROBOT-----------------
@router.put("/{movementId}/storage", response_model=bool, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def saveMovementInLocalById(movementId: int,
                                  movementService: MovementService = Depends(Provide[Container.movementService])):
    return movementService.saveMovementInLocalById(movementId)

# Eliminar movimiento por ID
@router.delete("/{movementId}/storage", response_model=bool, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def deleteMovementInLocalById(movementId: int,
                                    movementService: MovementService = Depends(Provide[Container.movementService])):
    return movementService.deleteMovementInLocalById(movementId)