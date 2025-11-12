from abc import ABC, abstractmethod
from typing import AsyncIterable
from typing import Any

class SpeechToText(ABC):
    @abstractmethod
    async def start_transcription_session(self, websocket: Any):
        raise NotImplementedError
    
    @abstractmethod
    async def send_audio_chunk(self, session_id: str, audio_data: str):
        raise NotImplementedError
    
    @abstractmethod
    async def end_transcription_session(self, session_id: str) -> str:
        raise NotImplementedError
    
    @abstractmethod
    async def cleanup_session(self, session_id: str):
        raise NotImplementedError
    
    @abstractmethod
    def get_audio_bytes(self, data: Any) -> bytes:
        raise NotImplementedError