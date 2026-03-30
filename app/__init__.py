from flask import Flask, app, cli, render_template, request, redirect, url_for, flash
from datetime import date, datetime
from app.services.compras_service import CompraService
from app.services.vendas_service import VendasService
from app.services.clientes_service import ClienteService
from app.services.participantes_service import ParticipanteService
from app.database.estoque_repository import EstoqueRepository
from app.database.Participantes_repository import ParticipantesRepository
from app.database.Clientes_repository import ClienteRepository
from app.database.Compras_repository import CompraRepository
from app.database.Vendas_repository import VendaRepository


def create_app():
    app = Flask(__name__)
    app.secret_key = "loja-roupa-key"

    @app.route("/")
    def index():
        return render_template("index.html", logo_header="imagens/logo.ico")

    @app.route("/vendas", methods=["GET", "POST"])
    def vendas():
        estoque_repo = EstoqueRepository()
        clientes_repo = ClienteRepository()

        if request.method == "POST":
            try:
                print("1 - Entrou no POST")

                cliente_id = int(request.form.get("cliente_id"))
                print("2 - cliente_id ok")

                estoque_id = int(request.form.get("estoque_id"))
                print("3 - estoque_id ok")

                quantidade = int(request.form.get("Quantidade-ven"))
                print("4 - quantidade ok")

                service = VendasService()
                print("5 - service criado")

                id_venda = service.realizar_venda(
                cliente_id=cliente_id,
                estoque_id=estoque_id,
                quantidade=quantidade
            )
                print("6 - venda realizada", id_venda)

          

            except Exception as e:
                flash(f"Erro ao lançar venda: {str(e)}", "erro")
        
        produtos      = estoque_repo.buscar_todos()
        clientes      = clientes_repo.buscar_todos()
        return render_template("vendas/venda.html", logo_header="imagens/venda.png", produtos=produtos, clientes=clientes)

    @app.route("/compras", methods=["GET", "POST"])
    def compras():
        estoque_repo       = EstoqueRepository()
        participantes_repo = ParticipantesRepository()

        if request.method == "POST":
            try:
                fornecedor_id = int(request.form.get("fornecedor_id"))
                estoque_id    = int(request.form.get("estoque_id"))
                quantidade    = int(request.form.get("quantidade"))
                parcelas      = int(request.form.get("parcelas"))

                service = CompraService()
                id_compra, valor_unitario = service.lançamento_compra(
                    fornecedor_id=fornecedor_id,
                    estoque_id=estoque_id,
                    quantidade=quantidade
                )

                if parcelas > 1:
                    service.lançamento_compra_parcelada(
                        compra_id=id_compra,
                        valor_unitario=valor_unitario,
                        quantidade=quantidade,
                        parcelas=parcelas
                    )

                flash("Compra lançada com sucesso!", "sucesso")
                return redirect(url_for("compras"))

            except Exception as e:
                flash(f"Erro ao lançar compra: {str(e)}", "erro")

        produtos      = estoque_repo.buscar_todos()
        participantes = participantes_repo.buscar_todos()

        return render_template("compras/compra.html",
                               logo_header="imagens/compra.png",
                               produtos=produtos,
                               participantes=participantes)
    

    @app.route("/estoque")
    def estoque():
        estoque_repo = EstoqueRepository()
        produtos = estoque_repo.buscar_todos()

        total_itens    = len(produtos)
        estoque_baixo  = sum(1 for p in produtos if 0 < p.quantidade <= 5)
        estoque_zerado = sum(1 for p in produtos if p.quantidade <= 0)

        return render_template(
            "estoque/estoque.html",
            logo_header="imagens/estoque.png",
            produtos=produtos,
            total_itens=total_itens,
            estoque_baixo=estoque_baixo,
            estoque_zerado=estoque_zerado,
        )

    @app.route("/financeiro/contas_pagar")
    def contas_pagar():
        repo   = CompraRepository()
        contas = repo.buscar_todos_apagar()
        hoje   = datetime.now()

        for c in contas:
            if c.data_vencimento.tzinfo is not None:
                c.data_vencimento = c.data_vencimento.replace(tzinfo=None)

        total_contas   = len(contas)
        total_pendente = sum(c.valor_pendente for c in contas if c.valor_pendente > 0)
        total_vencidas = sum(1 for c in contas if c.valor_pendente > 0 and c.data_vencimento < hoje)

        return render_template(
        "Financeiro/ContasPagar.html",
        logo_header="imagens/pagar.png",
        contas=contas,
        hoje=hoje,
        total_contas=total_contas,
        total_pendente=total_pendente,
        total_vencidas=total_vencidas,
    )
 
 
    @app.route("/financeiro/contas_receber")
    def contas_receber():
        repo = VendaRepository()
        contas = repo.buscar_todos_areceber()
        hoje   = datetime.now()

        for c in contas:
            if c.data_vencimento.tzinfo is not None:
                c.data_vencimento = c.data_vencimento.replace(tzinfo=None)
 
        total_contas   = len(contas)
        total_pendente = sum(c.valor_pendente for c in contas if c.valor_pendente > 0)
        total_vencidas = sum(1 for c in contas if c.valor_pendente > 0 and c.data_vencimento < hoje)
 
        return render_template(
        "Financeiro/ContasReceber.html",
        logo_header="imagens/receber.png",
        contas=contas,
        hoje=hoje,
        total_contas=total_contas,
        total_pendente=total_pendente,
        total_vencidas=total_vencidas,
    )

    @app.route("/clientes", methods=["GET", "POST"])  # <-- faltava isso
    def clientes():
  
        if request.method == "POST":
            try:
                nome = request.form.get("nome")
                service = ClienteService()
                service.LançamentoClienteCamposObrigatorios(nome=nome)
                flash("Cliente cadastrado com sucesso!", "sucesso")
                return redirect(url_for("clientes"))
            except  Exception as e:
                flash(f"Erro ao cadastrar cliente: {str(e)}", "erro")

        clientes_repo = ClienteRepository()
        cli = clientes_repo.buscar_todos()
        total_cli = len(cli)
        return render_template("clientes/clientes.html",
                               logo_header="imagens/Clientes.png",
                               cli=cli,
                               total_cli=total_cli)

    @app.route("/participantes", methods=["GET", "POST"])
    def participantes():
        if request.method == "POST":
            try:
                nome = request.form.get("nome")
                service = ParticipanteService()
                service.LançamentoParticipanteCampoObrigatorio(nome=nome)
                flash("Participante cadastrado com sucesso!", "sucesso")
                return redirect(url_for("participantes"))
            except  Exception as e:
                flash(f"Erro ao cadastrar participante: {str(e)}", "erro")

        participantes_repo = ParticipantesRepository()
        partic = participantes_repo.buscar_todos()
        total_partic = len(partic)
        return render_template("participantes/participantes.html",
                               logo_header="imagens/participantes.png",
                               partic=partic,
                               total_partic=total_partic)
    return app