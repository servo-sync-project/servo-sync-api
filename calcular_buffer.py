import json

# Datos simulados para probar
maximum_position = {
    "angles": [180] * 24,
    "delay": 1000
}

maximum_movement = {
    "name": "XXXX-XXXX-XXXX-XXXX-XXXX-XXXX-", 
    "positions": [maximum_position] * 16
}

# Convertir el payload simulado a una cadena JSON
simulated_payload_json = json.dumps([maximum_position])

# Calcular el tamaño del buffer necesario para el payload
buffer_size = len(simulated_payload_json.encode('utf-8'))

print(f"El tamaño del buffer necesario para el payload simulado es: {buffer_size} bytes")