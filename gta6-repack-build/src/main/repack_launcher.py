"""Entry point for the GTA6 Repack desktop launcher shell.

Spawns the Qt UI thread and wires the repack service bus to the platform
adapters (filesystem, archive, RPF tooling).
"""
from __future__ import annotations

import logging
import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from src.main.repack_bus import RepackBus
from src.main.platform.win_fs_adapter import WinFsAdapter
from src.main.platform.rpf_adapter import RpfAdapter
from src.repack_services.install_pipeline import InstallPipeline
from src.repack_services.manifest_resolver import ManifestResolver
from src.repack_services.verify_engine import VerifyEngine

log = logging.getLogger("gta6repack.launcher")


def build_bus(root: Path) -> RepackBus:
    fs = WinFsAdapter(root)
    rpf = RpfAdapter(fs)
    bus = RepackBus()
    bus.register("manifest", ManifestResolver(fs))
    bus.register("install", InstallPipeline(fs, rpf))
    bus.register("verify", VerifyEngine(fs))
    return bus


def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    log.info("launcher root=%s", root)

    app = QApplication(sys.argv[:1])
    from src.renderer.window import RepackWindow

    bus = build_bus(root)
    win = RepackWindow(bus)
    win.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())