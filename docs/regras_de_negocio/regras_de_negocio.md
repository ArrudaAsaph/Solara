# Regras de Negócio (RN)

> **Arquivo:** `regras_de_negocio.md`
> **Descrição:** Define as regras que governam o comportamento do sistema, validações e restrições de negócio.

---

## Hierarquia de Usuários do Sistema

A hierarquia de papéis no sistema, do nível mais alto ao mais baixo, é:

```
Empresa
  └── Gerente
        ├── Analista Energético
        ├── Analista Financeiro
        ├── Investidor
        └── Consumidor
```

> **Obs.:** O **Vendedor** não é um usuário do sistema — é uma entidade cadastrada exclusivamente para fins de controle financeiro e comissionamento, sem credenciais de acesso (ver RN09).

---

## Tabela de Regras de Negócio

| **Código** | **Descrição** | **Requisito(s) Atendido(s)** |
| :--------: | :------------ | :--------------------------: |
| **RN01** | Apenas gerentes e empresas podem cadastrar usuários no sistema. | RF01 |
| **RN02** | Apenas empresas podem gerenciar usuários do tipo gerente (cadastrar, atualizar, listar, ativar/desativar e controlar permissões e perfil). | RF01, RF02, RF03, RF04, RF05 |
| **RN03** | Não deve existir usuário que não esteja obrigatoriamente vinculado a uma pessoa ou a uma empresa. | RF01, RF02, RF03, RF04, RF05 |
| **RN04** | Não deve ser possível remover um usuário do sistema, apenas ativá-lo ou desativá-lo, preservando os dados históricos. | RF03 |
| **RN05** | A empresa ou gerente pode cadastrar, atualizar, listar, ativar ou desativar apenas usuários vinculados à mesma empresa à qual ele pertence. | RF01, RF02, RF03, RF05 |
| **RN06** | Usuários desativados não podem autenticar nem acessar funcionalidades do sistema. | RF03 |
| **RN07** | Não deve existir mais de um usuário com o mesmo e-mail ou identificador de acesso dentro da mesma empresa. | RF01, RF02 |
| **RN08** | As permissões atribuídas a um usuário devem ser compatíveis com seu papel no sistema, não sendo permitido conceder privilégios superiores ao papel definido. | RF04 |
| **RN09** | Vendedores cadastrados não possuem acesso direto ao sistema. Suas informações ficam salvas para fins de controle financeiro e comissionamento, porém não possuem credenciais de acesso. | RF06, RF21, RF22, RF24 |
| **RN10** | Uma usina só pode ser cadastrada se estiver vinculada à empresa do ator administrativo responsável pelo cadastro. | RF07 |
| **RN11** | Não deve existir mais de uma usina com o mesmo identificador dentro da mesma empresa. | RF07 |
| **RN12** | Apenas empresa e gerentes podem cadastrar, atualizar, ativar ou desativar usinas. | RF07, RF08, RF09 |
| **RN13** | Todas as usinas devem ter um endereço cadastrado no sistema, associado à própria usina. | RF07 |
| **RN14** | Uma usina não pode ter mais de um endereço cadastrado. | RF07 |
| **RN15** | Um endereço pode ter mais de uma usina cadastrada. | RF07 |
| **RN16** | Um usuário somente pode cadastrar, atualizar, ativar/desativar ou gerenciar permissões de usuários com papel hierarquicamente inferior ao seu próprio dentro da mesma empresa **e se ele for do tipo, gerente ou empresa**. Um gerente não pode gerenciar outro gerente; uma empresa não pode ser gerenciada por outra empresa, e analistas não podem gerenciar usuários. | RF01, RF02, RF03, RF04 |
| **RN17** | Qualquer alteração de dados sensíveis exige senha do ator administrativo. | RF02, RF04 |
| **RN18** | Não deve ser possível que os **usuários não administrativos** alterem qualquer tipo de dado sensível de suas contas (CPF, nome completo e tipo de perfil). | RF02, RF04, RF18 |
| **RN19** | Um Analista (Energético ou Financeiro) só pode ter acesso às usinas que estão vinculadas a ele. | RF12, RF14, RF17, RF20 |
| **RN20** | Analistas (Energético e Financeiro) podem listar apenas usuários vinculados às usinas às quais também estão vinculados. Não podem visualizar usuários fora desse escopo, nem usuários do tipo Empresa ou Gerente. | RF17 |
| **RN21** | O usuário autenticado e ativo pode atualizar apenas os próprios dados não sensíveis. Não é permitido editar dados de terceiros neste fluxo. | RF18 |
| **RN22** | A ativação ou desativação de usuário exige confirmação de senha do ator administrativo responsável pela ação. | RF03, RF19 |
| **RN23** | Empresa e gerente podem cadastrar, listar, atualizar e remover vendedores apenas da mesma empresa à qual estão vinculados. | RF06, RF21, RF22, RF24 |
| **RN24** | Não deve existir mais de um vendedor com o mesmo CPF dentro da mesma empresa. | RF06, RF22 |
| **RN25** | Analistas (Energético e Financeiro) podem listar apenas usinas às quais estão vinculados; não podem visualizar usinas fora desse vínculo. | RF20 |
| **RN26** | A empresa pode atualizar apenas os próprios dados cadastrais e de contato; não pode atualizar dados de outra empresa. | RF23 |
| **RN27** | A atualização de usina só pode ocorrer quando a usina estiver vinculada à mesma empresa do ator (empresa ou gerente). | RF08 |
| **RN28** | Qualquer alteração em dados sensíveis da usina exige confirmação de senha do ator administrativo responsável. | RF08 |
| **RN29** | Não é permitido remover vendedor com contrato ativo ou comissionamento pendente; nesses casos a ação deve ser bloqueada. | RF24 |
| **RN30** | A ativação/desativação de usina só pode ocorrer para usinas vinculadas à mesma empresa do ator (empresa ou gerente). | RF09 |
| **RN31** | Usinas desativadas não podem ser usadas em novos contratos, novos rateios ou novas vinculações operacionais até serem reativadas. | RF09 |
