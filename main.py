from contextlib import asynccontextmanager
import logging
import debugpy
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from sqlmodel import SQLModel
import uvicorn
from core.constants import TITLE, DESCRIPTION, CONTACT, LICENSE_INFO, SWAGGER_UI_PARAMETERS, SWAGGER_FAVICON_URL

from security.api.rest.auth_controller import router as AuthController
from security.api.rest.user_controller import router as UserController

from device.api.rest.robot_controller import router as RobotController
from device.api.rest.servo_group_controller import router as ServoGroupController
from device.api.rest.movement_controller import router as MovementController
from device.api.rest.position_controller import router as PositionController

from core.container import Container
from core.default_data import defaultData
from core.database import engine
from crosscutting.mqtt_client import mqttClient
from core.config import settings

logger = logging.getLogger(__name__)

container = Container()
robotService = container.robotService()
userRepository = container.userRepository()

# Configuración de callbacks para MQTT
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info("Conectado al broker MQTT")
        mqttClient.subscribe("robot/+/access/status")
        mqttClient.subscribe("robot/+/access/positions")
        mqttClient.subscribe("robot/+/access/storage/#")
    else:
        logger.info(f"Conexión fallida. Código de retorno: {rc}")

def on_message(client, userdata, msg):
    topicParts = msg.topic.split('/')
    robotToken = topicParts[1]

    if msg.topic.endswith("/access/status"):
        if msg.payload.decode() == "offline":
            logger.info(f"Robot {robotToken} se ha desconectado")
            robotService.updateConnectionStatusByUUID(robotToken, False)
        elif msg.payload.decode() == "online":
            logger.info(f"Robot {robotToken} se ha conectado")
            robotService.updateConnectionStatusByUUID(robotToken, True)
        logger.info(f"Status recibido del robot {robotToken}: {msg.payload.decode()}")
    elif msg.topic.endswith("/access/positions"):
        logger.info(f"posiciones recibido para robot {robotToken}: {msg.payload.decode()}")
    elif msg.topic.endswith("/access/storage/save-movement"):
        logger.info(f"comando de almacenamiento recibido para robot {robotToken}: {msg.payload.decode()}")
    elif msg.topic.endswith("/access/storage/delete-movement"):
        logger.info(f"comando de almacenamiento recibido para robot {robotToken}: {msg.payload.decode()}")
    elif msg.topic.endswith("/access/storage/save-initial-position"):
        logger.info(f"comando de almacenamiento recibido para robot {robotToken}: {msg.payload.decode()}")
    elif msg.topic.endswith("/access/storage/clear"):
        logger.info(f"comando de almacenamiento recibido para robot {robotToken}: {msg.payload.decode()}")

def on_disconnect(client, userdata, rc):
    logger.info("Desconectado del broker MQTT")

# Lifespan handler para manejar el ciclo de vida de la aplicación
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Iniciar tablas de la base de datos
    SQLModel.metadata.create_all(engine)
    defaultData(userRepository)
    # Configurar el contenedor para la inyección de dependencias
    container.wire(modules=[
        "security.api.rest.auth_controller",
        "security.api.rest.user_controller",
        "device.api.rest.robot_controller",
        "device.api.rest.servo_group_controller",
        "device.api.rest.movement_controller",
        "device.api.rest.position_controller"
    ])

    mqttClient.on_connect = on_connect
    mqttClient.on_message = on_message
    mqttClient.on_disconnect = on_disconnect
    mqttClient.loop_start()
    # Yield permite que la aplicación ejecute normalmente después de que el contexto se ha configurado
    yield

    # Cuando la aplicación se cierra, paramos el loop de MQTT
    mqttClient.loop_stop()
    mqttClient.disconnect()

def create_app():
    # Crear la aplicación FastAPI utilizando el lifespan handler
    app = FastAPI(
        title=TITLE,
        description=DESCRIPTION,
        version="0.1",
        contact=CONTACT,
        license_info=LICENSE_INFO,
        swagger_ui_parameters=SWAGGER_UI_PARAMETERS,
        swagger_favicon_url=SWAGGER_FAVICON_URL,
        lifespan=lifespan
    )

    app.include_router(AuthController)
    app.include_router(UserController)
    app.include_router(RobotController)
    app.include_router(ServoGroupController)
    app.include_router(MovementController)
    app.include_router(PositionController)
    
    app.add_middleware(
        CORSMiddleware,
        #allow_origins=settings.origin_url,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    return app

app = create_app()

@app.get("/", include_in_schema=False, response_class=RedirectResponse)
async def redirect_to_swagger():    
    logger.info("Redirect to swagger...")
    return RedirectResponse(url="/docs")
    
if __name__ == "__main__":
    if settings.debug_mode == True:
        debugpy.listen(("0.0.0.0", 5678))
        debugpy.wait_for_client()
    uvicorn.run(app, host="0.0.0.0", port=8000)