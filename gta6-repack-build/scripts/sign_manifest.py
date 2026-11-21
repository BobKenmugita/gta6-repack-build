"""Attach an ed25519 signature to a repack manifest for release builds."""
from __future__ import annotations

import argparse
import base64
import json
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey


def load_key(path: Path) -> Ed25519PrivateKey:
    return Ed25519PrivateKey.from_private_bytes(path.read_bytes())


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("manifest", type=Path)
    ap.add_argument("--key", type=Path, required=True)
    args = ap.parse_args()

    data = args.manifest.read_bytes()
    sig = load_key(args.key).sign(data)
    out = args.manifest.with_suffix(".sig.json")
    out.write_text(
        json.dumps({"alg": "ed25519", "sig": base64.b64encode(sig).decode()}),
        encoding="utf-8",
    )
    print(f"signed -> {out}")


if __name__ == "__main__":
    main()