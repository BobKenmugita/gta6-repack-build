"""One record inside repack.manifest.json."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ManifestEntry:
    src: str
    dst: str
    kind: str = "file"  # "file" | "rpf" | "dlc"
    size: int = 0
    sha256: str = ""

    @classmethod
    def from_dict(cls, raw: dict) -> "ManifestEntry":
        return cls(
            src=raw["src"],
            dst=raw["dst"],
            kind=raw.get("kind", "file"),
            size=int(raw.get("size", 0)),
            sha256=raw.get("sha256", ""),
        )

    def to_dict(self) -> dict:
        return {
            "src": self.src,
            "dst": self.dst,
            "kind": self.kind,
            "size": self.size,
            "sha256": self.sha256,
        }