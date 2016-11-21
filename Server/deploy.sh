#!/bin/bash
set -e

source venv/bin/activate
branch=$1

git fetch
git checkout $branch
git pull origin $branch

pip install -r requirements.txt
sudo systemctl restart gunicorn
