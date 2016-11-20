#!/bin/bash

source venv/bin/activate
git checkout server
git pull origin server
pip install -r requirements.txt
sudo systemctl restart gunicorn
