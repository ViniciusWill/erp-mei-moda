from pydantic import BaseModel, Field
from typing import Optional


class Estoque(BaseModel):
    id: Optional[int] = None
    nome_produto: str
    tamanho: str = 0
    quantidade: int = Field(..., ge=0, description="A quantidade em estoque não pode ser negativo")
    valor_compra: float = Field(..., gt=0, description="O valor de compra deve ser maior que zero")
