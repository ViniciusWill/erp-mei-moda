from pydantic import BaseModel, Field
from typing import Optional

class Participante(BaseModel):
    id: Optional[int] = None
    nome: str = Field(..., min_length=2, description="o nome deve ter pelo menos dois caracteres")
    cnpj: Optional[str] = Field(None, description="CNPJ do participante, se aplicável")