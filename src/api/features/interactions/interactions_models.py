from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from uuid import UUID

class InteractionRequest(BaseModel):
    input: str
    chat_id: UUID
    company_id: UUID
    chat_history: List[Dict[str, Any]]
    user_id: UUID
    voice: Optional[bool] = False

class  InteractionResponse(BaseModel):
    response: str