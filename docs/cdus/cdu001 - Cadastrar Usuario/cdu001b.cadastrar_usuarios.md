# CDU001-B – Cadastrar Usuários (Ator: Gerente)

> **Arquivo:** `cdu001b_gerente_cadastrar_usuarios.md`
> **Descrição:** Caso de uso referente ao cadastro de usuários realizado pelo **Gerente**. O gerente pode cadastrar apenas usuários com papel hierarquicamente inferior ao seu, dentro da mesma empresa a que está vinculado.

---

## Identificação

| **Campo** | **Valor** |
| :-------- | :-------- |
| **Código** | CDU001-B |
| **Ator Principal** | Gerente |
| **Atores Secundários** | Sistema |
| **Requisito Atendido** | [RF01](../../requisitos/requisitos_funcionais.md#rf01) |

---

## Resumo

Permite ao gerente cadastrar novos usuários operacionais vinculados à sua empresa. O gerente **não pode** cadastrar outros gerentes — essa prerrogativa é exclusiva da empresa. Os papéis que o gerente pode cadastrar são: Analista Energético, Analista Financeiro, Investidor e Consumidor.

---

## Pré-condições

- O gerente deve estar autenticado no sistema.
- O gerente deve estar vinculado a uma empresa ativa.
- O gerente deve estar ativo.

---

## Pós-condições

- Usuário cadastrado e vinculado à empresa do gerente.
- Usuário criado com status **ativo** por padrão.
- Histórico de criação registrado no sistema.

---

## Mapeamento: CDU → Requisitos Funcionais

| **Requisito** | **Descrição** |
| :------------ | :------------ |
| [**RF01**](../../requisitos/requisitos_funcionais.md#rf01) | O gerente pode cadastrar usuários no sistema, exceto usuários do tipo Gerente. |

---

## Mapeamento: CDU → Regras de Negócio

| **Código** | **Descrição** |
| :--------: | :------------ |
| [**RN01**](../../regras_de_negocio/regras_de_negocio.md#rn01) | Apenas gerentes e empresas podem cadastrar usuários no sistema. |
| [**RN02**](../../regras_de_negocio/regras_de_negocio.md#rn02) | Apenas empresas podem gerenciar usuários do tipo gerente. O gerente **não pode** cadastrar outro gerente. |
| [**RN03**](../../regras_de_negocio/regras_de_negocio.md#rn03) | Não deve existir usuário que não esteja obrigatoriamente vinculado a uma pessoa ou a uma empresa. |
| [**RN05**](../../regras_de_negocio/regras_de_negocio.md#rn05) | O gerente pode cadastrar apenas usuários vinculados à mesma empresa à qual ele pertence. |
| [**RN07**](../../regras_de_negocio/regras_de_negocio.md#rn07) | Não deve existir mais de um usuário com o mesmo e-mail ou identificador de acesso dentro da mesma empresa. |
| [**RN16**](../../regras_de_negocio/regras_de_negocio.md#rn16) | Um usuário somente pode cadastrar usuários com papel hierarquicamente inferior ao seu. O gerente não pode cadastrar outro gerente. |

---

## Fluxo Principal

| **Passo** | **Ações do Ator** | **Ações do Sistema** |
| :-------: | :---------------- | :------------------- |
| 1 | Acessa a opção "Gerenciar Usuários". | |
| 2 | | Exibe a listagem de usuários vinculados à empresa, com filtros por nome, tipo de usuário e status. |
| 3 | Seleciona a opção "Cadastrar Usuário". | |
| 4 | | Exibe formulário de cadastro com campos: nome, e-mail e tipo de usuário. Os tipos disponíveis são apenas os de nível inferior ao gerente: Analista Energético, Analista Financeiro, Investidor e Consumidor. O status é definido como **ativo** por padrão. |
| 5 | Preenche os dados e confirma o cadastro. | |
| 6 | | Valida as Regras de Negócio [**RN01**](../../regras_de_negocio/regras_de_negocio.md#rn01), [**RN02**](../../regras_de_negocio/regras_de_negocio.md#rn02), [**RN03**](../../regras_de_negocio/regras_de_negocio.md#rn03), [**RN05**](../../regras_de_negocio/regras_de_negocio.md#rn05), [**RN07**](../../regras_de_negocio/regras_de_negocio.md#rn07) e [**RN16**](../../regras_de_negocio/regras_de_negocio.md#rn16), e cria o novo usuário no sistema. |
| 7 | Visualiza o usuário cadastrado na listagem. | |

---

## Fluxos de Exceção

### Fluxo de Exceção I – Falha na validação do cadastro

| **Passo** | **Ações do Ator** | **Ações do Sistema** |
| :-------: | :---------------- | :------------------- |
| 0.1 | Preenche o formulário com dados inválidos ou incompletos. | |
| 0.2 | | Valida as Regras de Negócio [**RN01**](../../regras_de_negocio/regras_de_negocio.md#rn01), [**RN02**](../../regras_de_negocio/regras_de_negocio.md#rn02), [**RN03**](../../regras_de_negocio/regras_de_negocio.md#rn03), [**RN05**](../../regras_de_negocio/regras_de_negocio.md#rn05), [**RN07**](../../regras_de_negocio/regras_de_negocio.md#rn07) e [**RN16**](../../regras_de_negocio/regras_de_negocio.md#rn16) aplicáveis. |
| 0.3 | | Exibe mensagens de erro indicando campos inválidos ou duplicidade de dados. |
| 0.4 | Corrige os dados informados e confirma novamente. | |

### Fluxo de Exceção II – Tentativa de cadastrar usuário do tipo Gerente

| **Passo** | **Ações do Ator** | **Ações do Sistema** |
| :-------: | :---------------- | :------------------- |
| 0.5 | Tenta selecionar o tipo "Gerente" no formulário de cadastro. | |
| 0.6 | | Valida as Regras de Negócio [**RN02**](../../regras_de_negocio/regras_de_negocio.md#rn02) e [**RN16**](../../regras_de_negocio/regras_de_negocio.md#rn16). |
| 0.7 | | Bloqueia a ação e exibe mensagem informando que gerentes só podem ser cadastrados pela empresa. |