#!/usr/bin/env bash

# Instala dependencias necesarias
apt-get update
apt-get install -y wget unzip curl gnupg

# Instala Google Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt install -y ./google-chrome-stable_current_amd64.deb

# Limpieza
rm -f google-chrome-stable_current_amd64.deb
