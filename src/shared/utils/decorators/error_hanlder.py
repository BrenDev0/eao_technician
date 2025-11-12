# core/decorators/error_handling.py
from functools import wraps
import logging
from typing import Callable, Any
from src.shared.utils.logs.logger import Logger
from src.shared.dependencies.container import Container


def error_handler(module: str) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func) 
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger: Logger = Container.resolve("logger")
                logger.log(
                    message=f"Error in {func.__name__}",
                    level=logging.ERROR,
                    name=f"{module}.{func.__name__}",
                    exc_info=True
                )
                raise  
        return wrapper
    return decorator