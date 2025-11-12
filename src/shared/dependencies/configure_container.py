from src.shared.dependencies.container import Container

from src.shared.utils.logs.logger import Logger

def configure_container():
    """
    Configure non request scoped dependencies here
    """
    logger = Logger()
    Container.register("logger", logger)
   