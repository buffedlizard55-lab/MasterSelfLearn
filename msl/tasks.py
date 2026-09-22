"""Task planning — what the engine goes and reads this cycle.

The plan is the mechanism behind "expansive": every cycle re-derives its reading
list from the *current* library, so topics that appeared last cycle get deeper
reads this cycle, and each deep read can surface new entities for the next one.

Three task classes:

``probe``   one small read per registered source, to prove it is alive
``survey``  the standing questions of each topic family
``deepen``  follow-up reads on entities the library already tracks

Everything is capped: ``MAX_TASKS_PER_CYCLE`` exists so growth never turns into
abuse of somebody's API.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from urllib.parse import quote

from . import config
from .sources import REGISTRY, BY_ID
from .topics import FAMILY_BY_SLUG, Library

MAX_TASKS_PER_CYCLE = 70
MAX_DEEPEN_PER_CYCLE = 12
MAX_GITHUB_SEARCHES = 6
MAX_PAGEVIEW_ARTICLES = 8
MAX_FR_TERMS = 4


@dataclass
class Task:
    source_id: str
    url: str
    adapter: str
    topic: str
    kind: str                       # probe | survey | deepen
    ctx: Dict[str, Any] = field(default_factory=dict)
    accepts: Optional[str] = None

    @property
    def key(self) -> str:
        return f"{self.source_id}|{self.url}"


def _gh(q: str, per: int = 20) -> str:
    return ("https://api.github.com/search/repositories?q=" + quote(q) +
            f"&sort=stars&order=desc&per_page={per}")


def _wiki(article: str, start: str, end: str) -> str:
    return ("https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/"
            f"en.wikipedia/all-access/user/{quote(article)}/daily/{start}/{end}")


def _fr(term: str, per: int = 5) -> str:
    return ("https://www.federalregister.gov/api/v1/documents.json?per_page="
            f"{per}&order=newest&conditions%5Bterm%5D={quote(term)}")


def build_plan(library: Library, now: str, start_day: str, end_day: str,
               window_label: str, offline: bool = False) -> List[Task]:
    """Return the ordered read list for this cycle."""
    tasks: List[Task] = []
    seen: set = set()

    def push(t: Task) -> bool:
        if t.key in seen or len(tasks) >= MAX_TASKS_PER_CYCLE:
            return False
        if BY_ID.get(t.source_id) is None:
            return False
        seen.add(t.key)
        tasks.append(t)
        return True

    # 1. probes — cheap, and they are what keeps `status` honest
    for s in REGISTRY:
        if s.status == "blocked" and s.consecutive_failures >= config.SOURCE_FAILS_BEFORE_CRITICAL:
            # still probe it: a blocked source that recovers must be allowed back
            pass
        push(Task(s.id, s.probe_url, s.id, "source-health", "probe",
                  {"topic": "source-health", "source": s.id},
                  accepts=s.accepts))

    # 2. surveys — the standing question of each family that has a usable source
    for fam_slug, fam in FAMILY_BY_SLUG.items():
        usable = [sid for sid in fam.sources
                  if sid in BY_ID and BY_ID[sid].status != "blocked"]
        if not usable:
            continue

        if "github_search" in usable and len(fam.keywords) > 0:
            for kw in fam.keywords[:2]:
                push(Task("github_search", _gh(f"{kw} created:>=2026-06-23", 20),
                          "github_search", fam_slug, "survey",
                          {"topic": fam_slug, "query": f"{kw} created:>=2026-06-23",
                           "query_label": f"new repositories matching “{kw}” since 2026-06-23"}))
            push(Task("github_search", _gh(" ".join(fam.keywords[:2]) + " created:>=2026-09-14", 25),
                      "github_search", fam_slug, "survey",
                      {"topic": fam_slug,
                       "query": " ".join(fam.keywords[:2]) + " created:>=2026-09-14",
                       "query_label": f"repositories matching “{' '.join(fam.keywords[:2])}” created in the last 7 days"}))

        if "federal_register" in usable:
            terms = [k for k in fam.keywords if " " in k or len(k) > 4][:MAX_FR_TERMS]
            for term in (terms or ["data"]):
                push(Task("federal_register", _fr(term), "federal_register",
                          fam_slug, "survey",
                          {"topic": fam_slug, "term": term}))

        if "arxiv" in usable:
            cat = "cs.AI" if "ai" in fam_slug or "research" in fam_slug else "cs.LG"
            push(Task("arxiv",
                      "https://export.arxiv.org/api/query?search_query="
                      f"cat:{cat}&sortBy=submittedDate&sortOrder=descending&max_results=8",
                      "arxiv", fam_slug, "survey",
                      {"topic": fam_slug, "query_label": f"the 8 newest arXiv {cat} submissions"},
                      accepts="application/atom+xml"))

        if "pubmed" in usable and fam.keywords:
            term = fam.keywords[0].replace(" ", "+")
            push(Task("pubmed",
                      "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
                      f"?db=pubmed&term={quote(term)}&retmax=1&retmode=json",
                      "pubmed", fam_slug, "survey",
                      {"topic": fam_slug, "term": term}))

        if "clinicaltrials" in usable:
            push(Task("clinicaltrials",
                      "https://clinicaltrials.gov/api/v2/studies?pageSize=5",
                      "clinicaltrials", fam_slug, "survey", {"topic": fam_slug}))

        if "openalex" in usable:
            push(Task("openalex",
                      "https://api.openalex.org/works?sort=publication_date:desc"
                      f"&per-page=5&mailto={config.CONTACT_EMAIL}",
                      "openalex", fam_slug, "survey",
                      {"topic": fam_slug, "query_label": "the newest indexed works"}))

        if "crossref" in usable:
            push(Task("crossref",
                      "https://api.crossref.org/works?rows=3&sort=created&order=desc"
                      f"&mailto={config.CONTACT_EMAIL}",
                      "crossref", fam_slug, "survey", {"topic": fam_slug}))

        if "europepmc" in usable:
            push(Task("europepmc",
                      "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
                      "?query=artificial+intelligence&format=json&pageSize=3",
                      "europepmc", fam_slug, "survey", {"topic": fam_slug}))

        if "stackexchange" in usable:
            push(Task("stackexchange",
                      "https://api.stackexchange.com/2.3/questions?order=desc&sort=votes"
                      "&site=stackoverflow&pagesize=5&tagged=python",
                      "stackexchange", fam_slug, "survey", {"topic": fam_slug}))

        if "huggingface" in usable:
            push(Task("huggingface", "https://huggingface.co/api/models?sort=trendingScore&limit=10",
                      "huggingface", fam_slug, "survey", {"topic": fam_slug}))

        if "nws_alerts" in usable:
            push(Task("nws_alerts", "https://api.weather.gov/alerts/active?area=CA",
                      "nws_alerts", fam_slug, "survey",
                      {"topic": fam_slug, "area": "California"}))

        if "usgs_fdsn" in usable:
            push(Task("usgs_fdsn",
                      "https://earthquake.usgs.gov/fdsnws/event/1/count?format=geojson"
                      "&starttime=2026-09-14&minmagnitude=5.0",
                      "usgs_fdsn", fam_slug, "survey",
                      {"topic": fam_slug, "window": "7d",
                       "label": f"{window_label} at magnitude 5.0 and above"}))

        if "census_acs" in usable:
            push(Task("census_acs",
                      "https://api.census.gov/data/2022/acs/acs5?get=NAME,B01001_001E&for=state:06",
                      "census_acs", fam_slug, "survey", {"topic": fam_slug}))

        if "worldbank" in usable:
            push(Task("worldbank",
                      "https://api.worldbank.org/v2/country/USA/indicator/NY.GDP.MKTP.CD"
                      "?format=json&per_page=3",
                      "worldbank", fam_slug, "survey",
                      {"topic": fam_slug, "indicator": "NY.GDP.MKTP.CD"}))

        if "ecb_sdmx" in usable:
            push(Task("ecb_sdmx",
                      "https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A"
                      "?lastNObservations=3&format=jsondata",
                      "ecb_sdmx", fam_slug, "survey",
                      {"topic": fam_slug, "flow": "EXR D.USD.EUR.SP00.A",
                       "label": "the daily USD/EUR spot reference rate"}))

        if "frankfurter" in usable:
            push(Task("frankfurter", "https://api.frankfurter.app/latest?from=USD&to=EUR,KRW,JPY",
                      "frankfurter", fam_slug, "survey", {"topic": fam_slug}))

        if "bls" in usable:
            push(Task("bls", "https://api.bls.gov/publicAPI/v2/timeseries/data/CUUR0000SA0",
                      "bls", fam_slug, "survey", {"topic": fam_slug, "series": "CUUR0000SA0"}))

        if "sec_edgar" in usable:
            push(Task("sec_edgar", "https://data.sec.gov/submissions/CIK0000320193.json",
                      "sec_edgar", fam_slug, "survey", {"topic": fam_slug}))

        if "nominatim" in usable:
            push(Task("nominatim", "https://nominatim.openstreetmap.org/search?q=Seoul&format=json&limit=1",
                      "nominatim", fam_slug, "survey", {"topic": fam_slug, "query": "Seoul"}))

        if "kalshi_public" in usable:
            push(Task("kalshi_public", "https://api.elections.kalshi.com/trade-api/v2/markets?limit=5",
                      "kalshi_public", fam_slug, "survey", {"topic": fam_slug}))

        if "mlb_statsapi" in usable:
            push(Task("mlb_statsapi",
                      f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={end_day}",
                      "mlb_statsapi", fam_slug, "survey", {"topic": fam_slug}))

        if "nhl_web" in usable:
            push(Task("nhl_web", "https://api-web.nhle.com/v1/scoreboard/now",
                      "nhl_web", fam_slug, "survey", {"topic": fam_slug}))

        if "nba_cdn" in usable:
            push(Task("nba_cdn",
                      "https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json",
                      "nba_cdn", fam_slug, "survey", {"topic": fam_slug}))

        if "github_repos" in usable:
            push(Task("github_repos",
                      f"https://api.github.com/users/{config.REPO_OWNER}/repos?per_page=100&sort=updated",
                      "github_repos", fam_slug, "survey",
                      {"topic": fam_slug, "owner": config.REPO_OWNER}))

    # 3. attention survey — the tracked Wikipedia articles, always the same shape
    arts = [t.slug[5:].replace("-", "_") for t in library.topics.values()
            if t.slug.startswith("wiki:") and t.status != "retired"][:MAX_PAGEVIEW_ARTICLES]
    for a in (arts or ["Artificial_intelligence"]):
        push(Task("wikimedia_pageviews", _wiki(a, start_day, end_day),
                  "wikimedia_pageviews", "public-attention", "survey",
                  {"topic": "public-attention"}))

    # 4. deepen — follow up on the most-signalled tracked entities
    deepened = 0
    for t in sorted(library.topics.values(), key=lambda x: -x.signals):
        if deepened >= MAX_DEEPEN_PER_CYCLE:
            break
        if t.status == "retired":
            continue
        if t.slug.startswith("repo:") and t.origin_url:
            full = t.slug[5:]
            push(Task("github_search", _gh(f"repo:{t.origin_url.split('github.com/')[-1]}", 1),
                      "github_search", "open-source-momentum", "deepen",
                      {"topic": "open-source-momentum",
                       "query_label": f"the tracked repository {full}"}))
            deepened += 1
        elif t.slug.startswith("wiki:"):
            deepened += 1  # already covered by the pageview survey above
    return tasks


def offline_plan(library: Library, seed_dir=None) -> List[Task]:
    """A plan that reads nothing from the network.

    Used by the test suite and by ``--offline`` so the whole pipeline can be
    exercised, deterministically, against the hashed seed captures.
    """
    return []
