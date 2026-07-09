#!/bin/bash
echo "Actualizando sistema"
sudo apt update && sudo apt upgrade -y
echo "Instalando Python"
sudo apt install pythonpy python3.14-venv git -y &&
echo "Actualizando repo"
git pull origin main
echo "Descargando mongo server"
wget "https://repo.mongodb.org/apt/ubuntu/dists/noble/mongodb-org/8.3/multiverse/binary-amd64/mongodb-org-server_8.3.4_amd64.deb"
echo "Instalando mongo server"
sudo apt install -y mongodb-org-server_8.3.4_amd64.deb
echo "Aplicando configuración"

SERVICE_FILE="/etc/systemd/system/mongod.service.d/override.conf"
sudo mkdir -p /etc/systemd/system/mongod.service.d/
printf "[Service]\nEnvironment=\"GLIBC_TUNABLES=glibc.pthread.rseq=1\"\n" | sudo tee $SERVICE_FILE
sudo systemctl daemon-reload
sudo systemctl restart mongod
echo "Configuración aplicada y servicio reiniciado."

