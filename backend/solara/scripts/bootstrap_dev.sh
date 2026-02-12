#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

cd "${PROJECT_DIR}"

python manage.py migrate
python manage.py bootstrap_dev_data \
  --superuser-username "${DJANGO_SUPERUSER_USERNAME:-admin}" \
  --superuser-email "${DJANGO_SUPERUSER_EMAIL:-admin@solara.local}" \
  --superuser-password "${DJANGO_SUPERUSER_PASSWORD:-admin123}" \
  --empresas "${SEED_EMPRESAS:-4}" \
  --usuarios-por-empresa "${SEED_USUARIOS_POR_EMPRESA:-8}" \
  --prefixo "${SEED_PREFIXO:-dev}"

printf '\nBootstrap concluido.\n'
printf 'Superadmin: %s\n' "${DJANGO_SUPERUSER_USERNAME:-admin}"
printf 'Senha superadmin: %s\n' "${DJANGO_SUPERUSER_PASSWORD:-admin123}"
