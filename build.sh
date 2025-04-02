#!/usr/bin/env bash

# Instala Google Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt install -y ./google-chrome-stable_current_amd64.deb

# Descarga y configura ChromeDriver compatible
CHROME_VERSION=$(google-chrome --version | grep -oP '\d+\.\d+\.\d+' | head -1)
CHROMEDRIVER_VERSION=$(wget -qO- "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION")
wget -O chromedriver.zip "https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip"
unzip chromedriver.zip
mv chromedriver /usr/local/bin/chromedriver
chmod +x /usr/local/bin/chromedriver
