import tiktoken
from typing import List
from openai import AsyncOpenAI

from src.workflow.domain.services.embedding_service import EmbeddingService

class OpenAIEmbeddingService(EmbeddingService):
    def __init__(self, api_key: str, model: str = "text-embedding-3-large"):
        self._client = AsyncOpenAI(api_key=api_key)
        self._model = model
        self._encoding = tiktoken.get_encoding("cl100k_base")
    
    async def embed_query(self, query: str) -> List[float]:
        """Embed a single query"""
        result = await self._client.embeddings.create(
            model=self._model,
            input=query
        )
        return result.data[0].embedding
