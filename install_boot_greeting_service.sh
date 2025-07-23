#!/bin/bash

echo "Moving kidprinter-boot-greeting.service to /etc/systemd/system/"
sudo mv /home/khadas/kidprinter/kidprinter-boot-greeting.service /etc/systemd/system/

echo "Reloading systemd daemon..."
sudo systemctl daemon-reload

echo "Enabling kidprinter-boot-greeting.service..."
sudo systemctl enable kidprinter-boot-greeting.service

echo "Starting kidprinter-boot-greeting.service..."
sudo systemctl start kidprinter-boot-greeting.service

echo "Service installation complete."
