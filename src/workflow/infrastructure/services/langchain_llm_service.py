from typing import AsyncGenerator
from langchain_openai import ChatOpenAI

from src.workflow.domain.services.llm_service import LlmService
from src.shared.utils.decorators.error_hanlder import error_handler

class LangchainLlmService(LlmService):
    __MODULE = "langchain.llm_service"
    def __init__(self, model: str = "gpt-4o"):
        self.model = model
    
    @error_handler(module=__MODULE)
    async def generate_stream(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = None
    ) -> AsyncGenerator[str, None]:
        llm = ChatOpenAI(
            model=self.model,
            temperature=temperature,
            max_tokens=max_tokens,
            streaming=True
        )
        
        async for chunk in llm.astream(prompt):
            yield chunk.content
    
    @error_handler(module=__MODULE)
    async def invoke(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = None
    ) -> str:
        llm = ChatOpenAI(
            model=self.model,
            temperature=temperature,
            max_tokens=max_tokens
        )
        response = await llm.ainvoke(prompt)
        return response.content.strip()
    
    async def invoke_structured(
            self, 
            prompt: str, 
            response_model, 
            temperature: float = 0.7, 
            max_tokens: int = None
        ):
        llm = ChatOpenAI(
            model=self.model,
            temperature=temperature,
            max_tokens=max_tokens
        )

        structured_llm = llm.with_structured_output(response_model)
        response = await structured_llm.ainvoke(prompt)
        return response
        