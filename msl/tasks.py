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

Every date and window in a task URL is derived from the cycle's own clock.  They
used to be literals recorded on 2026-09-21 (``created:>=2026-09-14`` for a query
whose label said "created in the last 7 days", ``starttime=2026-09-14`` for a
count whose label said a different week).  A literal window does not fail when it
goes stale: it keeps returning a real number for a window the sentence no longer
describes, which is a confidently-published false statement.  The window is now
computed, so the query and the sentence cannot drift apart.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from urllib.parse import quote

from . import config
from .sources import REGISTRY, BY_ID
from .topics import FAMILY_BY_SLUG, STATUS_RETIRED, Library

#: Hard ceiling on reads in one cycle.  It exists to bound this engine's appetite,
#: not to be reached: when it *is* reached the plan is truncated and, because a
#: silent drop is a hidden gap, the dropped count is published as an irregularity.
#: (Until 2026-09-22 the cap was 70 and the plan was already exactly 70, so the
#: last deepening task was being dropped every cycle with nothing said about it.)
MAX_TASKS_PER_CYCLE = 84
#: Repositories followed up per cycle with the two Repositories API reads.
MAX_REPO_DEEPEN_PER_CYCLE = 3
MAX_GITHUB_SEARCHES = 6
MAX_PAGEVIEW_ARTICLES = 8
MAX_FR_TERMS = 4


def iso_day(compact: str) -> str:
    """``20260909`` → ``2026-09-09``.  Anything else is returned unchanged."""
    s = str(compact)
    return f"{s[0:4]}-{s[4:6]}-{s[6:8]}" if len(s) == 8 and s.isdigit() else s


def compact_day(now: str, days_back: int) -> str:
    """``now`` minus ``days_back`` days, as the ``YYYYMMDD`` the APIs want."""
    d = datetime.strptime(now[:10], "%Y-%m-%d") - timedelta(days=days_back)
    return d.strftime("%Y%m%d")


