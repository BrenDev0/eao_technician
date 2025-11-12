from typing import TypeVar, Dict, Any, cast

T = TypeVar('T')

class Container:
    _instances: Dict[str, Any] = {}

    @classmethod
    def register(cls, key: str, instance: Any) -> None:
        cls._instances[key] = instance

    @classmethod
    def resolve(cls, key: str) -> T:
        if key not in cls._instances:
            raise ValueError(f"Dependency '{key}' not found!")
        return cast(T, cls._instances[key])

    @classmethod
    def clear(cls) -> None:
        cls._instances.clear()