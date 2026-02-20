# CDU003-A – Atualizar Dados Próprios do Usuário

> **Arquivo:** `cdu003a_usuario_atualizar_dados_proprios.md`
> **Descrição:** Caso de uso referente à atualização dos próprios dados não sensíveis pelo usuário autenticado. Dados sensíveis são bloqueados para edição neste contexto — sua alteração é exclusiva da Empresa ou Gerente (CDU003-B).

---

## Identificação

| **Campo** | **Valor** |
| :-------- | :-------- |
| **Código** | CDU003-A |
| **Ator Principal** | Usuário |
| **Atores Secundários** | Sistema |
| **Requisito Atendido** | RF18 |

---

## Resumo

Permite que qualquer usuário autenticado e ativo atualize seus próprios dados não sensíveis. Os campos sensíveis (nome completo, CPF e tipo de perfil) e o status são exibidos somente para leitura e não podem ser alterados pelo próprio usuário.

### Campos disponíveis neste fluxo

| **Campo** | **Editável pelo usuário** |
| :-------- | :------------------------: |
| E-mail | ✅ |
| Username | ✅ |
| Senha | ✅ |
| E-mail de contato | ✅ |
| Telefone | ✅ |
| Nome completo | ❌ somente leitura |
| CPF | ❌ somente leitura |
| Tipo de perfil | ❌ somente leitura |
| Status (ativo/inativo) | ❌ somente leitura — gerenciado pelo CDU004 |

---

## Pré-condições

- O usuário deve estar autenticado no sistema.
- O usuário deve estar ativo.

---

## Pós-condições

- Os dados não sensíveis do usuário são atualizados com sucesso.
- O histórico das alterações é registrado.
- As regras de unicidade são mantidas.

---

## Mapeamento: CDU → Requisitos Funcionais

| **Requisito** | **Descrição** |
| :------------ | :------------ |
| **RF18** | O usuário pode atualizar apenas os próprios dados não sensíveis, mantendo o histórico das alterações e respeitando as regras de integridade. |

---

## Mapeamento: CDU → Regras de Negócio

| **Código** | **Descrição** |
| :--------: | :------------ |
| **RN07** | Não deve existir mais de um usuário com o mesmo e-mail ou identificador de acesso dentro da mesma empresa. |
| **RN18** | Usuários não administrativos não podem alterar dados sensíveis de suas próprias contas (nome completo, CPF e tipo de perfil). |
| **RN21** | O usuário autenticado e ativo pode atualizar apenas os próprios dados não sensíveis. Não é permitido editar dados de terceiros neste fluxo. |

---

## Fluxo Principal

| **Passo** | **Ações do Ator** | **Ações do Sistema** |
| :-------: | :---------------- | :------------------- |
| 1 | Acessa a opção "Meu Perfil" ou "Editar meus dados". | |
| 2 | | Exibe o formulário de edição. Os campos editáveis são: **e-mail, username, senha, e-mail de contato e telefone**. Os campos sensíveis (nome completo, CPF, tipo de perfil) e o status são renderizados como **somente leitura**, sem possibilidade de interação. |
| 3 | Atualiza os campos desejados e confirma. | |
| 4 | | Valida as Regras de Negócio **RN07**, **RN18** e **RN21**. |
| 5 | | Salva as alterações realizadas. |
| 6 | | Registra o histórico das alterações. |
| 7 | Visualiza os dados atualizados com confirmação de sucesso. | |

---

## Fluxos de Exceção

### Fluxo de Exceção I – Falha na validação dos dados

| **Passo** | **Ações do Ator** | **Ações do Sistema** |
| :-------: | :---------------- | :------------------- |
| 0.1 | Informa dados inválidos ou duplicados (ex.: e-mail já em uso). | |
| 0.2 | | Valida a Regra de Negócio **RN07**. |
| 0.3 | | Exibe mensagem de erro indicando a inconsistência. |
| 0.4 | Corrige os dados e confirma novamente. | |

### Fluxo de Exceção II – Tentativa de alterar dado sensível

| **Passo** | **Ações do Ator** | **Ações do Sistema** |
| :-------: | :---------------- | :------------------- |
| 0.5 | Tenta modificar campo sensível (nome completo, CPF ou tipo de perfil). | |
| 0.6 | | Valida a Regra de Negócio **RN18**. Os campos sensíveis são renderizados como somente leitura — a ação é bloqueada na interface antes mesmo do envio. |
