FROM python:3.12.4-slim
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 8000
ENTRYPOINT ["uvicorn", "main:app", "--reload", "--port=8000", "--host=0.0.0.0"]
