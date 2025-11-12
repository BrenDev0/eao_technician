from abc import ABC, abstractmethod

class TextToSpeech(ABC):
    @abstractmethod
    def transcribe(text: str):
        raise NotImplementedError