from abc import ABC, abstractmethod
from typing import AsyncGenerator, Type, TypeVar
from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)

class LlmService(ABC):
    @abstractmethod
    async def generate_stream(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = None
    ) -> AsyncGenerator[str, None]:
        raise NotImplementedError
    
    @abstractmethod
    async def invoke(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = None
    ) -> str:
        raise NotImplementedError

    @abstractmethod
    async def invoke_structured(
        self,
        prompt: str,
        response_model: Type[T],
        temperature: float = 0.7,
        max_tokens: int = None
    ) -> T:
        raise NotImplementedError