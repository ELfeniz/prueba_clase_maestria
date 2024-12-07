# Usar una imagen oficial de Python como base
FROM python:3.12-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Instalar las dependencias necesarias para psycopg2, scikit-learn, twisted-iocpsupport y otras librerías necesarias
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    g++ \
    nano \
    python3-dev \
    build-essential \
    tesseract-ocr \
    libtesseract-dev \
    nginx \
    poppler-utils \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Copiar el archivo de requisitos e instalar las dependencias de Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código fuente del backend al directorio de trabajo
COPY . /app/

# Copiar el archivo de configuración de Nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Exponer el puerto en el que correrá FastAPI
EXPOSE 80

# Comando para iniciar Nginx y Uvicorn (mejor para FastAPI que Gunicorn)
CMD ["sh", "-c", "service nginx start && uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4"]
