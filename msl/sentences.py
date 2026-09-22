"""Sentences that a template got wrong, and how many of them are in the ledger.

The ledger is append-only, so a claim whose *sentence* was malformed stays on the
record with the words it was published with.  The template is fixed and the next
cycle produces the same fact under a correct sentence — but the old rows do not go
away, and nothing in the pipeline would ever mention them again.

That is the same defect the irregularity register exists to prevent: an error that
is not written down is invisible.  So every sentence defect this project has found
is recorded here with the rule that produced it, the fix, and a pattern that
matches it, and the cycle publishes one aggregated finding per defect with a
*computed* count.  When the last matching row ages out of the register the finding
stops recurring and resolves itself; nothing here is hand-counted.

A defect is not a retraction.  ``msl/retractions.py`` withdraws claims about the
wrong subject; this module only reports rows whose sentence was written by a buggy
template, because the value in them is usually a correct reading of the right thing.
"""

from __future__ import annotations

import re
from typing import Any, Dict, List

#: Each entry matches a sentence the ledger should never have published.
#:
#: ``pattern`` uses ``re.search``.  Keep them narrow: a pattern that could match a
#: correct sentence turns a real finding into noise, which is how a register stops
#: being read.
DEFECTS: List[Dict[str, Any]] = [
    {
        "id": "SENT-DOUBLED-PHRASE",
        "pattern": re.compile(r"documents matching Documents matching"),
        "symptom": ("The Federal Register template interpolated the API's own "
                    "description — the phrase “Documents matching 'x'” — after the "
                    "word “matching”, so the sentence read “holds 1,573 documents "
                    "matching Documents matching 'artificial intelligence'”."),
        "fix": ("msl/adapters.federal_register builds the sentence from the term the "
                "project asked for and records the API's own phrasing in the row's "
                "tags instead of splicing it into a sentence it was not written for."),
    },
    {
        "id": "SENT-PLACEHOLDER-ARGUMENT",
        "pattern": re.compile(r"(series \?|the configured (window|query|area))"),
        "symptom": ("A template interpolated a parameter that comes from the task "
                    "context, so a read whose context lacked it published a literal "
                    "placeholder: “BLS reports series ? at 334.98”, “USGS counts 40 "
                    "earthquakes the configured window”, “for the configured query”."),
        "fix": ("the adapters now take the identifier from the payload the read "
                "returned (seriesID, indicator.id, the article name, the URL's own "
                "query parameters) and refuse to record a figure they cannot name. "
                "A field whose name is a placeholder is also withdrawn from reasoning "
                "— see msl/retractions.py."),
    },
    {
        "id": "SENT-EMPTY-SUBJECT",
        "pattern": re.compile(r"repositories matching \.\s*$|place result\(s\) for the query\."),
        "symptom": ("The subject of the sentence was missing entirely, leaving "
                    "“GitHub Search reports 3,667,127 repositories matching .” and "
                    "“Nominatim returns 1 place result(s) for the query.”"),
        "fix": ("every read now carries the identifying parameters of its own URL "
                "into its adapter context (msl/pipeline.url_context), and an adapter "
                "that cannot attribute its figure records a shape problem instead of "
                "publishing it."),
    },
]


def find_defects(claims: List[Any]) -> Dict[str, List[str]]:
    """Defect id → the claim ids whose published sentence matches it."""
    out: Dict[str, List[str]] = {}
    for c in claims:
        text = getattr(c, "statement", "") or ""
        if not text:
            continue
        for d in DEFECTS:
            if d["pattern"].search(text):
                out.setdefault(d["id"], []).append(getattr(c, "id", ""))
    return out
