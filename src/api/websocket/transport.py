from websockets import ConnectionClosed
from typing import Union, Any
from uuid import UUID
from src.api.websocket.connections import WebsocketConnectionsContainer

class WebSocketTransportService:
    @staticmethod
    async def send(
        connection_id: Union[str, UUID],
        data: Any
    ):
        ws = WebsocketConnectionsContainer.resolve_connection(connection_id=connection_id)

        if ws:
            try: 
                await ws.send_json(data)
            
            except ConnectionClosed:
                print(f"Connection {connection_id} disconnected")

            except Exception as e:
                print(f"Connection id: {connection_id}::::, Error sending data:::: {e}")
                raise e