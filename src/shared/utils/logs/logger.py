import logging
from typing import Optional

class Logger:
    @staticmethod
    def log(
        message: str,
        level: int = logging.INFO,
        name: str = "app",
        exc_info: Optional[bool] = False
    ):
        logger = logging.getLogger(name)
        logger.setLevel(level)

        if not logger.handlers:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(level)
            formatter = logging.Formatter("[%(asctime)s] %(levelname)s in %(name)s: %(message)s")
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

        logger.log(level, message, exc_info=exc_info)