def repo_full_name(url: str) -> str:
    """``https://github.com/owner/name`` → ``owner/name`` (else ``""``)."""
    parts = [p for p in (url or "").split("/") if p]
    for i, p in enumerate(parts):
        if p.endswith("github.com") and len(parts) > i + 2:
            return f"{parts[i + 1]}/{parts[i + 2]}"
    return ""


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
               window_label: str, offline: bool = False,
               stats: Optional[Dict[str, int]] = None) -> List[Task]:
    """Return the ordered read list for this cycle.

    ``stats``, when given, is filled with ``planned`` / ``dropped`` / ``cap``.  A
    task dropped by the cap used to be dropped in silence, which made the cap look
    like a plan that simply happened to be that size.
    """
    tasks: List[Task] = []
    seen: set = set()
    since_90d = iso_day(compact_day(now, 90))
    since_7d = iso_day(compact_day(now, 7))

    def push(t: Task) -> bool:
        if t.key in seen:
            return False                       # the same read twice is not a drop
        if BY_ID.get(t.source_id) is None:
            return False                       # an unregistered source is not a drop
        if len(tasks) >= MAX_TASKS_PER_CYCLE:
            if stats is not None:
                stats["dropped"] = stats.get("dropped", 0) + 1
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
                push(Task("github_search", _gh(f"{kw} created:>={since_90d}", 20),
                          "github_search", fam_slug, "survey",
                          {"topic": fam_slug, "query": f"{kw} created:>={since_90d}",
                           "query_label": f"new repositories matching “{kw}” created "
                                          f"since {since_90d}"}))
            push(Task("github_search", _gh(" ".join(fam.keywords[:2]) + f" created:>={since_7d}", 25),
                      "github_search", fam_slug, "survey",
                      {"topic": fam_slug,
                       "query": " ".join(fam.keywords[:2]) + f" created:>={since_7d}",
                       "query_label": f"repositories matching “{' '.join(fam.keywords[:2])}” "
                                      f"created since {since_7d}"}))

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
            # No hand-written area here: the probe reads the same URL, and if the two
            # tasks described it differently they would write the same measurement
            # under two different field names — the probe used to file this count as
            # ``nws.alerts[US]`` while the survey filed it as ``nws.alerts[California]``
            # for one and the same California query.  The URL says CA; that is what
            # both tasks now record.
            push(Task("nws_alerts", "https://api.weather.gov/alerts/active?area=CA",
                      "nws_alerts", fam_slug, "survey", {"topic": fam_slug}))

        if "usgs_fdsn" in usable:
            push(Task("usgs_fdsn",
                      "https://earthquake.usgs.gov/fdsnws/event/1/count?format=geojson"
                      f"&starttime={iso_day(start_day)}&endtime={iso_day(end_day)}"
                      "&minmagnitude=5.0",
                      "usgs_fdsn", fam_slug, "survey",
                      {"topic": fam_slug, "window": "7d",
                       # Only consulted if the URL loses its dates; the query's own
                       # window wins, because that is what was read.
                       "window_label": window_label}))

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
            # StatsAPI wants ISO dates, and this engine has proof: every recorded
            # MLB claim in data/claims.jsonl was read with `date=2026-09-20` and
            # returned a coherent schedule (15 games).  The pageview and USGS APIs
            # want the compact form, so `end_day` is compact here and has to be
            # converted — passing it straight through would send `date=20260920`,
            # a format this project has never seen answered.
            push(Task("mlb_statsapi",
                      "https://statsapi.mlb.com/api/v1/schedule?sportId=1"
                      f"&date={iso_day(end_day)}",
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
    # Wikipedia titles are case-sensitive past the first character, so the
    # article must come from the topic's recorded title and never be rebuilt
    # from its slug.  Slugs are lowercased for use as anchors; asking the API
    # for "artificial_intelligence" returns a different, near-empty page and the
    # engine then publishes a confident claim about the wrong subject.
    # MediaWiki auto-capitalises the first letter of every article title, so a
    # recorded title that starts lower-case is not a title — it is the slug read
    # back.  Asking for a lowercased title returns a different page, which is what
    # produced the retracted "artificial_intelligence" claims.  The old filter here
    # approximated that by requiring an underscore in the slug, which would also
    # have thrown away a perfectly good article such as "ChatGPT"; the capital is
    # the actual rule and it is what is checked now.
    arts = []
    skipped_titles = 0
    for t in library.topics.values():
        if not t.slug.startswith("wiki:") or t.status == STATUS_RETIRED:
            continue
        title = (t.title or "").strip()
        if not title or not title[0].isupper():
            skipped_titles += 1
            continue
        if title not in arts:
            arts.append(title)
    if stats is not None and skipped_titles:
        stats["wikiTitlesSkipped"] = skipped_titles
    arts = arts[:MAX_PAGEVIEW_ARTICLES]
    for a in (arts or ["Artificial_intelligence"]):
        push(Task("wikimedia_pageviews", _wiki(a, start_day, end_day),
                  "wikimedia_pageviews", "public-attention", "survey",
                  {"topic": "public-attention"}))

    # 4. deepen — follow up on the most-signalled tracked entities
    #
    # This used to be a `repo:owner/name` *search* per tracked repository, which is
    # the wrong bucket to spend: GitHub's unauthenticated search limit is 10
    # requests/minute and one of those deepen searches was answered "403 rate limit
    # exceeded" (recorded in the irregularity register, cycle 11).  The two
    # Repositories API reads below share nothing with that limit (they are core API,
    # which this engine barely touches), and they return what the Search API does
    # not: open issues, watching users, size, last push, primary language,
    # repository state, and the newest release tag.  Star and fork counts still
    # arrive, under the same field names as before, so no series is broken.
    tracked_repos = [t for t in sorted(library.topics.values(),
                                       key=lambda x: (-x.signals, x.slug))
                     if t.status != STATUS_RETIRED and t.slug.startswith("repo:")
                     and t.origin_url]
    for t in tracked_repos[:MAX_REPO_DEEPEN_PER_CYCLE]:
        full = repo_full_name(t.origin_url) or t.slug[5:]
        family = t.family if t.family in FAMILY_BY_SLUG else "open-source-momentum"
        push(Task("github_repo", f"https://api.github.com/repos/{full}",
                  "github_repo", family, "deepen",
                  {"topic": family, "repo": full}))
        push(Task("github_releases", f"https://api.github.com/repos/{full}/releases?per_page=1",
                  "github_releases", family, "deepen",
                  {"topic": family, "repo": full}))
    if stats is not None:
        stats["planned"] = len(tasks)
        stats["cap"] = MAX_TASKS_PER_CYCLE
    return tasks

