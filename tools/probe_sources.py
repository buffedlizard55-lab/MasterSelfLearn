#!/usr/bin/env python3
"""Read-only source probe.  Live-reads every registered source and publishes the
health ledger to ``data/source_health.json``.

This never writes the claim ledger.  It is the only thing allowed to move a
source's ``status`` between ``registered``, ``verified-live-read`` and
``blocked`` — a status is a fact about the last read, not an editorial opinion.

The loop itself lives in ``msl.probe``; this file is a thin wrapper so the CLI
and this tool cannot drift into two different probes.  That already happened
once: both copies called ``fetch(..., accepts=...)`` against a signature that
takes ``accept=``, both raised ``TypeError``, and the probe had never run.

    python3 tools/probe_sources.py                  # everything
    python3 tools/probe_sources.py arxiv nws_alerts # a subset
"""
from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from msl.probe import exit_code, probe_registry, summary_line, write_report  # noqa: E402


def main(argv):
    only = set(argv[1:]) or None
    rep = probe_registry(only=only)
    out = write_report(rep)
    print(f"\n{summary_line(rep)} → {out}")
    return exit_code(rep)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
