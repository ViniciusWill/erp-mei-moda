# ERP MEI Moda

Versao 1.0 de um ERP web para lojas de roupas, pensado para ajudar microempreendedores a controlar vendas, compras, estoque e financeiro em um unico lugar.

Sistema web de gestao criado para ajudar microempreendedores a organizarem o dia a dia da loja de forma simples, visual e acessivel, mesmo sem familiaridade com tecnologia.

O projeto foi pensado para substituir controles manuais, anotacoes soltas e planilhas dificeis de manter, reunindo em um so lugar processos essenciais como:
- vendas
- compras
- estoque
- clientes
- participantes/fornecedores
- contas a pagar
- contas a receber
- relatorios

O objetivo principal e tornar a gestao mais acessivel para pequenos lojistas, oferecendo uma ferramenta clara para acompanhar a operacao e reduzir a dependencia de controles improvisados.

## Para quem este projeto foi pensado

Este sistema foi idealizado para microempreendedores que:
- precisam controlar melhor a loja
- nao tem facilidade com planilhas ou softwares complexos
- querem visualizar operacoes de forma mais organizada
- precisam de um sistema simples para acompanhar entradas, saidas e compromissos financeiros

## Como um usuario final deveria usar este sistema

Para o publico-alvo do projeto, a melhor forma de uso nao e instalar Python, abrir terminal ou configurar banco manualmente.

O formato mais adequado para um microempreendedor comum e:
- acessar o sistema por um link no navegador
- usar a aplicacao ja hospedada
- nao precisar instalar dependencias tecnicas
- nao precisar configurar banco de dados localmente

Em outras palavras: para um usuario final sem perfil tecnico, o ideal e que o sistema esteja publicado online ou empacotado de forma simples, e nao que ele precise rodar o projeto manualmente.

### Demonstracao online

