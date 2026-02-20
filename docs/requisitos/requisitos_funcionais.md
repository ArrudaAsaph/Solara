# Requisitos Funcionais (RF)

> **Arquivo:** `requisitos_funcionais.md`
> **Descrição:** Define o que o sistema deve fazer sob a perspectiva dos atores, descrevendo as funcionalidades esperadas.

---

## Hierarquia de Atores

| **Nível** | **Ator** | **Descrição** |
| :-------: | :------- | :------------ |
| 1 | **Empresa** | Ator de maior privilégio. Gerencia gerentes e toda a estrutura da empresa no sistema. |
| 2 | **Gerente** | Gerencia usuários de nível inferior vinculados à sua empresa. |
| 3 | **Analista Energético** | Acesso a dados de geração e indicadores de usinas vinculadas. |
| 3 | **Analista Financeiro** | Acesso a dados financeiros e de comissionamento. |
| 4 | **Investidor** | Dono de usina(s), acesso a dados relacionados aos seus ativos. |
| 5 | **Consumidor** | Beneficiário do rateio de energia gerada. |
| — | **Vendedor** | Não é usuário do sistema. Cadastrado apenas para controle financeiro/comissionamento. |

---

## Tabela de Requisitos Funcionais

| **Código** | **Ator** | **Nome** | **Descrição** | **Prioridade** |
| :--------: | :------: | :------: | :------------ | :------------: |
| **RF01** | Empresa / Gerente | Cadastro de Usuários | A empresa ou o gerente pode cadastrar usuários no sistema, respeitando a hierarquia de papéis: a empresa cadastra gerentes e demais níveis; o gerente cadastra apenas usuários de nível inferior ao seu. | Alta |
| **RF02** | Empresa / Gerente | Atualização de Usuários | A empresa ou o gerente pode atualizar os dados cadastrais de usuários hierarquicamente inferiores já existentes no sistema, mantendo o histórico das alterações. | Alta |
| **RF03** | Empresa / Gerente | Ativação e Desativação de Usuários | A empresa ou o gerente pode ativar ou desativar usuários hierarquicamente inferiores, impedindo o acesso ao sistema sem excluir dados históricos. | Alta |
| **RF04** | Empresa / Gerente | Gerenciamento de Permissões | A empresa ou o gerente pode gerenciar permissões de acesso de usuários hierarquicamente inferiores, conforme o papel do usuário, garantindo acesso apenas às funcionalidades permitidas. | Alta |
| **RF05** | Empresa / Gerente | Listagem de Usuários | A empresa ou o gerente pode listar todos os usuários cadastrados vinculados à empresa, podendo usar filtros para a listagem. | Alta |
| **RF06** | Empresa / Gerente | Cadastro de Vendedores | A empresa ou o gerente pode cadastrar vendedores no sistema para fins de controle financeiro e comissionamento. O vendedor não possui acesso como usuário do sistema. | Alta |
| **RF07** | Empresa / Gerente | Cadastro de Usina | A empresa ou o gerente pode cadastrar usinas de geração de energia, informando dados técnicos, localização e vínculo com a empresa. | Alta |
| **RF08** | Empresa / Gerente | Atualização de Usina | A empresa ou o gerente pode atualizar os dados cadastrais e técnicos de uma usina, mantendo o histórico das alterações. | Alta |
| **RF09** | Empresa / Gerente | Ativação e Desativação de Usina | A empresa ou o gerente pode ativar ou desativar uma usina, impedindo seu uso em novos contratos sem excluir seus dados históricos. | Alta |
| **RF10** | Empresa / Gerente | Listagem de Usinas | A empresa ou o gerente pode listar e visualizar todas as usinas cadastradas da empresa, com filtros por status, localização e capacidade instalada. | Alta |
| **RF11** | Empresa / Gerente | Gerenciamento de Geração | A empresa ou o gerente acompanha e corrige dados de geração energética das usinas ao longo do tempo. | Alta |
| **RF12** | Empresa / Gerente | Vinculação de Analistas à Usina | A empresa ou o gerente pode vincular analistas energéticos e financeiros às usinas para permitir acesso aos dados conforme o papel. | Alta |
| **RF13** | Empresa / Gerente | Rateamento de Energia | A empresa ou o gerente pode configurar e gerenciar o rateamento da energia gerada por uma usina entre consumidores vinculados. | Alta |
| **RF14** | Empresa / Gerente / Analista Energético | Visualização de Indicadores da Usina | O ator pode visualizar indicadores consolidados de desempenho, geração, perdas e eficiência da usina. | Média |
| **RF15** | Empresa / Gerente | Histórico de Geração da Usina | A empresa ou o gerente pode visualizar o histórico completo de geração de energia da usina por período. | Média |
| **RF16** | Usuário | Visualizar Próprio Usuário | O usuário pode visualizar os seus próprios dados. | Média |
| **RF17** | Analista Energético / Analista Financeiro | Listagem de Usuários Vinculados às Usinas | O analista pode listar apenas usuários vinculados às usinas às quais ele também está vinculado, sem acesso a usuários fora desse escopo. | Média |
| **RF18** | Usuário | Atualização de Dados Próprios Não Sensíveis | O usuário pode atualizar apenas os próprios dados não sensíveis, mantendo o histórico das alterações e respeitando as regras de integridade. | Média |
| **RF19** | Empresa / Gerente | Confirmação Administrativa na Alteração de Status de Usuário | A ativação ou desativação de usuários deve exigir confirmação de senha do ator administrativo responsável pela ação. | Média |
| **RF20** | Analista Energético / Analista Financeiro | Listagem de Usinas Vinculadas | O analista pode listar e visualizar apenas as usinas às quais está vinculado, com filtros por status, localização e capacidade instalada. | Média |
| **RF21** | Empresa / Gerente | Listagem de Vendedores | A empresa ou o gerente pode listar os vendedores cadastrados vinculados à empresa, com filtros para consulta operacional e comercial. | Média |
| **RF22** | Empresa / Gerente | Atualização de Vendedores | A empresa ou o gerente pode atualizar os dados cadastrais e de comissionamento de vendedores vinculados à empresa, mantendo histórico das alterações. | Média |
| **RF23** | Empresa | Atualização de Dados da Empresa | A empresa pode atualizar os próprios dados cadastrais e de contato, mantendo histórico das alterações. | Média |
| **RF24** | Empresa / Gerente | Remoção de Vendedores | A empresa ou o gerente pode remover vendedores vinculados à própria empresa, respeitando as restrições de vínculo comercial/financeiro e mantendo rastreabilidade da ação. | Média |
