from fastapi import Depends

from src.shared.application.use_cases.ws_streaming import WsStreaming
from src.shared.domain.services.text_to_speech import TextToSpeech
from src.shared.dependencies.services import get_text_to_speech_service, get_ws_transport_service
from src.api.websocket.transport import WebSocketTransportService


def get_ws_streaming_use_case(
    ws_tranport_service: WebSocketTransportService = Depends(get_ws_transport_service),
    tts_service: TextToSpeech = Depends(get_text_to_speech_service)
):
    return WsStreaming(
        ws_tansport_service=ws_tranport_service,
        tts_service=tts_service
    )