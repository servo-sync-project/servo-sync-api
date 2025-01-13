FROM python:3.12.4-slim

WORKDIR /servo-sync-api

COPY . /servo-sync-api

RUN pip install -r requirements.txt

# Expone el puerto 8000
EXPOSE 8000

# Define el comando de entrada para ejecutar la aplicación FastAPI con Uvicorn
ENTRYPOINT ["uvicorn", "main:app", "--reload", "--port=8000", "--host=0.0.0.0"]
