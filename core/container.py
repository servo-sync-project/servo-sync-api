from dependency_injector import containers, providers
from device.domain.persistence.movement_repository import MovementRepository
from device.domain.persistence.position_repository import PositionRepository
from device.domain.persistence.servo_group_repository import ServoGroupRepository
from device.service.movement_service import MovementService
from device.service.position_service import PositionService
from device.service.servo_group_service import ServoGroupService
from security.domain.persistence.user_repository import UserRepository
from device.domain.persistence.robot_repository import RobotRepository
from security.service.auth_service import AuthService
from security.service.user_service import UserService
from device.service.robot_service import RobotService

class Container(containers.DeclarativeContainer):
    # Repositories
    userRepository = providers.Factory(UserRepository)
    robotRepository = providers.Factory(RobotRepository)
    servoGroupRepository = providers.Factory(ServoGroupRepository)
    movementRepository = providers.Factory(MovementRepository)
    positionRepository = providers.Factory(PositionRepository)
    
    # Services
    userService = providers.Factory(UserService, userRepository=userRepository)
    authService = providers.Factory(AuthService, userRepository=userRepository)
    
    robotService  = providers.Factory(RobotService, robotRepository=robotRepository, movementRepository=movementRepository, positionRepository=positionRepository)
    servoGroupService = providers.Factory(ServoGroupService, servoGroupRepository=servoGroupRepository)
    movementService = providers.Factory(MovementService, movementRepository=movementRepository)
    positionService = providers.Factory(PositionService, positionRepository=positionRepository)
    