from fastapi import Depends
import os 

from src.workflow.application.agents.technician import Technician

from src.workflow.domain.repositories.vector_repository import VectorRepository
from src.workflow.infrastructure.repositories.qdrant_vector_repository import QdrantVectorRepository, get_qdrant_client
from src.workflow.domain.services.embedding_service import EmbeddingService
from src.workflow.infrastructure.services.openai_embedding_service import OpenAIEmbeddingService
from src.workflow.domain.services.llm_service import LlmService
from src.workflow.infrastructure.services.langchain_llm_service import LangchainLlmService
from src.workflow.application.services.prompt_service import PromptService
from src.shared.dependencies.use_cases import get_ws_streaming_use_case
from src.shared.application.use_cases.ws_streaming import WsStreaming
from src.workflow.application.use_cases.search_for_context import SearchForContext


def get_vecotr_repository(
    client = Depends(get_qdrant_client)
) -> VectorRepository:
    return QdrantVectorRepository(
        client=client
    )

def get_embeddings_service() -> EmbeddingService:
    return OpenAIEmbeddingService(
        api_key=os.getenv("OPENAI_API_KEY")
    )


def get_llm_service() -> LlmService:
    return LangchainLlmService()


def get_prompt_service(
) -> PromptService:
    return PromptService()


def get_search_for_context_use_case(
    embedding_service: EmbeddingService = Depends(get_embeddings_service),
    repository: VectorRepository = Depends(get_vecotr_repository)
):
    return SearchForContext(
        embedding_service=embedding_service,
        vector_repository=repository
    )

def get_technician(
    llm_service: LlmService = Depends(get_llm_service),
    prompt_service: PromptService = Depends(get_prompt_service),
    streaming: WsStreaming = Depends(get_ws_streaming_use_case),
    search_context: SearchForContext = Depends(get_search_for_context_use_case)
) -> Technician:
    return Technician(
        llm_service=llm_service,
        prompt_service=prompt_service,
        streaming=streaming,
        search_context=search_context
    )

