"""In-process service registry that routes IPC packets to repack services."""
from __future__ import annotations

from typing import Any, Callable, Dict, Protocol


class Service(Protocol):
    name: str

    def handle(self, action: str, payload: dict[str, Any]) -> dict[str, Any]: ...


class RepackBus:
    def __init__(self) -> None:
        self._services: Dict[str, Service] = {}
        self._listeners: list[Callable[[str, dict], None]] = []

    def register(self, key: str, svc: Service) -> None:
        self._services[key] = svc

    def subscribe(self, fn: Callable[[str, dict], None]) -> None:
        self._listeners.append(fn)

    def dispatch(self, key: str, action: str, payload: dict[str, Any]) -> dict[str, Any]:
        svc = self._services.get(key)
        if svc is None:
            return {"ok": False, "error": f"no service registered for '{key}'"}
        result = svc.handle(action, payload)
        for fn in self._listeners:
            fn(key, result)
        return result