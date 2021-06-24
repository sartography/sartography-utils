#!/bin/bash
export FLASK_APP=~/star-drive/backend/app/__init__.py
source ~/python-venv/bin/activate
cd ~/star-drive/backend/
flask db migrate
flask db upgrade
flask initdb
nohup flask run &
