"""Claims that were verified but are about the wrong subject.

The evidence gate can prove a claim was read.  It cannot prove the URL asked for
the thing the reader will assume it asked for.  When that goes wrong the claim is
genuine, the arithmetic on it is genuine, and the conclusion is nevertheless
about something else — so it must be withdrawn from the reasoning and the site
without being erased from the ledger.

Rules this module exists to enforce:

* Nothing here deletes evidence.  ``data/claims.jsonl`` and ``data/evidence.jsonl``
  stay append-only; a retracted claim keeps its row, its hash and its id.
* A retraction is a standing irregularity.  It is raised every cycle, with the
  reason and the replacement, so a reader who lands on the old number can see
  why it is no longer being published.
* The prefix match is deliberate and narrow.  It names a field that cannot be
  produced by a correct read, not a pattern that might swallow good data.
"""
from __future__ import annotations

from typing import Dict, List, Optional

#: Each entry retracts every claim whose ``field`` starts with ``fieldPrefix``.
RETRACTIONS: List[Dict[str, str]] = [
    {
        "fieldPrefix": "wiki[artificial_intelligence]",
        "reason": (
            "Read from a lowercased Wikipedia slug.  Wikipedia titles are "
            "case-sensitive past the first character, so this URL resolves to a "
            "different, near-empty page rather than the article that receives "
            "roughly 15,000-21,000 views a day."
        ),
        "supersededBy": "wiki[Artificial_intelligence]",
        "firstSeenCycle": "5",
        "fixedInCycle": "7",
        "irregularity": "IRR-WIKI-CASE",
    },
    {
        "fieldPrefix": "trend[wiki:artificial_intelligence]",
        "reason": (
            "Derived from retracted pageview claims for the lowercased slug, so "
            "the trend describes the wrong page.  Recomputed from the canonical "
            "title instead."
        ),
        "supersededBy": "trend[wiki:Artificial_intelligence]",
        "firstSeenCycle": "5",
        "fixedInCycle": "7",
        "irregularity": "IRR-WIKI-CASE",
    },
]

_PREFIXES = [r["fieldPrefix"] for r in RETRACTIONS]


def is_retracted(field: str) -> bool:
    """True when ``field`` names a claim withdrawn as being about the wrong subject."""
    if not field:
        return False
    return any(field.startswith(p) for p in _PREFIXES)


def reason_for(field: str) -> Optional[str]:
    """The recorded reason a field was retracted, or None if it was not."""
    for r in RETRACTIONS:
        if field.startswith(r["fieldPrefix"]):
            return r["reason"]
    return None


def retracted_in(claims) -> List:
    """The retracted claims out of an iterable of Claim objects."""
    return [c for c in claims if is_retracted(getattr(c, "field", ""))]
