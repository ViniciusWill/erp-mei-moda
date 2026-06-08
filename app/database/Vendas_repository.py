from datetime import datetime

from sqlalchemy import select, delete

from app.database.base_repository import BaseRepository
from app.database.orm_models import (
    Cliente as ClienteORM,
    ContaReceber as ContaReceberORM,
    Estoque as EstoqueORM,
    Venda as VendaORM,
)
from app.models.Vendas_model import ContaReceber, Venda


class VendaRepository(BaseRepository):

    def lancamento_venda(self, venda: Venda, nova_qtd_estoque: int):
        with self._session() as session:
            nova_venda = VendaORM(
                cliente_id=venda.cliente_id,
                estoque_id=venda.estoque_id,
                quantidade=venda.quantidade,
                valor_unitario=venda.valor_unitario,
                data_venda=venda.data_venda.strftime("%Y-%m-%d %H:%M:%S"),
            )
            session.add(nova_venda)
            session.flush()

            estoque = session.get(EstoqueORM, venda.estoque_id)
            estoque.quantidade = nova_qtd_estoque

            return nova_venda.id, venda.valor_unitario

    def lancamento_venda_parcelada(self, nova_parcela: ContaReceber):
        with self._session() as session:
            parcela = ContaReceberORM(
                venda_id=nova_parcela.venda_id,
                parcela=nova_parcela.parcela,
                valor_parcela=nova_parcela.valor_parcela,
                valor_pendente=nova_parcela.valor_pendente,
                data_vencimento=str(nova_parcela.data_vencimento),
            )
            session.add(parcela)

    def buscar_todos_areceber(self):
        with self._session() as session:
            rows = session.execute(select(ContaReceberORM)).scalars().all()
            return [
                ContaReceber(
                    id=r.id,
                    venda_id=r.venda_id,
                    parcela=r.parcela,
                    valor_parcela=r.valor_parcela,
                    valor_pendente=r.valor_pendente,
                    data_vencimento=r.data_vencimento,
                )
                for r in rows
            ]

    def selecionar_todas_vendas(self):
        with self._session() as session:
            stmt = (
                select(VendaORM)
                .join(EstoqueORM, VendaORM.estoque_id == EstoqueORM.id)
                .join(ClienteORM, VendaORM.cliente_id == ClienteORM.id)
            )
            rows = session.execute(stmt).scalars().all()
            resultado = []
            for row in rows:
                data = row.data_venda
                if isinstance(data, str):
                    data = datetime.strptime(data[:10], "%Y-%m-%d")
                resultado.append({
                    "id": row.id,
                    "cliente_id": row.cliente_id,
                    "estoque_id": row.estoque_id,
                    "quantidade": row.quantidade,
                    "valor_unitario": row.valor_unitario,
                    "data_venda": data,
                    "nome_produto": row.estoque.nome_produto,
                    "tamanho_produto": row.estoque.tamanho,
                    "nome_cliente": row.cliente.nome,
                })
            return resultado

    def excluir_por_id(self, id: int):
        with self._session() as session:
            session.execute(delete(ContaReceberORM).where(ContaReceberORM.venda_id == id))
            session.execute(delete(VendaORM).where(VendaORM.id == id))
