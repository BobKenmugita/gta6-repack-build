"""Generate a repack.manifest.json from a folder of loose mod files."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("src", type=Path)
    ap.add_argument("--out", type=Path, default=Path("repack.manifest.json"))
    args = ap.parse_args()

    entries = []
    for f in sorted(args.src.rglob("*")):
        if not f.is_file():
            continue
        rel = f.relative_to(args.src).as_posix()
        entries.append({
            "src": rel,
            "dst": rel,
            "kind": "rpf" if f.suffix == ".rpf" else "file",
            "size": f.stat().st_size,
            "sha256": sha256(f),
        })

    args.out.write_text(json.dumps({"entries": entries}, indent=2), encoding="utf-8")
    print(f"wrote {len(entries)} entries -> {args.out}")


if __name__ == "__main__":
    main()