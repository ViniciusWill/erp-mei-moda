from pydantic import BaseModel, Field
from typing import Optional 


class Cliente(BaseModel):
    id: Optional[int] = None
    nome: str = Field(..., min_length=2, description="O nome deve ter pelo menos dois caracteres")
    cpf: Optional[str] = Field(None, min_length=11, max_length=11, description="CPF deve conter exatamente 11 numeros")
