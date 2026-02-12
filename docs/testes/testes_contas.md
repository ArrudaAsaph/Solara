# Guia de Testes Unitários - App `contas`

Este documento explica como executar e interpretar os testes unitários do app `contas`.

## 1. Onde estão os testes

Os testes estão no diretório:

- `backend/solara/contas/tests`

Arquivos principais:

- `backend/solara/contas/tests/factories.py`
- `backend/solara/contas/tests/test_cadastro_service.py`
- `backend/solara/contas/tests/test_pessoa_service.py`
- `backend/solara/contas/tests/test_usuario_service.py`

## 2. Pré-requisitos

No ambiente local, instale as dependências do backend:

```bash
cd backend
python -m pip install -r requirements.txt
```

Observação: sem `djangorestframework` instalado, o Django não inicia e os testes não executam.

## 3. Como executar

Rodar toda a suíte do app `contas`:

```bash
cd backend/solara
python manage.py test contas.tests -v 2
```

Rodar somente um arquivo:

```bash
python manage.py test contas.tests.test_cadastro_service -v 2
```

Rodar somente um teste específico:

```bash
python manage.py test contas.tests.test_cadastro_service.CadastroServiceTestCase.test_criar_com_empresa_normaliza_e_persiste_dados -v 2
```

## 4. Como os testes foram organizados

Padrões adotados:

- isolamento por teste com `django.test.TestCase`
- cenários de negócio por serviço (cadastro, pessoa, usuário)
- criação de dados via factory para reduzir repetição
- foco em regra de autorização, validação e fluxo feliz

### 4.1 `factories.py`

`ContaFactory` centraliza criação de:

- usuário (`criar_usuario`)
- empresa com usuário (`criar_empresa_com_usuario`)
- pessoa com usuário (`criar_pessoa_com_usuario`)

Objetivo: facilitar leitura dos testes e permitir montar cenários de permissão rapidamente.

## 5. O que cada teste valida e o que se espera

## 5.1 `test_cadastro_service.py`

Classe: `CadastroServiceTestCase`

1. `test_criar_com_empresa_normaliza_e_persiste_dados`
- Esperado:
  - retorna instância de `Pessoa`
  - CPF e telefone ficam normalizados (somente dígitos)
  - primeiro e último nome são derivados de `nome_completo`
  - senha do novo usuário é armazenada com hash (`check_password == True`)

2. `test_criar_retorna_erro_quando_gerente_tenta_cadastrar_gerente`
- Esperado:
  - retorna `Erro`
  - `status_code == 403`
  - garante a regra: gerente não cadastra gerente

3. `test_criar_retorna_erro_de_validacao_para_username_duplicado`
- Esperado:
  - retorna `Erro`
  - `status_code == 409`
  - campo `username` aparece na lista de erros de validação

## 5.2 `test_pessoa_service.py`

Classe: `PessoaServiceTestCase`

1. `test_listar_para_gerente_retorna_somente_hierarquia_da_empresa`
- Esperado:
  - gerente enxerga apenas perfis abaixo na hierarquia
  - não retorna o próprio gerente
  - não retorna pessoas de outra empresa

2. `test_buscar_por_id_retorna_erro_para_perfil_nao_visualizavel`
- Esperado:
  - retorna `Erro`
  - `status_code == 403`
  - gerente não pode visualizar outro gerente

3. `test_atualizar_altera_tipo_perfil_quando_senha_valida`
- Esperado:
  - atualização realizada com sucesso quando senha está correta
  - `tipo_perfil` da pessoa alvo é alterado

## 5.3 `test_usuario_service.py`

Classe: `UsuarioServiceTestCase`

1. `test_listar_para_empresa_retorna_usuarios_de_pessoas_da_empresa`
- Esperado:
  - empresa enxerga usuários da própria empresa
  - não enxerga usuários vinculados a outra empresa

2. `test_listar_para_gerente_exclui_perfil_gerente`
- Esperado:
  - gerente vê analista/investidor
  - gerente não vê outros gerentes

## 6. Boas práticas para novos testes

Quando criar novos testes:

1. manter nomes descritivos no padrão `test_<acao>_<resultado>`
2. montar cenário mínimo necessário usando `ContaFactory`
3. validar comportamento de negócio (não implementação interna)
4. sempre validar status e tipo de retorno (`Erro` vs entidade/queryset)
5. cobrir casos de autorização negada e sucesso

## 7. Critério de sucesso da suíte

A suíte é considerada saudável quando:

- todos os testes do módulo passam (`OK`)
- nenhum teste depende de ordem de execução
- falhas indicam quebra real de regra de negócio (permissão, validação, visibilidade)
