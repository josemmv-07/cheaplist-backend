FROM python:3.11-slim

# Instalar Chromium y otras dependencias
RUN apt-get update && \
    apt-get install -y chromium chromium-driver && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos del proyecto
COPY . /app

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Puerto expuesto por la app
ENV PORT=10000
EXPOSE 10000

# Comando para ejecutar Flask con gunicorn
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000"]
