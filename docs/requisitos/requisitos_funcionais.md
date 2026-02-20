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
| <a id="rf01"></a>[**RF01**](#rf01) | Empresa / Gerente | Cadastro de Usuários | A empresa ou o gerente pode cadastrar usuários no sistema, respeitando a hierarquia de papéis: a empresa cadastra gerentes e demais níveis; o gerente cadastra apenas usuários de nível inferior ao seu. | Alta |
| <a id="rf02"></a>[**RF02**](#rf02) | Empresa / Gerente | Atualização de Usuários | A empresa ou o gerente pode atualizar os dados cadastrais de usuários hierarquicamente inferiores já existentes no sistema, mantendo o histórico das alterações. | Alta |
| <a id="rf03"></a>[**RF03**](#rf03) | Empresa / Gerente | Ativação e Desativação de Usuários | A empresa ou o gerente pode ativar ou desativar usuários hierarquicamente inferiores, impedindo o acesso ao sistema sem excluir dados históricos. | Alta |
| <a id="rf04"></a>[**RF04**](#rf04) | Empresa / Gerente | Gerenciamento de Permissões | A empresa ou o gerente pode gerenciar permissões de acesso de usuários hierarquicamente inferiores, conforme o papel do usuário, garantindo acesso apenas às funcionalidades permitidas. | Alta |
| <a id="rf05"></a>[**RF05**](#rf05) | Empresa / Gerente | Listagem de Usuários | A empresa ou o gerente pode listar todos os usuários cadastrados vinculados à empresa, podendo usar filtros para a listagem. | Alta |
| <a id="rf06"></a>[**RF06**](#rf06) | Empresa / Gerente | Cadastro de Vendedores | A empresa ou o gerente pode cadastrar vendedores no sistema para fins de controle financeiro e comissionamento. O vendedor não possui acesso como usuário do sistema. | Alta |
| <a id="rf07"></a>[**RF07**](#rf07) | Empresa / Gerente | Cadastro de Usina | A empresa ou o gerente pode cadastrar usinas de geração de energia, informando dados técnicos, localização e vínculo com a empresa. | Alta |
| <a id="rf08"></a>[**RF08**](#rf08) | Empresa / Gerente | Atualização de Usina | A empresa ou o gerente pode atualizar os dados cadastrais e técnicos de uma usina, mantendo o histórico das alterações. | Alta |
| <a id="rf09"></a>[**RF09**](#rf09) | Empresa / Gerente | Ativação e Desativação de Usina | A empresa ou o gerente pode ativar ou desativar uma usina, impedindo seu uso em novos contratos sem excluir seus dados históricos. | Alta |
| <a id="rf10"></a>[**RF10**](#rf10) | Empresa / Gerente | Listagem de Usinas | A empresa ou o gerente pode listar e visualizar todas as usinas cadastradas da empresa, com filtros por status, localização e capacidade instalada. | Alta |
| <a id="rf11"></a>[**RF11**](#rf11) | Empresa / Gerente | Gerenciamento de Geração | A empresa ou o gerente acompanha e corrige dados de geração energética das usinas ao longo do tempo. | Alta |
| <a id="rf12"></a>[**RF12**](#rf12) | Empresa / Gerente | Vinculação de Analistas à Usina | A empresa ou o gerente pode vincular analistas energéticos e financeiros às usinas para permitir acesso aos dados conforme o papel. | Alta |
| <a id="rf13"></a>[**RF13**](#rf13) | Empresa / Gerente | Rateamento de Energia | A empresa ou o gerente pode configurar e gerenciar o rateamento da energia gerada por uma usina entre consumidores vinculados. | Alta |
| <a id="rf14"></a>[**RF14**](#rf14) | Empresa / Gerente / Analista Energético | Visualização de Indicadores da Usina | O ator pode visualizar indicadores consolidados de desempenho, geração, perdas e eficiência da usina. | Média |
| <a id="rf15"></a>[**RF15**](#rf15) | Empresa / Gerente | Histórico de Geração da Usina | A empresa ou o gerente pode visualizar o histórico completo de geração de energia da usina por período. | Média |
| <a id="rf16"></a>[**RF16**](#rf16) | Usuário | Visualizar Próprio Usuário | O usuário pode visualizar os seus próprios dados. | Média |
| <a id="rf17"></a>[**RF17**](#rf17) | Analista Energético / Analista Financeiro | Listagem de Usuários Vinculados às Usinas | O analista pode listar apenas usuários vinculados às usinas às quais ele também está vinculado, sem acesso a usuários fora desse escopo. | Média |
| <a id="rf18"></a>[**RF18**](#rf18) | Usuário | Atualização de Dados Próprios Não Sensíveis | O usuário pode atualizar apenas os próprios dados não sensíveis, mantendo o histórico das alterações e respeitando as regras de integridade. | Média |
| <a id="rf19"></a>[**RF19**](#rf19) | Empresa / Gerente | Confirmação Administrativa na Alteração de Status de Usuário | A ativação ou desativação de usuários deve exigir confirmação de senha do ator administrativo responsável pela ação. | Média |
| <a id="rf20"></a>[**RF20**](#rf20) | Analista Energético / Analista Financeiro | Listagem de Usinas Vinculadas | O analista pode listar e visualizar apenas as usinas às quais está vinculado, com filtros por status, localização e capacidade instalada. | Média |
| <a id="rf21"></a>[**RF21**](#rf21) | Empresa / Gerente | Listagem de Vendedores | A empresa ou o gerente pode listar os vendedores cadastrados vinculados à empresa, com filtros para consulta operacional e comercial. | Média |
| <a id="rf22"></a>[**RF22**](#rf22) | Empresa / Gerente | Atualização de Vendedores | A empresa ou o gerente pode atualizar os dados cadastrais e de comissionamento de vendedores vinculados à empresa, mantendo histórico das alterações. | Média |
| <a id="rf23"></a>[**RF23**](#rf23) | Empresa | Atualização de Dados da Empresa | A empresa pode atualizar os próprios dados cadastrais e de contato, mantendo histórico das alterações. | Média |
| <a id="rf24"></a>[**RF24**](#rf24) | Empresa / Gerente | Remoção de Vendedores | A empresa ou o gerente pode remover vendedores vinculados à própria empresa, respeitando as restrições de vínculo comercial/financeiro e mantendo rastreabilidade da ação. | Média |
