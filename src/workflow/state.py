from typing_extensions import TypedDict
from  uuid import UUID
from typing import Dict, List, Any, Optional

class State(TypedDict):
    company_id: UUID
    chat_history: List[Dict[str, Any]]
    input: str
    final_response: str
    chat_id: UUID
    voice: Optional[bool] = False