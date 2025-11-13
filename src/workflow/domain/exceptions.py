class NoContextError(Exception):
    def __init__(self, detail: str = "No context found"):
        super().__init__(detail)

class NoNamespaceError(Exception):
    def __init__(self, detail: str = "No namespace found"):
        super().__init__(detail)