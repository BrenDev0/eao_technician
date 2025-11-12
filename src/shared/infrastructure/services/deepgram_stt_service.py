from dotenv import load_dotenv
load_dotenv()

import asyncio
from typing import Any, Dict
import base64
import json
import os
import websockets
from src.shared.domain.services.speech_to_text import SpeechToText

class DeepgramSpeechToTextService(SpeechToText):
    def __init__(self, model: str = "nova-2", language: str = "es"):
        super().__init__()
        self.__model = model
        self.__language = language
        self.active_sessions: Dict[str, Any] = {}

    async def start_transcription_session(self):
        headers= {
            "Authorization": f"token {os.getenv("DEEPGRAM_API_KEY")}"
        }
        deepgram_ws = await websockets.connect(
            uri=f"wss://api.deepgram.com/v1/listen?encoding=opus&language={self.__language}&model={self.__model}",
            additional_headers=headers
        )
        session_id = f"session_{id(deepgram_ws)}"
        try:
            asyncio.create_task(self._listen_to_deepgram(session_id, deepgram_ws))
            session_data = {
                "connection": deepgram_ws,
                "transcript_parts": [],
                "is_active": True
            }

            self.active_sessions[session_id] = session_data
            return session_id
        
        except Exception as e:
            print(f"ERROR starting session: {e}")
            return None

    async def send_audio_chunk(self, session_id: str, audio_data: str):
        if session_id not in self.active_sessions:
            return
        
        session = self.active_sessions[session_id]
        connection = session["connection"]
        
        try:
            
            audio_bytes = self.get_audio_bytes(audio_data)
            if audio_bytes:
                await connection.send(audio_bytes)

        except websockets.exceptions.ConnectionClosed:
            print(f"Cannot send - Deepgram connection closed for session: {session_id}")
            session["is_active"] = False
        except Exception as e:
            print(f"Error sending audio chunk: {e}")
            session["is_active"] = False


    async def end_transcription_session(self, session_id: str) -> str:
        if session_id not in self.active_sessions:
            return ""
        
        session = self.active_sessions[session_id]
        connection = session["connection"]
        transcript_parts = session["transcript_parts"]
    
        try:
            await connection.close()
            
            full_transcript = " ".join(transcript_parts)
            # Clean up
            del self.active_sessions[session_id]
            
            print(f"Session ended: {session_id}")
            return full_transcript
            
        except Exception as e:
            print(f"Error ending session: {e}")
            return " ".join(transcript_parts)

    async def cleanup_session(self, session_id: str):

        if session_id in self.active_sessions:
            try:
                session = self.active_sessions[session_id]
                del self.active_sessions[session_id]
            except Exception as e:
                print(f"Error cleaning up session: {e}")

    def get_audio_bytes(self, data: Any) -> bytes:
        try:
            if isinstance(data, str):
                return base64.b64decode(data)
            elif isinstance(data, bytes):
                return data
            else:
                return b""
        except Exception as e:
            print(f"Error decoding audio: {e}")
            return b""
        
    async def _listen_to_deepgram(self, session_id: str, deepgram_ws: websockets.ClientConnection):
        try:
            async for message in deepgram_ws:
                if session_id not in self.active_sessions:
                    break
                    
                data = json.loads(message)
                
                # Handle different message types
                if data.get("type") == "Results":
                    transcript = data.get("channel", {}).get("alternatives", [{}])[0].get("transcript", "")
                    is_final = data.get("is_final", False)
                    
                    if transcript.strip():
                        session = self.active_sessions[session_id]
                        
                        if is_final:
                            session["transcript_parts"].append(transcript)
                        
        except websockets.exceptions.ConnectionClosed:
            print(f"Deepgram connection closed for session: {session_id}")
        except Exception as e:
            print(f"Error listening to Deepgram: {e}")
        finally:
            # Clean up session
            if session_id in self.active_sessions:
                self.active_sessions[session_id]["is_active"] = False