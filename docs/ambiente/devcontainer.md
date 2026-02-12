# Ambiente de Desenvolvimento com Dev Container

Este guia configura um ambiente completo para o backend Django com:

- VS Code Dev Container
- PostgreSQL em container dedicado
- extensoes de Python para produtividade
- Thunder Client para teste de API
- bootstrap automatico (migrations + superadmin + seed de empresas/usuarios)

## 1. Arquivos 

- `.devcontainer/devcontainer.json`
- `.devcontainer/docker-compose.yml`
- `.devcontainer/Dockerfile`
- `.devcontainer/post-create.sh`
- `backend/solara/scripts/bootstrap_dev.sh`
- `backend/solara/contas/management/commands/bootstrap_dev_data.py`
- `backend/solara/.env.example`

## 2. Como subir o ambiente

1. Abra o projeto no VS Code.
2. Execute `Dev Containers: Reopen in Container`.
3. Aguarde o `postCreateCommand` finalizar.

O `post-create.sh` faz:

1. instala dependencias do backend
2. executa `python manage.py migrate`
3. executa `python manage.py bootstrap_dev_data ...`

## 3. Servicos no compose

- `app`: container de desenvolvimento Python
- `db`: PostgreSQL 16

Variaveis principais do banco no container:

- `DB_ENGINE=postgres`
- `DB_NAME=solara`
- `DB_USER=solara`
- `DB_PASSWORD=solara`
- `DB_HOST=db`
- `DB_PORT=5432`

## 4. Rodar o servidor Django

No terminal do container:

```bash
cd backend/solara
python manage.py runserver 0.0.0.0:8000
```

## 5. Seed de dados e superadmin

O comando de seed e idempotente (pode rodar varias vezes sem duplicar por username).

### Comando direto

```bash
cd backend/solara
python manage.py bootstrap_dev_data \
  --superuser-username admin \
  --superuser-email admin@solara.local \
  --superuser-password admin123 \
  --empresas 4 \
  --usuarios-por-empresa 8 \
  --prefixo dev
```

### Script pronto

```bash
cd backend/solara
./scripts/bootstrap_dev.sh
```

### Variaveis para customizacao

- `DJANGO_SUPERUSER_USERNAME`
- `DJANGO_SUPERUSER_EMAIL`
- `DJANGO_SUPERUSER_PASSWORD`
- `SEED_EMPRESAS`
- `SEED_USUARIOS_POR_EMPRESA`
- `SEED_PREFIXO`

## 6. Dados gerados

- 1 superadmin (`admin` por padrao)
- N empresas (`--empresas`)
- M usuarios por empresa (`--usuarios-por-empresa`)
- perfis rotacionados por empresa:
  - `GERENTE`
  - `ANALISTA_ENERGETICO`
  - `ANALISTA_FINANCEIRO`
  - `INVESTIDOR`
  - `CONSUMIDOR`

Senha padrao dos usuarios seed (empresa e pessoa):

- `Senha@123456`

## 7. Extensoes instaladas no container

- `ms-python.python`
- `ms-python.vscode-pylance`
- `ms-python.debugpy`
- `ms-python.black-formatter`
- `charliermarsh.ruff`
- `ms-toolsai.jupyter`
- `batisteo.vscode-django`
- `rangav.vscode-thunder-client`
- `ms-azuretools.vscode-docker`

## 8. Banco no Django

O `settings.py` agora suporta:

- PostgreSQL quando `DB_ENGINE=postgres`
- SQLite como fallback quando `DB_ENGINE` nao for `postgres`

Isso permite desenvolver com PostgreSQL no container e continuar executando local com SQLite, se quiser.
