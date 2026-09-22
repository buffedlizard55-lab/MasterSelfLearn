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
    # --- fields whose NAME is a placeholder ---------------------------------
    # These are a different failure from the two above: the value is a correct
    # reading of the right subject, but the field name and the published sentence
    # carry an unfilled parameter ("?" or an empty query) because the parameter came
    # from the task's context and the context did not have it.  A misplaced value is
    # fixed by re-reading; a misnamed one is fixed by never producing it again — the
    # adapters now take the identifier from the payload, and refuse to record a
    # figure they cannot attribute.  The old rows stay in the ledger and are
    # withdrawn from publication and from reasoning, because a series named after
    # nothing cannot be compared with anything.
    {
        "fieldPrefix": "bls[?].latest",
        "reason": (
            "The field name and the published sentence both contain an unfilled "
            "placeholder — “BLS reports series ? at 334.98 for August 2026”.  The "
            "value was a correct reading; the name was not a name.  msl/adapters.bls "
            "now takes the series id from the payload's own seriesID."
        ),
        "supersededBy": "bls[CUUR0000SA0].latest",
        "firstSeenCycle": "5",
        "fixedInCycle": "15",
        "irregularity": "IRR-PLACEHOLDER-FIELD",
    },
    {
        "fieldPrefix": "worldbank[?].latest",
        "reason": (
            "Same defect: the indicator id came from the task context, so a read "
            "without it published the field ``worldbank[?].latest``.  "
            "msl/adapters.worldbank now takes indicator.id from the payload and "
            "refuses the fact if nothing names the indicator."
        ),
        "supersededBy": "worldbank[NY.GDP.MKTP.CD].latest",
        "firstSeenCycle": "5",
        "fixedInCycle": "15",
        "irregularity": "IRR-PLACEHOLDER-FIELD",
    },
    {
        "fieldPrefix": "nominatim.results[?]",
        "reason": (
            "Same defect: the place name came from the task context, so the answer "
            "was published as “Nominatim returns 1 place result(s) for the query.” "
            "under a placeholder name.  The place is the entire content of the "
            "answer, so msl/adapters.nominatim now refuses a read it cannot "
            "attribute to a place."
        ),
        "supersededBy": "nominatim.results[Seoul]",
        "firstSeenCycle": "5",
        "fixedInCycle": "15",
        "irregularity": "IRR-PLACEHOLDER-FIELD",
    },
    {
        "fieldPrefix": "github.total_count[]",
        "reason": (
            "Same defect, and the worst of them: every GitHub search whose context "
            "did not carry the query collapsed into ONE field, so unrelated searches "
            "shared a series and the site published “GitHub Search reports 3,667,127 "
            "repositories matching .”  msl/adapters.gh_search now writes the query it "
            "was given and refuses a total it cannot attribute to one."
        ),
        "supersededBy": "github.total_count[<query>]",
        "firstSeenCycle": "11",
        "fixedInCycle": "15",
        "irregularity": "IRR-PLACEHOLDER-FIELD",
    },
]

def is_retracted(field: str) -> bool:
    """True when ``field`` names a claim withdrawn as being about the wrong subject.

    Read from ``RETRACTIONS`` on every call rather than from a list built once at
    import time.  A cached copy of a mutable public table is a trap: editing the
    table above would silently change nothing, and the claim that was supposed to be
    withdrawn would keep scoring forecasts.
    """
    if not field:
        return False
    return any(field.startswith(r["fieldPrefix"]) for r in RETRACTIONS)


def reason_for(field: str) -> Optional[str]:
    """The recorded reason a field was retracted, or None if it was not."""
    for r in RETRACTIONS:
        if field.startswith(r["fieldPrefix"]):
            return r["reason"]
    return None


def retracted_in(claims) -> List:
    """The retracted claims out of an iterable of Claim objects."""
    return [c for c in claims if is_retracted(getattr(c, "field", ""))]
