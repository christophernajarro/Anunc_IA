# Usamos una imagen base de Python
FROM python:3.9-slim

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos el archivo de dependencias e instalamos las dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto de los archivos de la aplicación
COPY . .

# Exponemos el puerto 8000 donde correrá FastAPI
EXPOSE 8000

# Comando para iniciar el servidor FastAPI (el comando de migración está en docker-compose.yml)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
