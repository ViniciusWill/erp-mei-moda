from pydantic import BaseModel, Field
from typing import Optional 


class Cliente(BaseModel):
    id: Optional[int] = None
    nome: str = Field(..., min_length=2, description="O nome deve ter pelo menos dois caracteres")
