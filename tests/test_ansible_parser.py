from pathlib import Path
import sys

# allow importing from src-python without installing
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src-python"))

from apea.parse_ansible import parse_text  # type: ignore

def test_parses_basic_lines(tmp_path: Path):
    content = (
        "[2025-10-21 10:22:03] ERROR Unable to connect to <HOST_A>:443 (TLS handshake failed)\n"
        "[2025-10-21 10:22:04] WARN Retrying in 5 seconds\n"
        "[2025-10-21 10:22:09] ERROR Authentication failed for user <USER_A>\n"
    )
    p = tmp_path / "log.log"
    p.write_text(content, encoding="utf-8")

    events = list(parse_text(p.read_text()))
    assert len(events) == 3

    # first line should be ERROR and detect TLS/network
    e0 = events[0]
    assert e0.level == "ERROR"
    assert e0.detected_class in {"Network/Connectivity", "Authentication/Authorization"}
    assert "handshake" in (e0.detected_reason or "").lower()

    # second line should be WARN with no detection
    e1 = events[1]
    assert e1.level == "WARN"
    assert e1.detected_class is None

    # third line should be auth failure
    e2 = events[2]
    assert e2.level == "ERROR"
    assert e2.detected_class == "Authentication/Authorization"
