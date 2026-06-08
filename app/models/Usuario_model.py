from pydantic import BaseModel, Field
from typing import Optional

class Usuario(BaseModel):
    id: Optional[int] = None
    nome: str = Field(..., min_length=1)
    email: str = Field(..., min_length=1)
    cpf: str = Field(..., min_length=11, max_length=14)
    cnpj: Optional[str] = Field(None, min_length=14, max_length=18)
    senha_hash: str = Field(..., min_length=6)
    role: str = "operador"
