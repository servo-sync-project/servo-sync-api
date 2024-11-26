import paho.mqtt.client as mqtt
from core.config import settings

mqttClient = mqtt.Client(client_id=settings.mqtt_client_id)
mqttClient.username_pw_set(settings.mqtt_username, settings.mqtt_password)
mqttClient.tls_set()
mqttClient.connect(settings.mqtt_broker_url, settings.mqtt_broker_port, 60)

