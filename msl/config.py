"""Static configuration.  No secrets, no keys, no manual input anywhere."""
from __future__ import annotations

import os
import pathlib

REPO_OWNER = "buffedlizard55-lab"
REPO_NAME = "MasterSelfLearn"
SITE_URL = f"https://{REPO_OWNER}.github.io/{REPO_NAME}/"
REPO_URL = f"https://github.com/{REPO_OWNER}/{REPO_NAME}"
MASTER_SITE_URL = f"https://{REPO_OWNER}.github.io/MasterSite/"
OWNER_TIMEZONE = "America/Los_Angeles"

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SEED = DATA / "seed"

# --- identity sent on every outbound request (required by several operators) ---
USER_AGENT = (
    "MasterSelfLearn/0.1 (autonomous research engine; "
    "https://github.com/buffedlizard55-lab/MasterSelfLearn; "
    "contact buffedlizard55@gmail.com)"
)
CONTACT_EMAIL = "buffedlizard55@gmail.com"

# --- cadence ---------------------------------------------------------------
# .github/workflows/think.yml runs on this cron.  Kept here so the site can show
# the *next* run time without hardcoding it in JavaScript.
CYCLE_CRON = "*/30 * * * *"
CYCLE_INTERVAL_MINUTES = 30

# --- network ---------------------------------------------------------------
HTTP_TIMEOUT = int(os.environ.get("MSL_HTTP_TIMEOUT", "15"))
HTTP_RETRIES = int(os.environ.get("MSL_HTTP_RETRIES", "2"))
HTTP_BACKOFF_SECONDS = 2.0
MAX_RESPONSE_BYTES = 8 * 1024 * 1024
# Keep one half-hour scheduled cycle bounded even when many hosts black-hole
# connections. Deferred tasks are counted and flagged rather than letting the
# workflow be killed mid-write by its job timeout.
CYCLE_COLLECTION_BUDGET_SECONDS = int(
    os.environ.get("MSL_COLLECTION_BUDGET_SECONDS", "480"))
# Operator-specific host pacing. This is applied centrally before *every* HTTP
# attempt so probes, surveys, and retries cannot accidentally bypass it.
HOST_MIN_INTERVAL_SECONDS = {
    "export.arxiv.org": 3.0,            # arXiv API terms ask for a 3 s delay
    "nominatim.openstreetmap.org": 1.0, # public Nominatim policy: max 1 req/s
    "eutils.ncbi.nlm.nih.gov": 0.34,    # keyless NCBI ceiling: 3 req/s
}

# --- growth limits (keeps the library honest rather than merely large) -------
MAX_NEW_TOPICS_PER_CYCLE = 6          # expansion is deliberate, not greedy
MAX_TOPICS_TRACKED = 240              # oldest retired topics are pruned
MIN_SIGNALS_TO_PROPOSE_TOPIC = 2      # one signal is noise
CYCLES_BEFORE_RETIREMENT = 96         # ~2 days at 30 min with no signal
MIN_SCORED_FORECASTS_TO_RANK = 3      # below this a strategy is UNRANKED, not "0%"

# --- anti-hallucination thresholds ----------------------------------------
DERIVED_RECHECK_TOLERANCE = 1e-9      # arithmetic must reproduce exactly
SOURCE_FAILS_BEFORE_CRITICAL = 3      # consecutive probe failures -> critical


def runtime_mode() -> str:
    """Where this cycle is executing.  Recorded in every cycle log line."""
    if os.environ.get("GITHUB_ACTIONS") == "true":
        return "github-actions"
    if os.environ.get("MSL_OFFLINE") == "1":
        return "offline-fixtures"
    return "local"
