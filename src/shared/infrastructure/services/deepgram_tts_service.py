from deepgram import DeepgramClient
import base64
from src.shared.domain.services.text_to_speech import TextToSpeech

class DeepgramTextToSpeechService(TextToSpeech):
    def __init__(
        self,
        model: str = "aura-2-estrella-es"
    ):
        super().__init__()
        self.__model = model

    def  transcribe(self, text: str):
        deepgram = DeepgramClient()
        if text:
            response = deepgram.speak.v1.audio.generate(
                text=text,
                model= self.__model
            )
        
            audio_bytes = b"".join(response)      
            
            return base64.b64encode(audio_bytes).decode('utf-8')