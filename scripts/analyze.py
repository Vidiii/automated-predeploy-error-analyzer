#!/usr/bin/env python
import argparse
import json
from pathlib import Path

from pathlib import Path
import sys

# make relative imports work when running from repo root
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src-python"))

from apea.parse_ansible import parse_text  # noqa: E402

def main():
    ap = argparse.ArgumentParser(description="Analyze Ansible Tower log")
    ap.add_argument("file", type=Path, help="Path to log file")
    ap.add_argument("--job-id", default="local", help="Job ID to tag")
    ap.add_argument("--summary", action="store_true", help="Print a brief summary")
    args = ap.parse_args()

    text = args.file.read_text(encoding="utf-8", errors="replace")
    events = list(parse_text(text, job_id=args.job_id))

    # stream JSON lines to stdout
    for ev in events:
        print(json.dumps(ev.to_dict(), ensure_ascii=False))

    if args.summary:
        # small human summary
        classes = [e.detected_class for e in events if e.detected_class]
        by_class = {}
        for c in classes:
            by_class[c] = by_class.get(c, 0) + 1
        if by_class:
            print("\n=== Summary ===")
            for k, v in sorted(by_class.items(), key=lambda x: -x[1]):
                print(f"{k}: {v} hits")
        else:
            print("\n=== Summary ===\nNo failures detected by rules.")

if __name__ == "__main__":
    main()
