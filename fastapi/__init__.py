"""Minimal stub of FastAPI for testing without external dependencies.
Provides only the features used in this project: FastAPI class with get/post decorators
and route registration. The app instance is callable but not used directly by the
httpx stub.
"""
import inspect
from typing import Callable, Any, Dict, Tuple

class FastAPI:
    """Very small subset of FastAPI functionality.
    Registers route handlers and stores them in a dict for lookup by the httpx
    AsyncClient stub.
    """
    def __init__(self, title: str = "") -> None:
        self.title = title
        # key: (method, path) -> handler function
        self.routes: Dict[Tuple[str, str], Callable[..., Any]] = {}

    def get(self, path: str):
        def decorator(func: Callable[..., Any]):
            self.routes[("GET", path)] = func
            return func
        return decorator

    def post(self, path: str, status_code: int = 200, response_model: Any = None):
        def decorator(func: Callable[..., Any]):
            self.routes[("POST", path)] = func
            return func
        return decorator

    # The ASGI callable interface is not required for the current tests.
    async def __call__(self, scope, receive, send):  # pragma: no cover
        raise NotImplementedError("ASGI interface not implemented in stub.")
