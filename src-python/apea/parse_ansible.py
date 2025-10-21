import re
from datetime import datetime
from typing import Iterable

from .types import NormalizedLogEvent
from .rules import apply_rules

# matches: [YYYY-MM-DD HH:MM:SS] LEVEL message
_LINE = re.compile(
    r"^\[(?P<ts>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\]\s+(?P<level>DEBUG|INFO|WARN|ERROR)\s+(?P<msg>.+)$",
    re.ASCII,
)

def _iso(ts: str) -> str:
    # assume given timestamp is local/timezone-agnostic; store as ISO without TZ
    try:
        return datetime.strptime(ts, "%Y-%m-%d %H:%M:%S").isoformat()
    except ValueError:
        # fallback: current time; we keep parser resilient
        return datetime.utcnow().isoformat() + "Z"

def parse_text(text: str, job_id: str = "local") -> Iterable[NormalizedLogEvent]:
    for raw in text.splitlines():
        raw_stripped = raw.rstrip("\n")
        m = _LINE.match(raw_stripped)
        if not m:
            # emit generic INFO line so we keep context even if not parsed
            yield NormalizedLogEvent(
                timestamp=datetime.utcnow().isoformat() + "Z",
                tool="ansible_tower",
                job_id=job_id,
                level="INFO",
                message=raw_stripped,
                raw=raw_stripped,
            )
            continue

        ts = _iso(m.group("ts"))
        level = m.group("level")
        msg = m.group("msg")

        detected_class = detected_reason = suggested_fix = None
        hit = apply_rules(msg)
        if hit:
            detected_class, detected_reason, suggested_fix = hit

        yield NormalizedLogEvent(
            timestamp=ts,
            tool="ansible_tower",
            job_id=job_id,
            level=level,
            message=msg.strip(),
            raw=raw_stripped,
            detected_class=detected_class,
            detected_reason=detected_reason,
            suggested_fix=suggested_fix,
            meta={},
        )
