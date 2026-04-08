from .compras_routes import compras_bp
from .clientes_routes import clientes_bp
from .contas_a_pagar_routes import contas_a_pagar_bp    
from .contas_a_receber_routes import contas_a_receber_bp
from .estoque_routes import estoque_bp
from .participantes_routes import participantes_bp
from .vendas_routes import vendas_bp
from .relatorios_routes import relatorios_bp


def register_blueprints(app):
    app.register_blueprint(compras_bp)
    app.register_blueprint(clientes_bp)
    app.register_blueprint(contas_a_pagar_bp)
    app.register_blueprint(contas_a_receber_bp)
    app.register_blueprint(estoque_bp)
    app.register_blueprint(participantes_bp)
    app.register_blueprint(vendas_bp)
    app.register_blueprint(relatorios_bp)