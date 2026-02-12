#!/usr/bin/env bash
set -euo pipefail

cd /workspaces/Solara/backend
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

cd /workspaces/Solara/backend/solara
python manage.py migrate
python manage.py bootstrap_dev_data \
  --superuser-username admin \
  --superuser-email admin@solara.local \
  --superuser-password admin123 \
  --empresas 4 \
  --usuarios-por-empresa 8
