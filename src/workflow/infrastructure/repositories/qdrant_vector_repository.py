from typing import List
import os
from qdrant_client import QdrantClient
from src.workflow.domain.repositories.vector_repository import VectorRepository
from src.workflow.domain.entities import SearchResult

def get_qdrant_client():
    return QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY")
    )

class QdrantVectorRepository(VectorRepository):
    def __init__(self, client: QdrantClient):
        self.client = client

    async def similarity_search(
        self, 
        namespace: str,
        query_vector: List[float], 
        top_k: int = 4
    ) -> List[SearchResult]:
        results = self.client.search(
            collection_name=namespace,
            query_vector=query_vector,
            limit=top_k,
            with_payload=True
        )
        
        return [
            SearchResult(
                id=point.id,
                score=point.score,
                payload=point.payload,
                text=point.payload.get("text"),
                metadata=point.payload.get("metadata") 
            )
            for point in results
        ]