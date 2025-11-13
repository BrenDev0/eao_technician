from typing import List, Optional

from src.workflow.domain.services.embedding_service import EmbeddingService
from src.workflow.domain.repositories.vector_repository import VectorRepository

class SearchForContext():
    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_repository: VectorRepository
    ):
        self.__embedding_service = embedding_service
        self.__repository = vector_repository

    
    async def execute(
        self,
        input: str,
        namespace: str,
        top_k: int = 5,
        score_threshold: Optional[float] = None
    ) -> str:
        query_vector = await self.__embedding_service.embed_query(input)
        results = await self.__repository.similarity_search(
            query_vector=query_vector,
            top_k=top_k,
            namespace=namespace,
            score_threshold=score_threshold
        )

        context = "\n".join([result.text for result in results if result.text])
        return context