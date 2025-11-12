from typing import Union, Dict, Any
from uuid import UUID

class WebsocketConnectionsContainer:
    _active_connections: Dict[str, Any] = {}

    @classmethod
    def register_connection(cls, connection_id: Union[UUID, str], websocket: Any):
        key = str(connection_id)
        cls._active_connections[key] = websocket
        print(f"connection {key} added.")
        return
    
    @classmethod
    def resolve_connection(cls, connection_id: Union[UUID, str]) -> Any:
        key = str(connection_id)
        connection = cls._active_connections.get(key)
        if not connection:
            print(f"Connection {key} not found in get_connection()")
            return None

        return connection

    @classmethod
    def remove_connection(cls, connection_id: Union[UUID, str]):
        key = str(connection_id)
        cls._active_connections.pop(key, None)
        print(f'Connection: {key} was removed.')