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
| <a id="rn01"></a>[**RN01**](#rn01) | Apenas gerentes e empresas podem cadastrar usuários no sistema. | [RF01](../requisitos/requisitos_funcionais.md#rf01) |
| <a id="rn02"></a>[**RN02**](#rn02) | Apenas empresas podem gerenciar usuários do tipo gerente (cadastrar, atualizar, listar, ativar/desativar e controlar permissões e perfil). | [RF01](../requisitos/requisitos_funcionais.md#rf01), [RF02](../requisitos/requisitos_funcionais.md#rf02), [RF03](../requisitos/requisitos_funcionais.md#rf03), [RF04](../requisitos/requisitos_funcionais.md#rf04), [RF05](../requisitos/requisitos_funcionais.md#rf05) |
| <a id="rn03"></a>[**RN03**](#rn03) | Não deve existir usuário que não esteja obrigatoriamente vinculado a uma pessoa ou a uma empresa. | [RF01](../requisitos/requisitos_funcionais.md#rf01), [RF02](../requisitos/requisitos_funcionais.md#rf02), [RF03](../requisitos/requisitos_funcionais.md#rf03), [RF04](../requisitos/requisitos_funcionais.md#rf04), [RF05](../requisitos/requisitos_funcionais.md#rf05) |
| <a id="rn04"></a>[**RN04**](#rn04) | Não deve ser possível remover um usuário do sistema, apenas ativá-lo ou desativá-lo, preservando os dados históricos. | [RF03](../requisitos/requisitos_funcionais.md#rf03) |
| <a id="rn05"></a>[**RN05**](#rn05) | A empresa ou gerente pode cadastrar, atualizar, listar, ativar ou desativar apenas usuários vinculados à mesma empresa à qual ele pertence. | [RF01](../requisitos/requisitos_funcionais.md#rf01), [RF02](../requisitos/requisitos_funcionais.md#rf02), [RF03](../requisitos/requisitos_funcionais.md#rf03), [RF05](../requisitos/requisitos_funcionais.md#rf05) |
| <a id="rn06"></a>[**RN06**](#rn06) | Usuários desativados não podem autenticar nem acessar funcionalidades do sistema. | [RF03](../requisitos/requisitos_funcionais.md#rf03) |
| <a id="rn07"></a>[**RN07**](#rn07) | Não deve existir mais de um usuário com o mesmo e-mail ou identificador de acesso dentro da mesma empresa. | [RF01](../requisitos/requisitos_funcionais.md#rf01), [RF02](../requisitos/requisitos_funcionais.md#rf02) |
| <a id="rn08"></a>[**RN08**](#rn08) | As permissões atribuídas a um usuário devem ser compatíveis com seu papel no sistema, não sendo permitido conceder privilégios superiores ao papel definido. | [RF04](../requisitos/requisitos_funcionais.md#rf04) |
| <a id="rn09"></a>[**RN09**](#rn09) | Vendedores cadastrados não possuem acesso direto ao sistema. Suas informações ficam salvas para fins de controle financeiro e comissionamento, porém não possuem credenciais de acesso. | [RF06](../requisitos/requisitos_funcionais.md#rf06), [RF21](../requisitos/requisitos_funcionais.md#rf21), [RF22](../requisitos/requisitos_funcionais.md#rf22), [RF24](../requisitos/requisitos_funcionais.md#rf24) |
| <a id="rn10"></a>[**RN10**](#rn10) | Uma usina só pode ser cadastrada se estiver vinculada à empresa do ator administrativo responsável pelo cadastro. | [RF07](../requisitos/requisitos_funcionais.md#rf07) |
| <a id="rn11"></a>[**RN11**](#rn11) | Não deve existir mais de uma usina com o mesmo identificador dentro da mesma empresa. | [RF07](../requisitos/requisitos_funcionais.md#rf07) |
| <a id="rn12"></a>[**RN12**](#rn12) | Apenas empresa e gerentes podem cadastrar, atualizar, ativar ou desativar usinas. | [RF07](../requisitos/requisitos_funcionais.md#rf07), [RF08](../requisitos/requisitos_funcionais.md#rf08), [RF09](../requisitos/requisitos_funcionais.md#rf09) |
| <a id="rn13"></a>[**RN13**](#rn13) | Todas as usinas devem ter um endereço cadastrado no sistema, associado à própria usina. | [RF07](../requisitos/requisitos_funcionais.md#rf07) |
| <a id="rn14"></a>[**RN14**](#rn14) | Uma usina não pode ter mais de um endereço cadastrado. | [RF07](../requisitos/requisitos_funcionais.md#rf07) |
| <a id="rn15"></a>[**RN15**](#rn15) | Um endereço pode ter mais de uma usina cadastrada. | [RF07](../requisitos/requisitos_funcionais.md#rf07) |
| <a id="rn16"></a>[**RN16**](#rn16) | Um usuário somente pode cadastrar, atualizar, ativar/desativar ou gerenciar permissões de usuários com papel hierarquicamente inferior ao seu próprio dentro da mesma empresa **e se ele for do tipo, gerente ou empresa**. Um gerente não pode gerenciar outro gerente; uma empresa não pode ser gerenciada por outra empresa, e analistas não podem gerenciar usuários. | [RF01](../requisitos/requisitos_funcionais.md#rf01), [RF02](../requisitos/requisitos_funcionais.md#rf02), [RF03](../requisitos/requisitos_funcionais.md#rf03), [RF04](../requisitos/requisitos_funcionais.md#rf04) |
| <a id="rn17"></a>[**RN17**](#rn17) | Qualquer alteração de dados sensíveis exige senha do ator administrativo. | [RF02](../requisitos/requisitos_funcionais.md#rf02), [RF04](../requisitos/requisitos_funcionais.md#rf04) |
| <a id="rn18"></a>[**RN18**](#rn18) | Não deve ser possível que os **usuários não administrativos** alterem qualquer tipo de dado sensível de suas contas (CPF, nome completo e tipo de perfil). | [RF02](../requisitos/requisitos_funcionais.md#rf02), [RF04](../requisitos/requisitos_funcionais.md#rf04), [RF18](../requisitos/requisitos_funcionais.md#rf18) |
| <a id="rn19"></a>[**RN19**](#rn19) | Um Analista (Energético ou Financeiro) só pode ter acesso às usinas que estão vinculadas a ele. | [RF12](../requisitos/requisitos_funcionais.md#rf12), [RF14](../requisitos/requisitos_funcionais.md#rf14), [RF17](../requisitos/requisitos_funcionais.md#rf17), [RF20](../requisitos/requisitos_funcionais.md#rf20) |
| <a id="rn20"></a>[**RN20**](#rn20) | Analistas (Energético e Financeiro) podem listar apenas usuários vinculados às usinas às quais também estão vinculados. Não podem visualizar usuários fora desse escopo, nem usuários do tipo Empresa ou Gerente. | [RF17](../requisitos/requisitos_funcionais.md#rf17) |
| <a id="rn21"></a>[**RN21**](#rn21) | O usuário autenticado e ativo pode atualizar apenas os próprios dados não sensíveis. Não é permitido editar dados de terceiros neste fluxo. | [RF18](../requisitos/requisitos_funcionais.md#rf18) |
| <a id="rn22"></a>[**RN22**](#rn22) | A ativação ou desativação de usuário exige confirmação de senha do ator administrativo responsável pela ação. | [RF03](../requisitos/requisitos_funcionais.md#rf03), [RF19](../requisitos/requisitos_funcionais.md#rf19) |
| <a id="rn23"></a>[**RN23**](#rn23) | Empresa e gerente podem cadastrar, listar, atualizar e remover vendedores apenas da mesma empresa à qual estão vinculados. | [RF06](../requisitos/requisitos_funcionais.md#rf06), [RF21](../requisitos/requisitos_funcionais.md#rf21), [RF22](../requisitos/requisitos_funcionais.md#rf22), [RF24](../requisitos/requisitos_funcionais.md#rf24) |
| <a id="rn24"></a>[**RN24**](#rn24) | Não deve existir mais de um vendedor com o mesmo CPF dentro da mesma empresa. | [RF06](../requisitos/requisitos_funcionais.md#rf06), [RF22](../requisitos/requisitos_funcionais.md#rf22) |
| <a id="rn25"></a>[**RN25**](#rn25) | Analistas (Energético e Financeiro) podem listar apenas usinas às quais estão vinculados; não podem visualizar usinas fora desse vínculo. | [RF20](../requisitos/requisitos_funcionais.md#rf20) |
| <a id="rn26"></a>[**RN26**](#rn26) | A empresa pode atualizar apenas os próprios dados cadastrais e de contato; não pode atualizar dados de outra empresa. | [RF23](../requisitos/requisitos_funcionais.md#rf23) |
| <a id="rn27"></a>[**RN27**](#rn27) | A atualização de usina só pode ocorrer quando a usina estiver vinculada à mesma empresa do ator (empresa ou gerente). | [RF08](../requisitos/requisitos_funcionais.md#rf08) |
| <a id="rn28"></a>[**RN28**](#rn28) | Qualquer alteração em dados sensíveis da usina exige confirmação de senha do ator administrativo responsável. | [RF08](../requisitos/requisitos_funcionais.md#rf08) |
| <a id="rn29"></a>[**RN29**](#rn29) | Não é permitido remover vendedor com contrato ativo ou comissionamento pendente; nesses casos a ação deve ser bloqueada. | [RF24](../requisitos/requisitos_funcionais.md#rf24) |
| <a id="rn30"></a>[**RN30**](#rn30) | A ativação/desativação de usina só pode ocorrer para usinas vinculadas à mesma empresa do ator (empresa ou gerente). | [RF09](../requisitos/requisitos_funcionais.md#rf09) |
| <a id="rn31"></a>[**RN31**](#rn31) | Usinas desativadas não podem ser usadas em novos contratos, novos rateios ou novas vinculações operacionais até serem reativadas. | [RF09](../requisitos/requisitos_funcionais.md#rf09) |
