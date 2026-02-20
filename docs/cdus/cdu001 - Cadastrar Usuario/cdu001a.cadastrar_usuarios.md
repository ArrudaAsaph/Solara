# CDU001-A – Cadastrar Usuários (Ator: Empresa)

> **Arquivo:** `cdu001a_empresa_cadastrar_usuarios.md`
> **Descrição:** Caso de uso referente ao cadastro de usuários realizado pela **Empresa**. A empresa é o único ator que pode cadastrar usuários do tipo Gerente, além dos demais níveis inferiores da hierarquia.

---

## Identificação

| **Campo** | **Valor** |
| :-------- | :-------- |
| **Código** | CDU001-A |
| **Ator Principal** | Empresa |
| **Atores Secundários** | Sistema |
| **Requisito Atendido** | [RF01](../../requisitos/requisitos_funcionais.md#rf01) |

---

## Resumo

Permite à empresa cadastrar usuários operacionais da plataforma. Por ser o ator de maior privilégio, a empresa é a única que pode cadastrar usuários do tipo **Gerente**, além de todos os demais papéis da hierarquia (Analista Energético, Analista Financeiro, Investidor e Consumidor).

---

## Pré-condições

- A empresa deve estar autenticada no sistema.
- A empresa deve estar ativa.

---

## Pós-condições

- Usuário cadastrado e vinculado à empresa.
- Usuário criado com status **ativo** por padrão.
- Histórico de criação registrado no sistema.

---

## Mapeamento: CDU → Requisitos Funcionais

| **Requisito** | **Descrição** |
| :------------ | :------------ |
| [**RF01**](../../requisitos/requisitos_funcionais.md#rf01) | A empresa pode cadastrar usuários no sistema, incluindo usuários do tipo Gerente. |

---

## Mapeamento: CDU → Regras de Negócio

| **Código** | **Descrição** |
| :--------: | :------------ |
| [**RN01**](../../regras_de_negocio/regras_de_negocio.md#rn01) | Apenas gerentes e empresas podem cadastrar usuários no sistema. |
| [**RN02**](../../regras_de_negocio/regras_de_negocio.md#rn02) | Apenas empresas podem gerenciar usuários do tipo gerente (cadastrar, atualizar, listar, ativar/desativar e controlar permissões e perfil). |
| [**RN03**](../../regras_de_negocio/regras_de_negocio.md#rn03) | Não deve existir usuário que não esteja obrigatoriamente vinculado a uma pessoa ou a uma empresa. |
| [**RN07**](../../regras_de_negocio/regras_de_negocio.md#rn07) | Não deve existir mais de um usuário com o mesmo e-mail ou identificador de acesso dentro da mesma empresa. |
| [**RN16**](../../regras_de_negocio/regras_de_negocio.md#rn16) | Um usuário somente pode cadastrar, atualizar, ativar/desativar ou gerenciar permissões de usuários com papel hierarquicamente inferior ao seu próprio dentro da mesma empresa **e se ele for do tipo, gerente ou empresa**. |

---

## Fluxo Principal

| **Passo** | **Ações do Ator** | **Ações do Sistema** |
| :-------: | :---------------- | :------------------- |
| 1 | Acessa a opção "Gerenciar Usuários". | |
| 2 | | Exibe a listagem de usuários vinculados à empresa, com filtros por nome, tipo de usuário e status. |
| 3 | Seleciona a opção "Cadastrar Usuário". | |
| 4 | | Exibe formulário de cadastro com campos: nome, e-mail e tipo de usuário (todos os níveis disponíveis, incluindo Gerente). O status é definido como **ativo** por padrão. |
| 5 | Preenche os dados e confirma o cadastro. | |
| 6 | | Valida as Regras de Negócio [**RN01**](../../regras_de_negocio/regras_de_negocio.md#rn01), [**RN02**](../../regras_de_negocio/regras_de_negocio.md#rn02), [**RN03**](../../regras_de_negocio/regras_de_negocio.md#rn03), [**RN07**](../../regras_de_negocio/regras_de_negocio.md#rn07) e [**RN16**](../../regras_de_negocio/regras_de_negocio.md#rn16), e cria o novo usuário no sistema. |
| 7 | Visualiza o usuário cadastrado na listagem. | |

---

## Fluxos de Exceção

### Fluxo de Exceção I – Falha na validação do cadastro

| **Passo** | **Ações do Ator** | **Ações do Sistema** |
| :-------: | :---------------- | :------------------- |
| 0.1 | Preenche o formulário com dados inválidos ou incompletos. | |
| 0.2 | | Valida as Regras de Negócio [**RN01**](../../regras_de_negocio/regras_de_negocio.md#rn01), [**RN02**](../../regras_de_negocio/regras_de_negocio.md#rn02), [**RN03**](../../regras_de_negocio/regras_de_negocio.md#rn03), [**RN07**](../../regras_de_negocio/regras_de_negocio.md#rn07) e [**RN16**](../../regras_de_negocio/regras_de_negocio.md#rn16) aplicáveis. |
| 0.3 | | Exibe mensagens de erro indicando campos inválidos ou duplicidade de dados. |
| 0.4 | Corrige os dados informados e confirma novamente. | |