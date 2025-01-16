import logging
import os
from fastapi_mail import ConnectionConfig
from pydantic import DirectoryPath, Field, ValidationError
from pydantic_settings import BaseSettings
from uvicorn.config import LOGGING_CONFIG

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    api_version: str = Field("0.0.1", env="API_VERSION")
    debug_mode: bool = Field(False, env="DEBUG_MODE")

    database_url: str = Field(..., env="DATABASE_URL")
    origin_url: str = Field(..., env="ORIGIN_URL")
    initial_admin_email: str = Field(..., env="INITIAL_ADMIN_EMAIL")
    initial_admin_username: str = Field(..., env="INITIAL_ADMIN_USERNAME")
    initial_admin_password: str = Field(..., env="INITIAL_ADMIN_PASSWORD")
    secret_key: str = Field(..., env="SECRET_KEY")
    algorithm: str = Field("HS256", env="ALGORITHM")
    access_token_expire_minutes: int = Field(30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    unique_token_expire_days: int = Field(30, env="UNIQUE_TOKEN_EXPIRE_DAYS")
    verification_uuid_expire_days: int = Field(1, env="VERIFICATION_UUID_EXPIRE_DAYS")

    mqtt_broker_url: str = Field(..., env="MQTT_BROKER_URL")
    mqtt_broker_port: int = Field(8883, env="MQTT_BROKER_PORT")
    mqtt_client_id: str = Field(..., env="MQTT_CLIENT_ID")
    mqtt_username: str = Field(..., env="MQTT_USERNAME")
    mqtt_password: str = Field(..., env="MQTT_PASSWORD")

    # Configuraciones de correo electrónico
    mail_username: str = Field(..., env="MAIL_USERNAME")
    mail_password: str = Field(..., env="MAIL_PASSWORD")
    mail_from: str = Field(..., env="MAIL_FROM")
    mail_port: int = Field(587, env="MAIL_PORT")
    mail_server: str = Field("smtp.gmail.com", env="MAIL_SERVER")
    mail_starttls: bool = Field(True, env="MAIL_STARTTLS")
    mail_ssl_tls: bool = Field(False, env="MAIL_SSL_TLS")
    mail_template_folder: DirectoryPath = Field("./crosscutting/templates", env="MAIL_TEMPLATE_FOLDER")

    cloudinary_cloud_name: str = Field(..., env="CLOUDINARY_CLOUD_NAME")
    cloudinary_api_key: str = Field(..., env="CLOUDINARY_API_KEY")
    cloudinary_api_secret: str = Field(..., env="CLOUDINARY_API_SECRET")
    cloudinary_secure: bool = Field(True, env="CLOUDINARY_SECURE")

    class Config:
        env_file = ".env.prod" if os.getenv("ENV") == "prod" else ".env"

try:
    settings = Settings()
except ValidationError as e:
    logger.error("Error loading settings: %s", e.json())
    raise

# Configuración de FastAPI-Mail
def getEmailConfig():
    return ConnectionConfig(
        MAIL_USERNAME=settings.mail_username,
        MAIL_PASSWORD=settings.mail_password,
        MAIL_PORT=settings.mail_port,
        MAIL_SERVER=settings.mail_server,
        MAIL_STARTTLS=settings.mail_starttls,
        MAIL_SSL_TLS=settings.mail_ssl_tls,
        MAIL_FROM=settings.mail_from,
        MAIL_FROM_NAME="HumanSync",
        TEMPLATE_FOLDER=settings.mail_template_folder,
        USE_CREDENTIALS=True,
    )

LOGGING_CONFIG["formatters"]["default"] = {
    "()": "uvicorn.logging.DefaultFormatter",
    "format": "%(levelprefix)s %(asctime)s - %(name)s - %(message)s",
}

LOGGING_CONFIG["formatters"]["access"] = LOGGING_CONFIG["formatters"]["default"]

LOGGING_CONFIG["loggers"][""] = {
    "level": "INFO",
    "handlers": ["default"],
    "propagate": True,
}
    

