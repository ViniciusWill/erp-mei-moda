 Sistema ERP para Gestão de Loja de Roupas 

📝 Descrição
Sistema de gestão operacional e financeiro para varejo, desenvolvido em Python com foco absoluto em usabilidade, integridade de dados e acessibilidade.

O projeto foi idealizado especificamente para o microempreendedor brasileiro, visando democratizar o controle profissional de pequenos negócios através de uma ferramenta intuitiva. O objetivo é remover as barreiras tecnológicas para quem precisa gerenciar vendas, estoque e finanças, mas não possui familiaridade com softwares complexos ou planilhas confusas.


🚀 Evolução e Arquitetura
O sistema nasceu como uma ferramenta de automação e validação de dados utilizando Pandas e Excel, evoluindo para uma aplicação robusta com persistência em banco de dados relacional SQLite.

A arquitetura atual utiliza o padrão Service Layer (Camada de Serviços), separando as regras de negócio da persistência de dados (Repositories). Isso garante:
 - Baixa curva de aprendizado: Interface interativa e guiada, pensada no fluxo de trabalho real do lojista.
 - Confiabilidade: Validação rigorosa de tipos e dados com Pydantic, evitando erros de digitação comuns no dia a dia.
 - Escalabilidade: Estrutura profissional preparada para expansão e migração para outros bancos de dados.

✨ Diferenciais para o Microempreendedor
- Segurança de Dados: Diferente do Excel, onde registros podem ser apagados acidentalmente, o uso do SQLite garante a integridade histórica dos lançamentos.
- Validação Inteligente: O sistema impede entradas inválidas (como letras em campos de valor), reduzindo drasticamente o retrabalho financeiro.
- Processos Simplificados: Fluxos de compra e venda que automatizam o cálculo de estoque de forma transparente.


🛠️ Tecnologias Utilizadas
- Python 3.13+: Linguagem core.
- SQLite3: Banco de dados relacional embutido para persistência local.
- Pydantic: Validação de esquemas e entidades.


⚙️ Funcionalidades Implementadas
- Persistência Relacional: Dados armazenados de forma estruturada em tabelas SQL.
- Gestão de Compras: Fluxo que valida a existência de produtos no estoque via ID.
- Gestão de Vendas: Baixa automática em estoque e registro de transações financeiras.
= Cadastro de Participantes: Validação rigorosa de tipos para Clientes e Fornecedores.


📂 Estrutura de Pastas (Refletindo o Banco)
loja-roupa-py/
├── src/
│   ├── database/           # Repositórios (Queries SQL e comandos ao SQLite)
│   ├── models/             # Modelos Pydantic (Garantia de tipos)
│   ├── services/           # Regras de Negócio (Onde a lógica acontece)
│   └── main.py             # CLI - Interface de linha de comando
├── data/
│   └── sistema_loja.db     # O Banco de Dados SQLite
└── requirements.txt

📈 Roadmap — Próximos Passos
- Migração para PostgreSQL: Preparar o sistema para ambientes multiusuário.
- Interface Web (FastAPI): Expor os serviços para uma interface moderna.
- Relatórios Financeiros: Geração de PDFs com fechamento de caixa mensal.
- Autenticação: Sistema de login para diferentes níveis de acesso.



-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

🚀 Como Executar
- Clonar e Acessar:
git clone <url-do-repositorio>
cd loja-roupa-py

- Ambiente Virtual:
python -m venv venv
./venv/Scripts/activate  # Windows

- Instalar Dependências:
pip install -r requirements.txt

- Rodar o Sistema:
python src/main.py