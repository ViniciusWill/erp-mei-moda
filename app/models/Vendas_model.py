from pydantic import BaseModel, Field
from typing import Optional 
from datetime import datetime


class Venda(BaseModel):
    id: Optional[int] = None   
    cliente_id: int
    estoque_id: int
    quantidade: int = Field(..., gt=0)
    valor_unitario: float = Field(..., gt=0)
    data_venda: datetime


class ContaReceber(BaseModel):
    id: Optional[int] = None
    venda_id: int
    parcela: int = Field(..., gt=0)
    valor_parcela: float = Field(..., gt=0)
    valor_pendente: float = Field(..., ge=0)
    data_vencimento: datetime