[https://erp-mei.onrender.com/](https://erp-mei.onrender.com/)

## O uso local esta complexo para um usuario comum?

Sim. No estado atual do projeto, o fluxo local ainda e mais adequado para:
- desenvolvedores
- avaliadores tecnicos
- testes de portifolio

Hoje, para rodar localmente, e necessario:
- instalar Python
- instalar dependencias com `pip`
- criar as tabelas do banco
- popular dados iniciais
- iniciar a aplicacao manualmente

Isso nao e o fluxo ideal para o microempreendedor final.

Por isso, a proposta mais coerente com o objetivo do projeto e:
- disponibilizar o sistema online
- ou futuramente empacotar uma versao mais simples para instalacao local

## Sobre deploy e acesso web

O projeto pode ser publicado em plataformas de hospedagem para que o usuario acesse tudo pelo navegador.

No momento, uma alternativa pratica para portfolio e testes e o uso de plataformas como Render, porque elas permitem:
- publicar a aplicacao web rapidamente
- configurar variaveis de ambiente
- conectar com banco externo
- disponibilizar uma URL publica para demonstracao

Isso nao substitui uma estrutura corporativa maior, mas e suficiente para demonstracao funcional, validacao de ideia e portfolio tecnico.

## Requisitos para desenvolvimento local

- Python 3.13 ou superior
- `pip`

Opcional:
- PostgreSQL, se voce quiser rodar com banco externo

## Como rodar localmente para desenvolvimento ou avaliacao tecnica

### 1. Clonar o projeto
```bash
git clone <url-do-repositorio>
cd loja-roupa-py
```

### 2. Criar e ativar um ambiente virtual

Windows PowerShell:
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Windows CMD:
```bat
python -m venv venv
venv\Scripts\activate.bat
```

Linux/macOS:
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Instalar as dependencias
```bash
pip install -r requirements.txt
```

## Configuracao do banco

O projeto funciona de duas formas:

### Opcao A: uso local com SQLite
Nao precisa configurar nada.

Se a variavel `DATABASE_URL` nao existir, o sistema cria e usa automaticamente o arquivo local:

`dados/sistema_loja.db`

### Opcao B: uso local com PostgreSQL de teste
Defina a variavel de ambiente `TEST_DATABASE_URL` antes de iniciar a aplicacao.

Quando voce roda o projeto localmente, o sistema usa `TEST_DATABASE_URL` se ela existir.
Assim, voce evita alterar o banco de producao durante testes.

Exemplo:
```bash
TEST_DATABASE_URL=postgresql://usuario:senha@host:5432/banco_teste
```

No Windows PowerShell:
```powershell
$env:TEST_DATABASE_URL="postgresql://usuario:senha@host:5432/banco_teste"
```

Voce tambem pode criar um arquivo `.env` local seguindo o modelo de `.env.example`.

### Opcao C: uso em producao com PostgreSQL
No Render, configure a variavel de ambiente `DATABASE_URL` apontando para o banco de producao.

Em producao, nao use `TEST_DATABASE_URL`.

### Replicar producao para o banco local de teste
Para rodar localmente com os mesmos dados da producao, configure no seu `.env` local:

```env
PROD_DATABASE_URL=postgresql://usuario:senha@host:5432/banco_producao
TEST_DATABASE_URL=postgresql://usuario:senha@host:5432/banco_teste
```

Depois execute:

```bash
python scripts/sync_prod_to_test.py
```

O script apaga os dados do banco de teste e copia os dados atuais da producao.
Ele nao deve ser executado no Render.

Para rodar sem confirmacao interativa:

```bash
python scripts/sync_prod_to_test.py --yes
```

## Inicializacao do sistema

### 4. Criar as tabelas
```bash
python app/database/setup_db.py
```

### 5. Inserir dados iniciais de exemplo
```bash
python Tests/inserir_dados.py
```

Esse script pode ser executado mais de uma vez sem duplicar os registros principais.

## Executar a aplicacao

### 6. Rodar localmente
```bash
python run.py
```

Depois disso, acesse:

`http://127.0.0.1:5000`

## Fluxo recomendado para primeiro teste

Depois de abrir o sistema no navegador:

1. Acesse a tela inicial
2. Verifique os cadastros em Clientes e Participantes
3. Verifique os produtos em Estoque
4. Teste um lancamento em Vendas
5. Teste um lancamento em Compras
6. Consulte Contas a Pagar, Contas a Receber e Relatorios

Se voce executou `Tests/inserir_dados.py`, o sistema ja cria uma base minima para navegacao.

## Deploy

Fluxo recomendado de deploy:

1. configurar a variavel `DATABASE_URL` no ambiente, se usar PostgreSQL
2. instalar dependencias com `pip install -r requirements.txt`
3. executar a criacao das tabelas:
   `python app/database/setup_db.py`
4. opcionalmente inserir dados iniciais:
   `python Tests/inserir_dados.py`
5. iniciar o servidor WSGI:
   `gunicorn run:app`

Comando de start recomendado:
```bash
python app/database/setup_db.py && gunicorn run:app
```

Nao rode `python Tests/inserir_dados.py` no Start Command de producao. Esse script serve apenas para popular o banco de teste/desenvolvimento com dados de exemplo.

## Estrutura principal do projeto

```text
app/
  database/    acesso ao banco e repositories
  models/      entidades e validacoes
  routes/      blueprints e rotas da aplicacao
  services/    regras de negocio
  static/      css, js e imagens
  templates/   paginas HTML
Tests/
  inserir_dados.py
  test_post_routes.py
run.py
```

## Testes

Para rodar os testes principais de POST:
```bash
pytest Tests/test_post_routes.py -q -p no:cacheprovider
```

## Observacoes importantes

- O projeto usa nomes de arquivos sensiveis a maiusculas/minusculas em ambiente Linux.
- Em producao, nao exponha a `DATABASE_URL` em logs.
- Para ambiente local, o SQLite e suficiente para avaliacao e testes iniciais.
- Para o usuario final do projeto, o melhor formato de entrega e acesso via navegador, com a aplicacao ja publicada.

## Status atual

O projeto esta organizado em:
- blueprints para rotas
- service layer para regras de negocio
- repositories para persistencia
- suporte a SQLite e PostgreSQL
