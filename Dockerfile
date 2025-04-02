FROM python:3.11-slim

# Evitar prompts durante instalaciones
ENV DEBIAN_FRONTEND=noninteractive

# Instalar Chromium + fonts y dependencias necesarias para Selenium
RUN apt-get update && \
    apt-get install -y \
    chromium \
    chromium-driver \
    fonts-liberation \
    libnss3 \
    libgconf-2-4 \
    libxss1 \
    libappindicator1 \
    libindicator7 \
    wget \
    curl \
    gnupg2 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos del proyecto
COPY . .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Configurar variables de entorno
ENV PORT=10000
EXPOSE 10000

# Comando para ejecutar la app
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000"]
