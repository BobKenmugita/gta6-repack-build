"""Aggregated plan handed from the manifest resolver to the pipeline."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from src.repack_models.manifest_entry import ManifestEntry


@dataclass(slots=True)
class RepackPlan:
    entries: list[ManifestEntry] = field(default_factory=list)
    source: Path | None = None

    def total_bytes(self) -> int:
        return sum(e.size for e in self.entries)

    def by_kind(self, kind: str) -> list[ManifestEntry]:
        return [e for e in self.entries if e.kind == kind]

    def to_dict(self) -> dict:
        return {
            "source": str(self.source) if self.source else None,
            "entries": [e.to_dict() for e in self.entries],
            "total_bytes": self.total_bytes(),
        }