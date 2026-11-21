from pathlib import Path

from src.platform.win_fs_adapter import WinFsAdapter
from src.repack_services.manifest_resolver import ManifestResolver


def test_resolve_simple_manifest(tmp_path: Path) -> None:
    manifest = tmp_path / "repack.manifest.json"
    manifest.write_text(
        '{"entries":[{"src":"a.bin","dst":"a.bin","kind":"file","size":4}]}'
    )
    resolver = ManifestResolver(WinFsAdapter(tmp_path))
    result = resolver.handle("resolve", {"manifest": str(manifest)})
    assert result["ok"] is True
    assert result["count"] == 1
    assert result["plan"]["total_bytes"] == 4


def test_resolve_missing_manifest_reports_error(tmp_path: Path) -> None:
    resolver = ManifestResolver(WinFsAdapter(tmp_path))
    result = resolver.handle("resolve", {"manifest": str(tmp_path / "nope.json")})
    assert result["ok"] is False