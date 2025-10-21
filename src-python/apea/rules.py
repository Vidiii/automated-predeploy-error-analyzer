import re
from typing import Optional, Tuple

# each rule returns (class, reason, fix) on match; else None
_RULES = [
    (
        re.compile(r"authentication failed|invalid credentials", re.I),
        ("Authentication/Authorization",
         "Authentication failed while connecting to target",
         "Verify username/password or token; check vault/secret and account lockout."),
    ),
    (
        re.compile(r"(tls handshake failed|ssl:.*handshake|certificate verify failed)", re.I),
        ("Network/Connectivity",
         "TLS/SSL handshake failed",
         "Ensure correct CA certs and system time; set verify settings or update certificates."),
    ),
    (
        re.compile(r"(unable to connect|connection refused|timed out|timeout occurred)", re.I),
        ("Network/Connectivity",
         "Network connection issue",
         "Check host/port, firewall, proxy, and DNS reachability."),
    ),
    (
        re.compile(r"(variable .* not defined|undefined variable|is not set)", re.I),
        ("Configuration/Variable Missing",
         "Required variable missing",
         "Define the variable in inventory, extra_vars, or pipeline secrets."),
    ),
    (
        re.compile(r"(command .* not found|returned 127)", re.I),
        ("Dependency/Package Not Found",
         "Command missing on runner",
         "Install dependency on agent/runner and validate PATH."),
    ),
]

def apply_rules(text: str) -> Optional[Tuple[str, str, str]]:
    for pattern, payload in _RULES:
        if pattern.search(text):
            return payload
    return None
