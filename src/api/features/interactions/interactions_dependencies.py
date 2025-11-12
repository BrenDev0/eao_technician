from src.api.features.interactions.interactions_controller import InteractionsController
from src.shared.dependencies.container import Container


def get_interactions_controller():
    return InteractionsController()