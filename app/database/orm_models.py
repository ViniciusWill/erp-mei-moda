from sqlalchemy import Column, Integer, String, Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False, unique=True)
    cpf = Column(String(11))

    vendas = relationship("Venda", back_populates="cliente")


class Estoque(Base):
    __tablename__ = "estoque"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome_produto = Column(String, nullable=False)
    tamanho = Column(String, nullable=False)
    quantidade = Column(Integer, nullable=False)
    valor_compra = Column(Float, nullable=False)

    __table_args__ = (UniqueConstraint("nome_produto", "tamanho"),)

    vendas = relationship("Venda", back_populates="estoque")
    compras = relationship("Compra", back_populates="estoque")


class Participante(Base):
    __tablename__ = "participantes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False, unique=True)
    cnpj = Column(String(14))

    compras = relationship("Compra", back_populates="fornecedor")


class Venda(Base):
    __tablename__ = "vendas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    estoque_id = Column(Integer, ForeignKey("estoque.id"), nullable=False)
    quantidade = Column(Integer, nullable=False)
    valor_unitario = Column(Float, nullable=False)
    data_venda = Column(String, nullable=False)

    cliente = relationship("Cliente", back_populates="vendas")
    estoque = relationship("Estoque", back_populates="vendas")
    parcelas = relationship("ContaReceber", back_populates="venda")


class ContaReceber(Base):
    __tablename__ = "contas_a_receber"

    id = Column(Integer, primary_key=True, autoincrement=True)
    venda_id = Column(Integer, ForeignKey("vendas.id"), nullable=False)
    parcela = Column(Integer, nullable=False)
    valor_parcela = Column(Float, nullable=False)
    valor_pendente = Column(Float, nullable=False)
    data_vencimento = Column(String, nullable=False)

    venda = relationship("Venda", back_populates="parcelas")


class Compra(Base):
    __tablename__ = "compras"

    id = Column(Integer, primary_key=True, autoincrement=True)
    estoque_id = Column(Integer, ForeignKey("estoque.id"), nullable=False)
    fornecedor_id = Column(Integer, ForeignKey("participantes.id"), nullable=False)
    quantidade = Column(Integer, nullable=False)
    valor_unitario = Column(Float, nullable=False)
    data_compra = Column(String, nullable=False)

    estoque = relationship("Estoque", back_populates="compras")
    fornecedor = relationship("Participante", back_populates="compras")
    parcelas = relationship("ContaPagar", back_populates="compra")


class ContaPagar(Base):
    __tablename__ = "contas_a_pagar"

    id = Column(Integer, primary_key=True, autoincrement=True)
    compra_id = Column(Integer, ForeignKey("compras.id"), nullable=False)
    parcela = Column(Integer, nullable=False)
    valor_parcela = Column(Float, nullable=False)
    valor_pendente = Column(Float, nullable=False)
    data_vencimento = Column(String, nullable=False)

    compra = relationship("Compra", back_populates="parcelas")


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    cpf = Column(String(11))
    cnpj = Column(String(18))
    email = Column(String(255), nullable=False)
    senha_hash = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, server_default="operador")

    recuperacoes = relationship("RecuperacaoSenha", back_populates="usuario")


class EmailAutorizado(Base):
    __tablename__ = "emails_autorizados"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False, unique=True)
    usado = Column(Integer, nullable=False, server_default="0")  # 0=pendente, 1=usado
    criado_em = Column(String, nullable=False)


class RecuperacaoSenha(Base):
    __tablename__ = "recuperacao_senha"

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    codigo_hash = Column(String(255), nullable=False)
    expira_em = Column(String, nullable=False)
    usado_em = Column(String)
    criado_em = Column(String, nullable=False)

    usuario = relationship("Usuario", back_populates="recuperacoes")
