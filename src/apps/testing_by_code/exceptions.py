class CodeExecutionError(Exception):
    """Выполняемый код написан с ошибкой"""

    def __init__(self, message: str | None = None) -> None:
        if message:
            super().__init__(message)
        else:
            super().__init__()
