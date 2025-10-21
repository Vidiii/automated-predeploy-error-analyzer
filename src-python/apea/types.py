from typing import Dict, Iterable, Optional
from dataclasses import dataclass, asdict

@dataclass
class NormalizedLogEvent:
    timestamp: str              # ISO 8601 string
    tool: str                   # "ansible_tower", etc.
    job_id: str
    level: str                  # DEBUG/INFO/WARN/ERROR
    message: str
    raw: str
    step: Optional[str] = None
    detected_class: Optional[str] = None
    detected_reason: Optional[str] = None
    suggested_fix: Optional[str] = None
    meta: Optional[Dict] = None

    def to_dict(self) -> Dict:
        d = asdict(self)
        # keep meta a dict even if None
        d["meta"] = d.get("meta") or {}
        return d
