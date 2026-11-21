"""Local IPC channel — a tiny JSON-lines socket used by the preload bridge."""
from __future__ import annotations

import json
import socket
import threading
from typing import Any

from src.main.repack_bus import RepackBus

HOST = "127.0.0.1"
PORT = 27845


class RepackChannel:
    def __init__(self, bus: RepackBus) -> None:
        self.bus = bus
        self._srv: socket.socket | None = None

    def start(self) -> None:
        srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((HOST, PORT))
        srv.listen(4)
        self._srv = srv
        threading.Thread(target=self._accept_loop, daemon=True).start()

    def stop(self) -> None:
        if self._srv:
            self._srv.close()
            self._srv = None

    def _accept_loop(self) -> None:
        assert self._srv is not None
        while True:
            try:
                conn, _ = self._srv.accept()
            except OSError:
                return
            threading.Thread(target=self._serve, args=(conn,), daemon=True).start()

    def _serve(self, conn: socket.socket) -> None:
        with conn, conn.makefile("rwb") as fh:
            for line in fh:
                try:
                    req: dict[str, Any] = json.loads(line)
                    resp = self.bus.dispatch(
                        req.get("service", ""),
                        req.get("action", ""),
                        req.get("payload", {}),
                    )
                except Exception as exc:  # noqa: BLE001
                    resp = {"ok": False, "error": str(exc)}
                fh.write((json.dumps(resp) + "\n").encode())
                fh.flush()