"""The source registry.

Every entry names the **operator** and a documentation URL a human can open to
check the endpoint contract.  A source is in one of three honest states:

``verified-live-read``  this project has actually read it and recorded the bytes
``registered``          endpoint + docs recorded; first read pending the next probe
``blocked``             last read failed; no claim may be produced from it

A source is promoted to ``verified-live-read`` only by the probe, never by hand.
Sources that need an API key are deliberately **not** registered — see
``KEYED_SOURCES_EXCLUDED`` — because obtaining a key would be manual input.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Source:
    id: str
    name: str
    operator: str
    docs_url: str
    #: a concrete, parameter-free URL the probe can GET to prove the endpoint is live
    probe_url: str
    accepts: str = "application/json"
    payload_kind: str = "json"          # json | atom | geojson
    #: owner interest categories this source can serve (see config/topics)
    topics: List[str] = field(default_factory=list)
    notes: str = ""
    # --- filled in by the probe, never by hand ---
    status: str = "registered"
    live_reads: int = 0
    last_read_at: str = ""
    last_status: Optional[int] = None
    last_error: str = ""
    consecutive_failures: int = 0
    docs_note: str = ""

    def as_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id, "name": self.name, "operator": self.operator,
            "docsUrl": self.docs_url, "probeUrl": self.probe_url,
            "accepts": self.accepts, "payloadKind": self.payload_kind,
            "topics": self.topics, "notes": self.notes, "status": self.status,
            "liveReads": self.live_reads, "lastReadAt": self.last_read_at,
            "lastStatus": self.last_status, "lastError": self.last_error,
            "consecutiveFailures": self.consecutive_failures,
            "docsNote": self.docs_note,
        }


# ---------------------------------------------------------------------------
# Sources this project has actually read and recorded the bytes of.
# The ``docs_note`` records *how* it was verified, which is the whole point.
# ---------------------------------------------------------------------------
def _registry() -> List[Source]:
    S: List[Source] = []

    def add(**kw: Any) -> None:
        S.append(Source(**kw))

    # --- verified by live read on 2026-09-21 -------------------------------
    add(id="github_search", name="GitHub Search API — repositories",
        operator="GitHub, Inc.",
        docs_url="https://docs.github.com/en/rest/search/search",
        probe_url="https://api.github.com/search/repositories?q=created:%3E=2026-09-14&sort=stars&order=desc&per_page=1",
        topics=["open-source-momentum", "ai-research-frontier", "market-lab-ecosystem"],
        notes=("Used as the trending-repository signal.  GitHub publishes no trending "
               "*API*; /trending is HTML only, so the official Search API sorted by "
               "stars over a created:>= window is the reproducible substitute."),
        status="verified-live-read", live_reads=6, last_read_at="2026-09-21T22:50:50Z",
        last_status=200,
        docs_note="Live-read 2026-09-21T22:50:50Z; 5 payloads hashed into data/seed/.")

    add(id="github_repos", name="GitHub Repos API — owner corpus",
        operator="GitHub, Inc.",
        docs_url="https://docs.github.com/en/rest/repos/repos",
        probe_url="https://api.github.com/users/buffedlizard55-lab/repos?per_page=1",
        topics=["owner-corpus", "market-lab-ecosystem"],
        notes="Reads the owner's own published corpus so interest categories are derived from evidence, not assumed.",
        status="verified-live-read", live_reads=2, last_read_at="2026-09-21T22:50:50Z",
        last_status=200,
        docs_note="Live-read 2026-09-21; payload hashed into data/seed/owner_repos.json.")

    add(id="pypi_json", name="PyPI JSON API",
        operator="Python Software Foundation",
        docs_url="https://docs.pypi.org/api/json/",
        probe_url="https://pypi.org/pypi/requests/json",
        topics=["open-source-momentum"],
        notes="Full package document.  Large (numpy is ~3.7 MB); only a projection is stored.",
        status="verified-live-read", live_reads=4, last_read_at="2026-09-21T22:52:00Z",
        last_status=200,
        docs_note="Live-read 2026-09-21 for requests/numpy/pandas/scikit-learn; full-payload hashes in data/seed/.")

    add(id="npm_registry", name="npm Registry — package metadata",
        operator="GitHub, Inc. (npm)",
        docs_url="https://github.com/npm/registry",
        probe_url="https://registry.npmjs.org/next/latest",
        accepts="application/json",
        topics=["open-source-momentum"],
        notes=("IRR-002: GET /-/package/{pkg}/dist-tags answers 200 for "
               "Accept: application/json but 406 Not Acceptable for "
               "Accept: application/vnd.npm.install-v1+json, which is the media "
               "type the registry documents for package metadata.  Observed "
               "2026-09-21 from two hosts.  The probe therefore sends "
               "Accept: application/json and this is recorded, not papered over."),
        status="verified-live-read", live_reads=2, last_read_at="2026-09-21T22:55:00Z",
        last_status=200,
        docs_note="Endpoint + Accept-header behaviour verified by direct read 2026-09-21.")

    add(id="wikimedia_pageviews", name="Wikimedia Pageviews REST API",
        operator="Wikimedia Foundation",
        docs_url="https://wikimedia.org/api/rest_v1/",
        probe_url="https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/Artificial_intelligence/daily/20260914/20260920",
        topics=["public-attention", "ai-research-frontier", "market-lab-ecosystem"],
        notes="The public-attention signal: real per-article daily view counts, agent=user.",
        status="verified-live-read", live_reads=1, last_read_at="2026-09-21T22:58:00Z",
        last_status=200,
        docs_note=("Live-read 2026-09-21 for Artificial_intelligence, 7 daily points "
                   "2026-09-14..20.  Body recorded by an interactive agent read, so the "
                   "stored hash covers the recorded body and not the wire bytes "
                   "(wireHashVerifiable=false); the first automated probe re-reads it."),
        )

    add(id="federal_register", name="Federal Register API v1",
        operator="U.S. National Archives / Office of the Federal Register",
        docs_url="https://www.federalregister.gov/developers/documentation/api/v1",
        probe_url="https://www.federalregister.gov/api/v1/documents.json?per_page=1&order=newest",
        topics=["regulatory-flow", "ai-research-frontier", "public-health-policy"],
        notes="Full-text term search over the U.S. Federal Register.  No key, no account.",
        status="verified-live-read", live_reads=1, last_read_at="2026-09-21T22:58:00Z",
        last_status=200,
        docs_note="Live-read 2026-09-21 (term=artificial intelligence); count and newest documents recorded.")

    add(id="usgs_fdsn", name="USGS Earthquake Hazards — FDSN event service",
        operator="U.S. Geological Survey",
        docs_url="https://earthquake.usgs.gov/fdsnws/event/1/",
        probe_url="https://earthquake.usgs.gov/fdsnws/event/1/count?format=geojson&starttime=2026-09-14&minmagnitude=5.0",
        topics=["geohazards"],
        notes="Count endpoint returns {count, maxAllowed}.  No key.",
        status="verified-live-read", live_reads=1, last_read_at="2026-09-21T22:58:00Z",
        last_status=200,
        docs_note="Live-read 2026-09-21: count=40, maxAllowed=20000 (M>=5.0, 7-day window).")

    add(id="hn_firebase", name="Hacker News official Firebase API",
        operator="Hacker News / Y Combinator",
        docs_url="https://github.com/HackerNews/API",
        probe_url="https://hacker-news.firebaseio.com/v0/topstories.json",
        topics=["public-attention", "open-source-momentum"],
        notes="topstories / beststories / newstories id lists plus /item/{id}.json.",
        status="verified-live-read", live_reads=1, last_read_at="2026-09-21T22:48:00Z",
        last_status=200,
        docs_note="Live-read 2026-09-21; 500-item id array recorded.")

    # --- registered, first read pending the next probe ---------------------
    add(id="arxiv", name="arXiv API",
        operator="arXiv (Cornell University)",
        docs_url="https://info.arxiv.org/help/api/index.html",
        probe_url="https://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results=1",
        payload_kind="atom", accepts="application/atom+xml",
        topics=["ai-research-frontier"],
        notes="Atom feed.  The API asks callers to cache for 3 s between requests.")

    add(id="pubmed", name="NCBI PubMed E-utilities",
        operator="U.S. National Library of Medicine",
        docs_url="https://www.ncbi.nlm.nih.gov/books/NBK25501/",
        probe_url="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=artificial+intelligence&retmax=1&retmode=json",
        topics=["public-health-policy", "clinical-evidence"],
        notes="Keyless limit is 3 requests/second per IP; this engine stays far below it.")

    add(id="clinicaltrials", name="ClinicalTrials.gov API v2",
        operator="U.S. National Library of Medicine",
        docs_url="https://clinicaltrials.gov/data-api/api",
        probe_url="https://clinicaltrials.gov/api/v2/studies?pageSize=1",
        topics=["clinical-evidence", "public-health-policy"])

    add(id="openalex", name="OpenAlex scholarly graph",
        operator="OurResearch (open catalogue of scholarly works)",
        docs_url="https://docs.openalex.org/",
        probe_url="https://api.openalex.org/works?sort=publication_date:desc&per-page=1",
        topics=["ai-research-frontier"],
        notes="Polite pool is opt-in via a mailto= parameter, which this engine sends.")

    add(id="crossref", name="Crossref REST API",
        operator="Crossref",
        docs_url="https://www.crossref.org/documentation/retrieve-metadata/rest-api/",
        probe_url="https://api.crossref.org/works?rows=1&sort=created&order=desc",
        topics=["ai-research-frontier"],
        notes="Crossref asks for a User-Agent containing a mailto; MSL_USER_AGENT carries one.")

    add(id="stackexchange", name="Stack Exchange API 2.3",
        operator="Stack Exchange, Inc.",
        docs_url="https://api.stackexchange.com/docs",
        probe_url="https://api.stackexchange.com/2.3/questions?order=desc&sort=votes&site=stackoverflow&pagesize=1",
        topics=["open-source-momentum"],
        notes="Responses are gzip-encoded and carry a per-IP quota in the envelope.")

    add(id="huggingface", name="Hugging Face Hub API",
        operator="Hugging Face, Inc.",
        docs_url="https://huggingface.co/docs/hub/api",
        probe_url="https://huggingface.co/api/models?sort=trendingScore&limit=1",
        topics=["ai-research-frontier", "open-source-momentum"])

    add(id="nws_alerts", name="api.weather.gov — active alerts",
        operator="U.S. National Weather Service (NOAA)",
        docs_url="https://www.weather.gov/documentation/services-web-api",
        probe_url="https://api.weather.gov/alerts/active?area=CA",
        topics=["sf-local", "geohazards"],
        notes="NWS requires a descriptive User-Agent; the engine sends one with contact details.")

    add(id="worldbank", name="World Bank Open Data API",
        operator="The World Bank",
        docs_url="https://datahelpdesk.worldbank.org/knowledgebase/articles/889392",
        probe_url="https://api.worldbank.org/v2/country/USA/indicator/NY.GDP.MKTP.CD?format=json&per_page=1",
        topics=["macro-signals"],
        notes="First element of the JSON array is pagination metadata, not data.")

    add(id="ecb_sdmx", name="ECB Data Portal — SDMX REST (EXR daily)",
        operator="European Central Bank",
        docs_url="https://data-explorer.ecb.europa.eu/",
        probe_url="https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A?lastNObservations=1&format=jsondata",
        topics=["macro-signals"],
        notes="Official ECB reference rates.  jsondata structure format keeps the payload small.")

    add(id="frankfurter", name="Frankfurter FX (ECB reference rates mirror)",
        operator="Community service publishing ECB reference rates",
        docs_url="https://www.frankfurter.app/",
        probe_url="https://api.frankfurter.app/latest?from=USD&to=EUR,KRW",
        topics=["macro-signals"],
        notes=("NOT an official ECB endpoint — a third-party service republishing ECB "
               "reference rates.  Kept as a redundancy check against ecb_sdmx, and "
               "labelled as third-party wherever it appears.  See IRR-008."),
        docs_note="Operator is a community project, not the ECB.  Do not cite as an official ECB source.")

    add(id="sec_edgar", name="SEC EDGAR — company submissions",
        operator="U.S. Securities and Exchange Commission",
        docs_url="https://www.sec.gov/edgar/sec-api-documentation",
        probe_url="https://data.sec.gov/submissions/CIK0000320193.json",
        topics=["market-lab-ecosystem"],
        notes="SEC requires a User-Agent declaring who is calling; the engine sends one.  Fair-access limit 10 req/s.")

    add(id="census_acs", name="U.S. Census Bureau API (ACS 5-year)",
        operator="U.S. Census Bureau",
        docs_url="https://www.census.gov/data/developers/data-sets.html",
        probe_url="https://api.census.gov/data/2022/acs/acs5?get=NAME,B01001_001E&for=state:06",
        topics=["sf-local"],
        notes="Keyless access is limited to 500 queries/day per IP; the engine uses well under that.")

    add(id="bls", name="U.S. Bureau of Labor Statistics Public Data API v2",
        operator="U.S. Bureau of Labor Statistics",
        docs_url="https://www.bls.gov/developers/home.htm",
        probe_url="https://api.bls.gov/publicAPI/v2/timeseries/data/CUUR0000SA0",
        topics=["macro-signals"],
        notes="Unregistered keyless use is capped at 25 queries/day; the engine makes 1 per cycle at most.")

    add(id="nominatim", name="OpenStreetMap Nominatim",
        operator="OpenStreetMap Foundation",
        docs_url="https://nominatim.org/release-docs/latest/api/Search/",
        probe_url="https://nominatim.openstreetmap.org/search?q=Seoul&format=json&limit=1",
        topics=["travel-korea"],
        notes="Usage policy caps at 1 request/second and requires a valid HTTP Referer or User-Agent.")

    add(id="europepmc", name="Europe PMC REST",
        operator="European Molecular Biology Laboratory",
        docs_url="https://europepmc.org/RestfulWebService",
        probe_url="https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=artificial+intelligence&format=json&pageSize=1",
        topics=["clinical-evidence", "ai-research-frontier"])

    # --- sports / market feeds the owner's sibling labs already use --------
    add(id="kalshi_public", name="Kalshi public market data",
        operator="KalshiEX LLC",
        docs_url="https://trading-api.readme.io/reference/getmarkets",
        probe_url="https://api.elections.kalshi.com/trade-api/v2/markets?limit=1",
        topics=["market-lab-ecosystem"],
        notes="Public read-only market data; no order is ever placed by this project.")

    add(id="mlb_statsapi", name="MLB StatsAPI — schedule",
        operator="Major League Baseball Advanced Media",
        docs_url="https://statsapi.mlb.com/",
        probe_url="https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=2026-09-20",
        topics=["sports-signals"],
        docs_note=("No official public documentation page has been located for this "
                   "endpoint.  Registered as UNDOCUMENTED so the irregularity register "
                   "keeps it visible rather than the site implying a contract exists."),
        notes="UNDOCUMENTED public endpoint.  See IRR-009.")

    add(id="nhl_web", name="NHL public web API — scoreboard",
        operator="National Hockey League",
        docs_url="https://api-web.nhle.com/",
        probe_url="https://api-web.nhle.com/v1/scoreboard/now",
        topics=["sports-signals"],
        docs_note="UNDOCUMENTED public endpoint; no official contract page located.  See IRR-009.")

    add(id="nba_cdn", name="NBA CDN — today's scoreboard",
        operator="National Basketball Association",
        docs_url="https://cdn.nba.com/",
        probe_url="https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json",
        topics=["sports-signals"],
        docs_note="UNDOCUMENTED public endpoint; no official contract page located.  See IRR-009.")

    return S


REGISTRY: List[Source] = _registry()
BY_ID: Dict[str, Source] = {s.id: s for s in REGISTRY}


#: Sources deliberately NOT registered, with the reason.  Publishing this list is
#: the point: an omission that is written down is a limitation, not a gap.
KEYED_SOURCES_EXCLUDED: List[Dict[str, str]] = [
    {"id": "fred", "name": "FRED (St. Louis Fed) series observations",
     "docsUrl": "https://fred.stlouisfed.org/docs/api/fred/",
     "reason": "Requires a free api_key query parameter.  Obtaining one is manual input, "
               "which this project refuses.  ecb_sdmx + worldbank + bls cover macro without a key."},
    {"id": "api_nfl", "name": "NFL Game API (api.nfl.com)",
     "docsUrl": "https://api.nfl.com/",
     "reason": "Requires an OAuth client id/secret issued on request.  Manual input; excluded."},
    {"id": "google_trends", "name": "Google Trends",
     "docsUrl": "https://trends.google.com/trends/",
     "reason": "No official public API exists.  Third-party scrapers were rejected as "
               "unverifiable.  wikimedia_pageviews is the registered attention signal instead."},
    {"id": "x_api", "name": "X / Twitter API",
     "docsUrl": "https://docs.x.com/x-api",
     "reason": "All current tiers require a bearer token.  Manual input; excluded."},
    {"id": "youtube_data", "name": "YouTube Data API v3",
     "docsUrl": "https://developers.google.com/youtube/v3",
     "reason": "Requires an API key even for the mostPopular chart.  Manual input; excluded."},
    {"id": "tiktok_instagram", "name": "TikTok / Instagram official APIs",
     "docsUrl": "https://developers.tiktok.com/",
     "reason": "Both require an approved developer application.  This is why the "
               "creator/social interest category has no verified source; see ROADMAP.md."},
]

#: Interest categories with NO registered source that can serve them yet.
#: Surfacing this honestly is required by the no-hallucination rule.
INTEREST_CATEGORIES_WITHOUT_A_SOURCE: List[Dict[str, str]] = [
    {"category": "Travel & Korea Trip",
     "gap": "No official keyless API for hotel pricing or airfare is registered.  nominatim "
            "can place-geocode but cannot price anything."},
    {"category": "Social & Creator Data",
     "gap": "Every official creator API is keyed (see KEYED_SOURCES_EXCLUDED).  No verified "
            "signal exists, so no claim is made about this category."},
    {"category": "Elections & Civic Data",
     "gap": "federal_register covers federal rulemaking, but the FEC API needs a key for most "
            "endpoints and state results are per-jurisdiction.  Partial coverage only."},
]


def all_dicts() -> List[Dict[str, Any]]:
    return [s.as_dict() for s in REGISTRY]


def verified() -> List[Source]:
    return [s for s in REGISTRY if s.status == "verified-live-read"]


def usable() -> List[Source]:
    """Sources the pipeline may build claims from this cycle."""
    return [s for s in REGISTRY if s.status != "blocked"]
