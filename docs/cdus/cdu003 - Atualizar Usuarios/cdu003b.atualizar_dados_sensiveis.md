# CDU003-B – Atualizar Dados Sensíveis do Usuário

> **Arquivo:** `cdu003b_atualizar_dados_sensiveis.md`
> **Descrição:** Caso de uso referente à atualização de dados sensíveis de um usuário existente no sistema. Por envolverem informações que podem estar registradas em contratos ou impactar a identidade do usuário, essas alterações são restritas à **Empresa** e ao **Gerente**, mediante confirmação de senha.

---

## Identificação

| **Campo** | **Valor** |
| :-------- | :-------- |
| **Código** | CDU003-B |
| **Ator Principal** | Empresa / Gerente |
| **Atores Secundários** | Sistema |
| **Requisito Atendido** | RF02 |

---

## Resumo

Permite à Empresa ou ao Gerente alterar os dados sensíveis de um usuário hierarquicamente inferior vinculado à mesma empresa. Por serem dados que podem impactar contratos vigentes, toda alteração exige confirmação da senha do ator responsável pela mudança, e o histórico completo é registrado com os valores anteriores e novos.

### O que são dados sensíveis

| **Campo** | **Motivo da sensibilidade** |
| :-------- | :-------------------------- |
| **Nome completo** | Pode estar registrado em contratos ativos |
| **CPF** | Identificador legal do usuário, usado em documentos fiscais |
| **Tipo de perfil** | Define o nível de acesso e pode impactar responsabilidades contratuais |

> **Status (ativo/inativo)** é gerenciado exclusivamente pelo **CDU004** e não é tratado neste caso de uso.

---

## Pré-condições

- O ator deve estar autenticado no sistema.
- O ator deve estar ativo e vinculado a uma empresa ativa.
- O usuário alvo deve estar vinculado à mesma empresa do ator.
- O usuário alvo deve possuir papel hierarquicamente inferior ao do ator (RN16).
- **Se o dado a ser alterado for o tipo de perfil:** o novo perfil deve ser hierarquicamente inferior ao papel do ator (RN16).

---

## Pós-condições

- O dado sensível é atualizado com sucesso.
- O histórico registra: campo alterado, valor anterior, novo valor, data/hora e identificação do ator responsável.
- As regras de integridade são mantidas.

---

## Mapeamento: CDU → Requisitos Funcionais

| **Requisito** | **Descrição** |
| :------------ | :------------ |
| **RF02** | A empresa ou o gerente pode atualizar os dados cadastrais de usuários já existentes no sistema, mantendo o histórico das alterações. |

---

## Mapeamento: CDU → Regras de Negócio

| **Código** | **Descrição** |
| :--------: | :------------ |
| **RN02** | Apenas empresas podem atualizar dados sensíveis de usuários do tipo gerente. O gerente não pode editar outro gerente. |
| **RN05** | A empresa ou o gerente pode atualizar apenas usuários vinculados à mesma empresa à qual pertence. |
| **RN16** | Um usuário somente pode atualizar dados de usuários com papel hierarquicamente inferior ao seu. Ao alterar o tipo de perfil, o novo perfil atribuído também deve ser inferior ao papel do ator. |
| **RN17** | Somente empresas e gerentes podem alterar dados sensíveis (nome completo, CPF e tipo de perfil), respeitando a hierarquia (RN16), mediante confirmação da senha do ator que está realizando a alteração. |
| **RN18** | Usuários não administrativos não podem alterar dados sensíveis de suas próprias contas. |

---

## Fluxo Principal

| **Passo** | **Ações do Ator** | **Ações do Sistema** |
| :-------: | :---------------- | :------------------- |
| 1 | Acessa a opção "Listar Usuários". | |
| 2 | | Exibe a listagem de usuários dentro do escopo do ator (conforme RN16). |
| 3 | Seleciona um usuário da listagem. | |
| 4 | | Exibe os dados cadastrais completos do usuário selecionado. |
| 5 | Seleciona a opção "Editar". | |
| 6 | | Exibe o formulário de edição. Os campos sensíveis (nome completo, CPF e tipo de perfil) estão habilitados para edição, com indicação visual destacando que a alteração exigirá confirmação de senha. |
| 7 | Altera um ou mais campos sensíveis e seleciona "Salvar". | |
| 8 | | Detecta alteração em campo sensível. Exibe modal de confirmação solicitando a **senha de acesso do ator**, conforme **RN17**. O modal exibe um resumo das alterações que serão aplicadas (campo, valor anterior → novo valor). |
| 9 | Lê o resumo das alterações, informa a senha de acesso e confirma. | |
| 10 | | Valida a senha informada. |
| 11 | | Valida as Regras de Negócio **RN02** (se aplicável), **RN05**, **RN16** e **RN17**. |
| 12 | | Aplica as alterações. |
| 13 | | Registra no histórico: campo alterado, valor anterior, novo valor, data/hora e identificação do ator responsável. |
| 14 | Visualiza os dados atualizados do usuário com confirmação de sucesso. | |

---

## Fluxos de Exceção

### Fluxo de Exceção I – Tentativa de editar usuário fora do escopo

| **Passo** | **Ações do Ator** | **Ações do Sistema** |
| :-------: | :---------------- | :------------------- |
| 0.1 | Tenta acessar usuário não vinculado à sua empresa ou de nível hierárquico igual/superior. | |
| 0.2 | | Valida as Regras de Negócio **RN05** e **RN16**. |
| 0.3 | | Bloqueia o acesso e exibe mensagem de acesso não autorizado. |

### Fluxo de Exceção II – Senha incorreta na confirmação

| **Passo** | **Ações do Ator** | **Ações do Sistema** |
| :-------: | :---------------- | :------------------- |
| 0.4 | Informa senha incorreta no modal de confirmação. | |
| 0.5 | | Valida a senha. Detecta que está incorreta. |
| 0.6 | | Mantém o modal aberto, exibe mensagem de senha inválida. Nenhuma alteração é aplicada. |
| 0.7 | Informa a senha correta e confirma novamente. | |

### Fluxo de Exceção III – Tentativa de atribuir tipo de perfil inválido

| **Passo** | **Ações do Ator** | **Ações do Sistema** |
| :-------: | :---------------- | :------------------- |
| 0.8 | Tenta alterar o tipo de perfil do usuário para um papel de nível igual ou superior ao seu (ex.: gerente tentando promover outro usuário a gerente). | |
| 0.9 | | Valida a Regra de Negócio **RN16**. |
| 0.10 | | Bloqueia a alteração e exibe mensagem informando que não é permitido atribuir perfil de nível igual ou superior ao do ator. O modal de senha não é exibido. |

### Fluxo de Exceção IV – Cancelamento no modal de confirmação

| **Passo** | **Ações do Ator** | **Ações do Sistema** |
| :-------: | :---------------- | :------------------- |
| 0.11 | Cancela a ação no modal de confirmação de senha. | |
| 0.12 | | Descarta todas as alterações pendentes. Retorna ao formulário de edição com os dados originais. Nenhuma modificação é persistida. |