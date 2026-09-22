#!/usr/bin/env python3
"""Read-only source probe.  Live-reads every registered source and publishes the
health ledger to ``data/source_health.json``.

This never writes the claim ledger.  It is the only thing allowed to move a
source's ``status`` between ``registered``, ``verified-live-read`` and
``blocked`` — a status is a fact about the last read, not an editorial opinion.

    python3 tools/probe_sources.py            # everything
    python3 tools/probe_sources.py arxiv nws_alerts   # a subset
"""
from __future__ import annotations

import json
import sys
import time
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from msl import config                                     # noqa: E402
from msl.http import fetch                                  # noqa: E402
from msl.sources import REGISTRY                            # noqa: E402


def main(argv):
    only = set(argv[1:])
    rows = []
    ok = failed = 0
    for s in REGISTRY:
        if only and s.id not in only:
            continue
        r = fetch(s.probe_url, accepts=s.accepts, retries=1)
        at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        rows.append({
            "id": s.id, "name": s.name, "operator": s.operator,
            "docsUrl": s.docs_url, "probeUrl": s.probe_url,
            "httpStatus": r.status, "ok": r.ok, "bytes": r.size,
            "elapsedMs": r.elapsed_ms, "attempts": r.attempts,
            "error": "" if r.ok else r.describe_error(),
            "sha256": r.sha256[:16] if r.body else "",
            "checkedAt": at,
        })
        if r.ok:
            ok += 1
            s.status = "verified-live-read"
            s.live_reads += 1
            s.consecutive_failures = 0
            s.last_error = ""
        else:
            failed += 1
            s.status = "blocked"
            s.consecutive_failures += 1
            s.last_error = r.describe_error()
        s.last_read_at = at
        s.last_status = r.status
        flag = "OK " if r.ok else "ERR"
        print(f"{flag} {r.status or '---'} {r.elapsed_ms:>5}ms {r.size:>8}B  "
              f"{s.id:<22} {'' if r.ok else r.describe_error()}")

    payload = {
        "generatedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "mode": config.runtime_mode(),
        "ok": ok, "failed": failed, "results": rows,
        "note": ("A blocked source produces no claims and no substitute value. "
                 "A source whose every read fails with a TLS/SSL EOF on every host "
                 "is usually an egress policy, not a data problem — check that "
                 "before treating it as a finding."),
    }
    out = config.DATA / "source_health.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=1) + "\n", encoding="utf-8")
    print(f"\n{ok} ok / {failed} failed → {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
