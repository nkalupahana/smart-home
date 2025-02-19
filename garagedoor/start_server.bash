#!/bin/bash

echo "Waiting for startup..."
sleep 60
cd ~/smart-home/garagedoor
screen -dm -S garagedoor-server -L -m bash -c "python3 -m gunicorn --workers 1 -b 0.0.0.0:8765 app:app"
