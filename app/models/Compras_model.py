from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime


class Compra(BaseModel):
    id: Optional[int] = None
    estoque_id: int
    fornecedor_id: int
    quantidade: int
    valor_unitario: float = Field(..., gt=0)
    data_compra: datetime

class ContaPagar(BaseModel):
    id: Optional[int] = None
    compra_id: int
    parcela: int = Field(..., gt=0)
    valor_parcela: float = Field(..., gt=0)
    valor_pendente: float = Field(..., ge=0)
    data_vencimento: datetime

