# constants.py
APP_NAME = "humansync_api"
TITLE = "HumanSync API"
DESCRIPTION = """
¡Bienvenido a la documentación de la API REST de control iot de robot asyncronico!

Esta API proporciona puntos finales para administrar preguntas, respuestas y comentarios en un sistema de preguntas y respuestas. Puede usar esta API para crear, recuperar, actualizar y eliminar registros. Las características principales incluyen:

- **Administración de robots**: crear una robot, recuperar una lista de robots, obtener detalles de un robot específica por su ID y eliminar robots.
- **Administración de movimmientos**: publicar una movimiento a un robot específico, recuperar todas los movimientos para una robot determinada, obtener detalles de un movimiento específico y eliminar movimientos.
- **Administración de posiciones**: agregar posiciones a los movimientos, recuperar todos las posiciones para un movimiento determinada y eliminar posiciones.

### Autenticación
Actualmente, esta API si requiere autenticación para proteger los puntos finales con mecanismos de autorización, aunque falta la correcta implementacion de la habilitacion por correo.

### Manejo de errores
La API proporciona mensajes de error significativos y códigos de estado HTTP para ayudarlo a comprender qué salió mal. Los códigos de estado comunes incluyen:
- **200 OK**: la solicitud fue exitosa.
- **201 Creado**: Se creó un nuevo recurso correctamente.
- **400 Solicitud incorrecta**: La solicitud no era válida o no se pudo atender de otra manera.
- **404 No encontrado**: No se pudo encontrar el recurso solicitado.
- **422 Entidad no procesable**: La solicitud estaba bien formada, pero no se pudo seguir debido a errores semánticos, como errores de validación en el cuerpo de la solicitud.
- **500 Error interno del servidor**: Se produjo un error en el servidor.

Explore los puntos finales a continuación para ver cómo puede integrar nuestra API en su aplicación. ¡Que disfrute codificando!
"""
CONTACT = {
    "name": "Johan J Huanca",
    "url": "https://www.linkedin.com/in/johan-huanca-nina-a76a2b204",
    "email": "j.huanca4141@gmail.com",
}
LICENSE_INFO = {
    "name": "MIT",
    "url": "https://opensource.org/licenses/MIT",
}
SWAGGER_UI_PARAMETERS = {"syntaxHighlight.theme": "obsidian"}
SWAGGER_FAVICON_URL = "https://example.com/your-favicon.ico" 
