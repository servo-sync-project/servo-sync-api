# Etapa 1: Instalación de dependencias en un entorno virtual
FROM python:3.12.4-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN python -m venv .venv && \
    .venv/bin/pip install --no-cache-dir -r requirements.txt

# Etapa 2: Copia del código fuente y configuración del entorno de producción
FROM python:3.12.4-slim as runtime
WORKDIR /app
COPY --from=builder /app/.venv ./.venv
COPY . .

# Configuración del entorno virtual
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# Exponer el puerto y definir el punto de entrada
EXPOSE 8000
ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
