
## Regras de Negócio (RN)

| **Código** | **Descrição**                                                                                                                                                | **Requisito(s) Atendido(s)** |
| :--------: | :----------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------: |
|  **RN01**  | Apenas gerentes e empresas podem cadastrar usuários no sistema.                                                                                              |             RF01             |
|  **RN02**  | Apenas empresas podem gerenciar usuários do tipo gerente (cadastrar, atualizar, listar, ativar/desativar e controlar permissões e perfil).                   | RF01, RF02, RF03, RF04, RF05 |
|  **RN03**  | Não deve existir usuário que não esteja obrigatoriamente vinculado a uma pessoa ou a uma empresa.                                                            | RF01, RF02, RF03, RF04, RF05 |
|  **RN04**  | Não deve ser possível remover um usuário do sistema, apenas ativá-lo ou desativá-lo, preservando os dados históricos.                                        |             RF03             |
|  **RN05**  | O gerente pode cadastrar, atualizar, listar, ativar ou desativar apenas usuários vinculados à mesma empresa à qual ele pertence.                             |    RF01, RF02, RF03, RF05    |
|  **RN06**  | Usuários desativados não podem autenticar nem acessar funcionalidades do sistema.                                                                            |             RF03             |
|  **RN07**  | Não deve existir mais de um usuário com o mesmo e-mail ou identificador de acesso dentro da mesma empresa.                                                   |          RF01, RF02          |
|  **RN08**  | As permissões atribuídas a um usuário devem ser compatíveis com seu papel no sistema, não sendo permitido conceder privilégios superiores ao papel definido. |             RF04             |
|  **RN09**  | Vendedores cadastradas não possuem acesso direto ao sistema, suas informações ficam salvas, porém não possuem credencias de acesso.  | RF06 |
|  **RN10**  | Uma usina só pode ser cadastrada se estiver vinculada a empresa do gerente.  | RF07 |
|  **RN11**  | Não deve existir mais de uma usina com o mesmo identificador, dentro da mesma empresa.  | RF07 |
|  **RN12**  | Apenas gerentes podem cadastrar, atualizar, ativar ou desativar usinas.  | RF07, RF08, RF09 |
|  **RN13**  | Todas as usina devem ter um endereço cadastrado no sistema, e associada à própria usina.  | RF07 |
|  **RN14**  | Uma usina não pode ter mais de um endereço cadastrado.  | RF07 |
|  **RN15**  | Um endereço pode ter mais de uma usina cadastrada.  | RF07 |



