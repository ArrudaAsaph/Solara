# LumenEnergy

## Ambiente de desenvolvimento (Dev Container + PostgreSQL)

Este projeto está preparado para rodar em um ambiente padronizado usando **VS Code Dev Container**.

Com isso, qualquer pessoa do time sobe o projeto com as mesmas versões e dependências, sem configurar Python/PostgreSQL manualmente na máquina local.

### Pré-requisitos

1. Docker Desktop (ou Docker Engine + Docker Compose)
2. VS Code
3. Extensão `Dev Containers` no VS Code

### Como usar (passo a passo)

1. Abra a pasta do projeto no VS Code.
2. Rode o comando: `Dev Containers: Reopen in Container`.
3. Aguarde o build e o `postCreateCommand` finalizar.

Quando o container termina de subir, o projeto já fica pronto para desenvolvimento.

Se quiser subir/descer manualmente fora do VS Code:

```bash
./scripts/devcontainer-up.sh
./scripts/devcontainer-down.sh
```

### O que o Dev Container cria e faz automaticamente

Ao subir o ambiente, o Docker Compose inicia:

- `app`: container Python de desenvolvimento
- `db`: PostgreSQL 16

Depois disso, o script de pós-criação executa automaticamente:

1. instalação de dependências (`pip install -r backend/requirements.txt`)
2. migrations do Django (`python manage.py migrate`)
3. bootstrap de dados de desenvolvimento (`python manage.py bootstrap_dev_data ...`)

Esse bootstrap cria/atualiza:

- 1 superadmin
- várias empresas
- vários usuários por empresa com perfis rotacionados

### Credenciais padrão de desenvolvimento

- Superadmin:
  - usuário: `admin`
  - senha: `admin123`
- Usuários seed (empresa/pessoa):
  - senha: `Senha@123456`

### Como rodar o backend

Dentro do terminal do container:

```bash
cd backend/solara
python manage.py runserver 0.0.0.0:8000
```

A API ficará acessível em `http://localhost:8000`.

### Comandos principais

Rodar bootstrap completo novamente:

```bash
cd backend/solara
./scripts/bootstrap_dev.sh
```

Rodar seed manual com parâmetros:

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

Rodar testes:

```bash
cd backend/solara
python manage.py test contas.tests -v 2
```

### Extensões instaladas automaticamente no container

- Python, Pylance, Debugpy
- Black formatter
- Ruff
- Django extension
- Thunder Client
- Jupyter
- Docker

### Configuração do banco

O Django foi configurado para:

- usar PostgreSQL quando `DB_ENGINE=postgres`
- usar SQLite como fallback fora do container

Variáveis de exemplo estão em:

- `backend/solara/.env.example`

### Documentação complementar

- Guia detalhado do ambiente: `docs/ambiente/devcontainer.md`
- Guia de testes do app contas: `docs/testes/testes_contas.md`
