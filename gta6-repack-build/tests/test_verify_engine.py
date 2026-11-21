import hashlib
from pathlib import Path

from src.platform.win_fs_adapter import WinFsAdapter
from src.repack_services.verify_engine import VerifyEngine


def test_verify_engine_flags_mismatch(tmp_path: Path) -> None:
    (tmp_path / "data.bin").write_bytes(b"hello")
    good = hashlib.sha256(b"hello").hexdigest()
    (tmp_path / "repack.sha256.json").write_text('{"data.bin": "deadbeef"}')

    engine = VerifyEngine(WinFsAdapter(tmp_path))
    result = engine.handle("check", {"install_dir": str(tmp_path)})
    assert result["ok"] is False
    assert "data.bin" in result["mismatches"]
    assert good  # sanity: real digest is computable