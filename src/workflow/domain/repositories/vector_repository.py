# src/core/domain/services/vector_store_service.py
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

from src.workflow.domain.services.embedding_service import DocumentChunk
from src.workflow.domain.entities import SearchResult

class DeleteFilter(BaseModel):
    filename: Optional[str] = None
    user_id: Optional[str] = None  
    company_id: Optional[str] = None
    document_id: Optional[str] = None

class VectorRepository(ABC): 
    @abstractmethod
    async def similarity_search(
        self, 
        query_vector: List[float], 
        top_k: int = 4,
        namespace: Optional[str] = None
    ) -> List[SearchResult]:
        raise NotImplementedError
    