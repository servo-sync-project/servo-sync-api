from dotenv import load_dotenv
from pydantic import Field, ValidationError
from pydantic_settings import BaseSettings
from crosscutting.logging import get_logger

load_dotenv()  

logger = get_logger(__name__)

class Settings(BaseSettings):
    api_version: str = Field(..., json_schema_extra={"env": "API_VERSION"})
    debug_mode: bool = Field(..., json_schema_extra={"env": "DEBUG_MODE"})

    database_url: str = Field(..., json_schema_extra={"env": "DATABASE_URL"})
    origin_url: str = Field(..., json_schema_extra={"env": "ORIGIN_URL"})
    initial_admin_image_url: str = Field(..., json_schema_extra={"env": "INITIAL_ADMIN_IMAGE_URL"})
    initial_admin_email: str = Field(..., json_schema_extra={"env": "INITIAL_ADMIN_EMAIL"})
    initial_admin_username: str = Field(..., json_schema_extra={"env": "INITIAL_ADMIN_USERNAME"})
    initial_admin_full_name: str = Field(..., json_schema_extra={"env": "INITIAL_ADMIN_FULL_NAME"})
    initial_admin_password: str = Field(..., json_schema_extra={"env": "INITIAL_ADMIN_PASSWORD"})
    secret_key: str = Field(..., json_schema_extra={"env": "SECRET_KEY"})
    algorithm: str = Field(..., json_schema_extra={"env": "ALGORITHM"})
    access_token_expire_minutes: int = Field(..., json_schema_extra={"env": "ACCESS_TOKEN_EXPIRE_MINUTES"})

    mqtt_broker_url: str = Field(..., json_schema_extra={"env": "MQTT_BROKER_URL"})
    mqtt_broker_port: int = Field(..., json_schema_extra={"env": "MQTT_BROKER_PORT"})
    mqtt_client_id: str = Field(..., json_schema_extra={"env": "MQTT_CLIENT_ID"})
    mqtt_username: str = Field(..., json_schema_extra={"env": "MQTT_USERNAME"})
    mqtt_password: str = Field(..., json_schema_extra={"env": "MQTT_PASSWORD"})

    class Config:
        env_file = ".env"

try:
    settings = Settings()
except ValidationError as e:
    logger.error("Error loading settings: %s", e.json())
    raise

