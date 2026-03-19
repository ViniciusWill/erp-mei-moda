from flask import Flask, render_template

def create_app():
    app = Flask(__name__)

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/vendas")
    def vendas():
        return render_template("vendas/venda.html")

    @app.route("/compras")
    def compras():
        return render_template("compras/compra.html")

    @app.route("/estoque")
    def estoque():
        return render_template("estoque/estoque.html")

    @app.route("/Financeiro/contas_pagar")
    def contas_pagar():
        return render_template("Financeiro/ContasPagar.html")

    @app.route("/Financeiro/contas_receber")
    def contas_receber():
        return render_template("Financeiro/ContasReceber.html")

    @app.route("/clientes")
    def clientes():
        return render_template("clientes/clientes.html")

    @app.route("/participantes")
    def participantes():
        return render_template("participantes/participantes.html")

    return app