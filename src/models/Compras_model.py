from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class Compra(BaseModel):
    id: Optional[int] = None
    fornecedor_id: int
    estoque_id: int
    tamanho: str
    quantidade: int
    data_compra: datetime
    valor_unitario: float = Field(..., gt=0)


class ContaPagar(BaseModel):
    id: Optional[int] = None
    compra_id: int 
    parcela: int = Field(..., gt=0)
    valor_parcela: float = Field(..., gt=0)
    valor_pendente: float = Field(..., ge=0)
    data_vencimento: datetime
