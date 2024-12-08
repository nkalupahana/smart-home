#!/bin/bash

echo "Waiting for startup..."
sleep 60
cd ~/smart-home/curtains
screen -dm -S curtains-server -L -m bash -c "python3 -m gunicorn --workers 4 --timeout 120 --preload -b 0.0.0.0:8765 app:app"
