# ERP MEI Moda — v2.0

Sistema web de gestao para microempreendedores de moda. Controla vendas, compras, estoque, clientes, fornecedores, financeiro e relatorios em um unico lugar.

## Demonstracao online

[https://erp-mei.onrender.com/](https://erp-mei.onrender.com/)

---

## O que o sistema faz

- Lancamento de vendas e compras com parcelamento automatico
- Controle de estoque com atualizacao automatica por venda/compra
- Contas a pagar e a receber com acompanhamento de parcelas
- Cadastro de clientes e fornecedores (participantes)
- Relatorios de vendas, compras e financeiro
- Acesso de visitante com banco zerado para demonstracao
- Gerenciamento de acessos: roles de admin e operador
- Pre-autorizacao de emails para novos cadastros

---

## Arquitetura

```
app/
  database/
    orm_models.py       modelos SQLAlchemy (schema declarativo)
    db_config.py        engine principal, visitante e factory de testes
    base_repository.py  session manager com suporte a visitante e testes
    *_repository.py     repositories por dominio
  models/               modelos Pydantic (validacao de entrada)
  routes/               blueprints Flask por dominio
  services/             regras de negocio
  static/               css, js, imagens
  templates/            HTML Jinja2
alembic/                migrations de banco
  versions/             scripts versionados de alteracao de schema
Tests/
  test_post_routes.py   suite de testes com SQLAlchemy injetado
scripts/
  criar_usuario.py      cria usuario interativamente
  resetar_senha.py      reseta senha por nome/email/cpf
  resetar_senha_direto.py  reseta senha apontando direto para o .db
  sync_prod_to_test.py  copia producao para banco de teste
run.py
alembic.ini
requirements.txt
```

### Selecao de banco por contexto

| Contexto | Banco usado |
|---|---|
| `TEST_DATABASE_URL` definida | PostgreSQL de teste |
| `DATABASE_URL` definida (ou Render) | PostgreSQL de producao |
| Nenhuma variavel + local | SQLite `dados/sistema_loja.db` |
| Sessao de visitante | SQLite `dados/visitante.db` (zerado a cada acesso) |
| Testes automatizados | SQLite em memoria (injetado pelo fixture) |

---

## Requisitos

- Python 3.13 ou superior
- PostgreSQL (opcional — SQLite e usado localmente sem configuracao)

---

## Como rodar localmente

### 1. Clonar e criar ambiente virtual

```bash
git clone <url-do-repositorio>
cd erp-mei-moda
python -m venv venv
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Linux/macOS:
source venv/bin/activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar variaveis de ambiente (opcional)

Crie um arquivo `.env` na raiz seguindo o modelo `.env.example`.

Para rodar com PostgreSQL de teste localmente:
```env
TEST_DATABASE_URL=postgresql://usuario:senha@host:5432/banco_teste
```

Para envio de email (recuperacao de senha):
```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=seu@email.com
SMTP_PASSWORD=sua-senha-de-app
SMTP_USE_TLS=true
```

### 4. Criar as tabelas

```bash
alembic upgrade head
```

### 5. Criar usuario administrador

```bash
python scripts/criar_usuario.py
```

Depois, acesse a tela **Gerenciador de Acessos** para promover o usuario para `admin`.

Ou via script direto:

```bash
python scripts/resetar_senha.py
```

### 6. Rodar

```bash
python run.py
```

Acesse: `http://127.0.0.1:5000`

---

## Migrations com Alembic

O Alembic gerencia evolucoes de schema sem recriar o banco do zero.

```bash
# Ver estado atual das migrations
alembic current

# Verificar se ha diferencas entre modelos e banco
alembic check

# Gerar migration automatica apos alterar orm_models.py
alembic revision --autogenerate -m "descricao da mudanca"

# Aplicar todas as migrations pendentes
alembic upgrade head

# Reverter uma migration
alembic downgrade -1
```

---

## Controle de acesso (roles)

| Role | Permissoes |
|---|---|
| `admin` | Acesso total + Gerenciador de Acessos |
| `operador` | Acesso ao sistema sem tela de gerenciamento |

O admin pode:
- Promover ou rebaixar outros usuarios
- Pre-autorizar emails para novos cadastros (Primeiro Acesso)
- Revogar autorizacoes pendentes

**Regra:** um email so pode criar conta na tela de Primeiro Acesso se o admin o tiver adicionado na lista de emails autorizados.

---

## Acesso visitante

O botao **Sou Visitante** na tela de login:
- Reseta e recria o banco `dados/visitante.db` (zerado e limpo)
- Sessao expira em 1 hora
- Dados criados pelo visitante nao afetam o banco principal

---

## Scripts utilitarios

```bash
# Criar novo usuario
python scripts/criar_usuario.py

# Resetar senha por nome, email ou CPF (usa banco configurado no .env)
python scripts/resetar_senha.py

# Resetar senha apontando direto para um arquivo .db
python scripts/resetar_senha_direto.py

# Copiar producao para banco de teste
python scripts/sync_prod_to_test.py
python scripts/sync_prod_to_test.py --yes  # sem confirmacao interativa
```

---

## Testes

```bash
pytest Tests/test_post_routes.py -v -p no:cacheprovider
```

Os testes usam SQLAlchemy com SQLite em arquivo temporario (isolado por teste). Nao exigem conexao externa.

---

## Deploy (Render ou similar)

### Variaveis de ambiente obrigatorias

| Variavel | Descricao |
|---|---|
| `DATABASE_URL` | URL do PostgreSQL de producao |
| `SECRET_KEY` | Chave secreta Flask (gere uma aleatoria) |

### Variaveis opcionais

| Variavel | Descricao |
|---|---|
| `SMTP_HOST` / `SMTP_USER` / `SMTP_PASSWORD` | Configuracao de email para recuperacao de senha |

### Comando de start

```bash
alembic upgrade head && gunicorn run:app
```

O `alembic upgrade head` aplica migrations pendentes antes de subir o servidor. Nao e necessario rodar `setup_db.py` — o Alembic gerencia o schema completo.

---

## Observacoes

- Nao exponha `DATABASE_URL` ou `SECRET_KEY` em logs ou repositorios publicos.
- O arquivo `.env` ja esta no `.gitignore`. Nunca commite credenciais reais.
- Para o usuario final sem perfil tecnico, o formato recomendado e acesso via navegador com o sistema ja publicado online.
