#!/usr/bin/env bash

# Instala dependencias necesarias
apt-get update
apt-get install -y wget unzip curl gnupg

# Instala Google Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt install -y ./google-chrome-stable_current_amd64.deb

# Obtener versión compatible de Chrome
CHROME_VERSION=$(google-chrome --version | grep -oP '\d+\.\d+\.\d+' | head -1)
CHROMEDRIVER_VERSION=$(curl -sS "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION")

# Descargar ChromeDriver y moverlo a /usr/local/bin
wget -O chromedriver.zip "https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip"
unzip chromedriver.zip
mv chromedriver /usr/local/bin/
chmod +x /usr/local/bin/chromedriver

# Limpieza
rm -f chromedriver.zip google-chrome-stable_current_amd64.deb
