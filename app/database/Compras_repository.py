from datetime import datetime

from sqlalchemy import select, delete

from app.database.base_repository import BaseRepository
from app.database.orm_models import (
    Compra as CompraORM,
    ContaPagar as ContaPagarORM,
    Estoque as EstoqueORM,
    Participante as ParticipanteORM,
)
from app.models.Compras_model import Compra, ContaPagar


class CompraRepository(BaseRepository):

    def lancamento_compra(self, compra: Compra, nova_qtd_estoque: int):
        with self._session() as session:
            nova_compra = CompraORM(
                estoque_id=compra.estoque_id,
                fornecedor_id=compra.fornecedor_id,
                quantidade=compra.quantidade,
                valor_unitario=compra.valor_unitario,
                data_compra=compra.data_compra.strftime("%Y-%m-%d %H:%M:%S"),
            )
            session.add(nova_compra)
            session.flush()

            estoque = session.get(EstoqueORM, compra.estoque_id)
            estoque.quantidade = nova_qtd_estoque

            return nova_compra.id, compra.valor_unitario

    def lancamento_compra_parcelada(self, nova_parcela: ContaPagar):
        with self._session() as session:
            parcela = ContaPagarORM(
                compra_id=nova_parcela.compra_id,
                parcela=nova_parcela.parcela,
                valor_parcela=nova_parcela.valor_parcela,
                valor_pendente=nova_parcela.valor_pendente,
                data_vencimento=str(nova_parcela.data_vencimento),
            )
            session.add(parcela)

    def buscar_todos_apagar(self):
        with self._session() as session:
            rows = session.execute(select(ContaPagarORM)).scalars().all()
            return [
                ContaPagar(
                    id=r.id,
                    compra_id=r.compra_id,
                    parcela=r.parcela,
                    valor_parcela=r.valor_parcela,
                    valor_pendente=r.valor_pendente,
                    data_vencimento=r.data_vencimento,
                )
                for r in rows
            ]

    def selecionar_todas_compras(self):
        with self._session() as session:
            stmt = (
                select(CompraORM)
                .join(EstoqueORM, CompraORM.estoque_id == EstoqueORM.id)
                .join(ParticipanteORM, CompraORM.fornecedor_id == ParticipanteORM.id)
            )
            rows = session.execute(stmt).scalars().all()
            resultado = []
            for row in rows:
                data = row.data_compra
                if isinstance(data, str):
                    data = datetime.strptime(data[:10], "%Y-%m-%d")
                resultado.append({
                    "id": row.id,
                    "fornecedor_id": row.fornecedor_id,
                    "estoque_id": row.estoque_id,
                    "quantidade": row.quantidade,
                    "valor_unitario": row.valor_unitario,
                    "data_compra": data,
                    "nome_produto": row.estoque.nome_produto,
                    "tamanho_produto": row.estoque.tamanho,
                    "nome_fornecedor": row.fornecedor.nome,
                })
            return resultado

    def excluir_por_id(self, id: int):
        with self._session() as session:
            session.execute(delete(ContaPagarORM).where(ContaPagarORM.compra_id == id))
            session.execute(delete(CompraORM).where(CompraORM.id == id))
