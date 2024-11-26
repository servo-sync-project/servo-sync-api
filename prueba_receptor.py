import os
import paho.mqtt.client as mqtt

# Configuración del broker MQTT
topic = "robot/+/access/#"
MQTT_BROKER_URL = os.getenv("MQTT_BROKER_URL")
MQTT_BROKER_PORT = int(os.getenv("MQTT_BROKER_PORT"))
MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")

# Crear la instancia del cliente MQTT
mqtt_client = mqtt.Client(client_id="cliente_prueba")
mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
mqtt_client.tls_set()  # Habilitar TLS para el puerto 8883

# Definir los callbacks
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado al broker MQTT")
        client.subscribe(topic)
    else:
        print(f"Conexión fallida. Código de retorno: {rc}")

def on_message(client, userdata, msg):
    print(f"Mensaje recibido del tópico '{msg.topic}': {msg.payload.decode()}")

def on_disconnect(client, userdata, rc):
    print("Desconectado del broker MQTT")

# Asignar los callbacks al cliente
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.on_disconnect = on_disconnect

# Conectar al broker MQTT
try:
    mqtt_client.connect(MQTT_BROKER_URL, MQTT_BROKER_PORT, 60)
    mqtt_client.loop_forever()  # Mantener la conexión activa para escuchar los mensajes
except Exception as e:
    print(f"Error al intentar conectar al broker MQTT: {e}")