from fastapi import Depends
from src.shared.domain.services.speech_to_text import SpeechToText
from src.shared.domain.services.text_to_speech import TextToSpeech
from src.shared.infrastructure.services.deepgram_stt_service import DeepgramSpeechToTextService
from src.api.websocket.transport import WebSocketTransportService

from src.shared.infrastructure.services.deepgram_tts_service import DeepgramTextToSpeechService

def get_ws_transport_service() -> WebSocketTransportService:
    return WebSocketTransportService()


def get_speech_to_text_service() -> SpeechToText:
    return DeepgramSpeechToTextService(
        model="nova",
        language="es"
    )

def get_text_to_speech_service() -> TextToSpeech:
    return DeepgramTextToSpeechService(
        model="aura-2-celeste-es"
    )

