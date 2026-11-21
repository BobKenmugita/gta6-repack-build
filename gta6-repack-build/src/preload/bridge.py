"""Preload bridge shim — mirrors the IPC contract for the renderer."""
from __future__ import annotations

import json
import socket
from typing import Any

from src.main.ipc.repack_channel import HOST, PORT


class RepackBridge:
    def __init__(self, host: str = HOST, port: int = PORT) -> None:
        self.host, self.port = host, port

    def call(self, service: str, action: str, payload: dict[str, Any]) -> dict[str, Any]:
        msg = {"service": service, "action": action, "payload": payload}
        with socket.create_connection((self.host, self.port), timeout=10) as sock:
            sock.sendall((json.dumps(msg) + "\n").encode())
            data = sock.makefile("rb").readline()
        return json.loads(data or b"{}")

    def verify_install(self, install_dir: str) -> dict[str, Any]:
        return self.call("verify", "check", {"install_dir": install_dir})

    def start_install(self, manifest_path: str) -> dict[str, Any]:
        return self.call("install", "run", {"manifest": manifest_path})