# IRREGULARITIES

Generated `2026-09-22T01:41:22Z` at cycle 5.

56 registered — 0 critical,
19 warn, 37 info.
30 open, 26 resolved,
14 standing.

**Standing** entries are structural limits of this project, not transient
failures: they do not auto-resolve, because the owner needs to keep seeing them.
A non-standing entry that stops recurring is marked `resolved` rather than
deleted, so the register keeps its history.

---

## WARN (19)

### `IRR-033` — The owner's source document could not be read by a machine

*WARN* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 5 (2026-09-22T01:41:22Z) · 5 occurrence(s) · **open** · standing · topic `owner-corpus`

The brief points at a shared ChatGPT transcript (https://chatgpt.com/share/6ab1612a-2f14-83e8-9de6-808d21a48e53). A GET of that URL returns an HTML shell whose body is rendered client-side; the only server-supplied content is the <title>, “Design Autonomous Research System”. No requirement in this repository is sourced from that transcript. The design was derived instead from the written brief and from the owner's own published corpus, which is readable. If the transcript contains requirements that are missing here, they are missing.

**Reproduce:** `curl -s https://chatgpt.com/share/6ab1612a-2f14-83e8-9de6-808d21a48e53 | grep -o '<title>[^<]*'`

### `IRR-034` — GitHub publishes no trending API

*WARN* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 5 (2026-09-22T01:41:22Z) · 5 occurrence(s) · **open** · standing · source `github_search` · topic `open-source-momentum`

The obvious “trending repositories” signal has no official endpoint: https://github.com/trending returns HTML only, and GitHub's REST API exposes no trending route. The engine substitutes the official Search API sorted by stars over a created:>= window, which is reproducible and documented, and says so wherever the number appears. A trending *page* is a curated list with an undisclosed ranking; a search result is not, and the two are not equivalent.

**Reproduce:** `curl -s -o /dev/null -w '%{http_code} %{content_type}\n' https://github.com/trending`

### `IRR-035` — npm's documented media type is rejected by its own dist-tags endpoint

*WARN* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 5 (2026-09-22T01:41:22Z) · 5 occurrence(s) · **open** · standing · source `npm_registry` · topic `open-source-momentum`

GET https://registry.npmjs.org/-/package/next/dist-tags answers 200 for Accept: application/json and HTTP 406 Not Acceptable for Accept: application/vnd.npm.install-v1+json — the media type the registry documents for package metadata. Observed 2026-09-21 from two independent hosts. The engine therefore sends Accept: application/json for this route. This is recorded rather than quietly worked around so the next reader does not rediscover it.

**Reproduce:** `curl -s -o /dev/null -w '%{http_code}\n' -H 'Accept: application/vnd.npm.install-v1+json' https://registry.npmjs.org/-/package/next/dist-tags   # -> 406`

### `IRR-036` — Three interest categories have no registered source that can serve them

*WARN* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 5 (2026-09-22T01:41:22Z) · 5 occurrence(s) · **open** · standing · topic `travel-korea`

Travel & Korea Trip, Social & Creator Data, and Elections & Civic Data appear in the owner's verified corpus, but no official keyless API is registered that can answer their questions: hotel and airfare pricing has no keyless official API at all; every creator platform API is keyed; the FEC API requires a key for most routes and state results are per-jurisdiction. No claim is made about these categories. See KEYED_SOURCES_EXCLUDED in msl/sources.py and ROADMAP.md.

**Reproduce:** `python3 -c "import msl.sources as s; print(s.INTEREST_CATEGORIES_WITHOUT_A_SOURCE)"`

### `IRR-042` — Topics with no verified claims behind them

*WARN* · first seen cycle 3 (2026-09-22T01:34:57Z) · last seen cycle 5 (2026-09-22T01:41:22Z) · 3 occurrence(s) · **open** · topic `library`

19 tracked topic(s) were proposed at least two cycles ago and still have zero verified claims: agency:health-and-human-services-department, agency:securities-and-exchange-commission, repo:zai-org/zcode, agency:centers-for-disease-control-and-prevention, frdoc:2026-19271, frdoc:2026-19148, sf-local, repo:brayonpi/hexstellar, repo:hanyuanwang/livestream-agent-studio, repo:jtydhr88/screenwriting-skills, repo:nanako0129/sepia, repo:shadcn-ui/lint (+7 more).  They are listed as unsupported rather than described, and each will be retired after 96 cycles without a signal. If a topic matters, the fix is to register a source that can answer it — not to write prose about it.

**Reproduce:** `python3 -c "import json;[print(t['slug']) for t in json.load(open('data/library.json'))['topics'] if t['claims']==0]"`

### `IRR-043` — clinicaltrials could not be read

*WARN* · first seen cycle 4 (2026-09-22T01:39:14Z) · last seen cycle 5 (2026-09-22T01:41:22Z) · 2 occurrence(s) · **open** · source `clinicaltrials` · topic `source-health`

HTTPError: HTTP 403 Forbidden on GET https://clinicaltrials.gov/api/v2/studies?pageSize=1 after 3 attempt(s). No claim was produced and no substitute value was invented.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://clinicaltrials.gov/api/v2/studies?pageSize=1'`

### `IRR-044` — clinicaltrials rate-limited this cycle

*WARN* · first seen cycle 4 (2026-09-22T01:39:14Z) · last seen cycle 5 (2026-09-22T01:41:22Z) · 4 occurrence(s) · **open** · source `clinicaltrials`

HTTP 403 on https://clinicaltrials.gov/api/v2/studies?pageSize=5. The engine backs off rather than retrying, and produces no claim from this source this cycle.

**Reproduce:** `curl -sSI 'https://clinicaltrials.gov/api/v2/studies?pageSize=1' | head -5`

### `IRR-045` — ecb_sdmx payload shape problem

*WARN* · first seen cycle 4 (2026-09-22T01:39:14Z) · last seen cycle 5 (2026-09-22T01:41:22Z) · 2 occurrence(s) · **open** · source `ecb_sdmx` · topic `source-health`

ecb_sdmx: unexpected jsondata shape (KeyError: 'data')  Zero facts were taken from the affected part of the payload.

**Reproduce:** `curl -sS 'https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A?lastNObservations=1&format=jsondata' | head -c 400`

### `IRR-046` — sec_edgar could not be read

*WARN* · first seen cycle 4 (2026-09-22T01:39:14Z) · last seen cycle 5 (2026-09-22T01:41:22Z) · 2 occurrence(s) · **open** · source `sec_edgar` · topic `source-health`

HTTPError: HTTP 403 Forbidden on GET https://data.sec.gov/submissions/CIK0000320193.json after 3 attempt(s). No claim was produced and no substitute value was invented.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://data.sec.gov/submissions/CIK0000320193.json'`

### `IRR-047` — sec_edgar rate-limited this cycle

*WARN* · first seen cycle 4 (2026-09-22T01:39:14Z) · last seen cycle 5 (2026-09-22T01:41:22Z) · 2 occurrence(s) · **open** · source `sec_edgar`

HTTP 403 on https://data.sec.gov/submissions/CIK0000320193.json. The engine backs off rather than retrying, and produces no claim from this source this cycle.

**Reproduce:** `curl -sSI 'https://data.sec.gov/submissions/CIK0000320193.json' | head -5`

### `IRR-048` — nhl_web payload shape problem

*WARN* · first seen cycle 4 (2026-09-22T01:39:14Z) · last seen cycle 5 (2026-09-22T01:41:22Z) · 2 occurrence(s) · **open** · source `nhl_web` · topic `source-health`

nhl_web: games is not a list  Zero facts were taken from the affected part of the payload.

**Reproduce:** `curl -sS 'https://api-web.nhle.com/v1/scoreboard/now' | head -c 400`

### `IRR-049` — nba_cdn could not be read

*WARN* · first seen cycle 4 (2026-09-22T01:39:14Z) · last seen cycle 5 (2026-09-22T01:41:22Z) · 2 occurrence(s) · **open** · source `nba_cdn` · topic `source-health`

HTTPError: HTTP 403 Forbidden on GET https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json after 3 attempt(s). No claim was produced and no substitute value was invented.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json'`

### `IRR-050` — nba_cdn rate-limited this cycle

*WARN* · first seen cycle 4 (2026-09-22T01:39:14Z) · last seen cycle 5 (2026-09-22T01:41:22Z) · 2 occurrence(s) · **open** · source `nba_cdn`

HTTP 403 on https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json. The engine backs off rather than retrying, and produces no claim from this source this cycle.

**Reproduce:** `curl -sSI 'https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json' | head -5`

### `IRR-051` — ecb_sdmx payload shape problem

*WARN* · first seen cycle 4 (2026-09-22T01:39:14Z) · last seen cycle 5 (2026-09-22T01:41:22Z) · 2 occurrence(s) · **open** · source `ecb_sdmx` · topic `macro-signals`

ecb_sdmx: unexpected jsondata shape (KeyError: 'data')  Zero facts were taken from the affected part of the payload.

**Reproduce:** `curl -sS 'https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A?lastNObservations=3&format=jsondata' | head -c 400`

### `IRR-052` — clinicaltrials could not be read

*WARN* · first seen cycle 4 (2026-09-22T01:39:14Z) · last seen cycle 5 (2026-09-22T01:41:22Z) · 2 occurrence(s) · **open** · source `clinicaltrials` · topic `clinical-evidence`

HTTPError: HTTP 403 Forbidden on GET https://clinicaltrials.gov/api/v2/studies?pageSize=5 after 3 attempt(s). No claim was produced and no substitute value was invented.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://clinicaltrials.gov/api/v2/studies?pageSize=5'`

### `IRR-053` — mlb_statsapi could not be read

*WARN* · first seen cycle 4 (2026-09-22T01:39:14Z) · last seen cycle 5 (2026-09-22T01:41:22Z) · 2 occurrence(s) · **open** · source `mlb_statsapi` · topic `sports-signals`

HTTPError: HTTP 400 Bad Request on GET https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=20260915 after 3 attempt(s). No claim was produced and no substitute value was invented.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=20260915'`

### `IRR-054` — 5 of 70 planned reads failed

*WARN* · first seen cycle 4 (2026-09-22T01:39:14Z) · last seen cycle 5 (2026-09-22T01:41:22Z) · 2 occurrence(s) · **open**

5 read(s) failed while 65 succeeded. Each failure is listed separately with its HTTP status or transport error and a reproduction command. A partial cycle is still published, but every figure that would have come from a failed source is absent rather than carried forward silently.

**Reproduce:** `python3 tools/probe_sources.py`

### `IRR-055` — europepmc payload shape problem

*WARN* · first seen cycle 5 (2026-09-22T01:41:22Z) · last seen cycle 5 (2026-09-22T01:41:22Z) · 1 occurrence(s) · **open** · source `europepmc` · topic `source-health`

europepmc: hitCount missing  Zero facts were taken from the affected part of the payload.

**Reproduce:** `curl -sS 'https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=artificial+intelligence&format=json&pageSize=1' | head -c 400`

### `IRR-056` — europepmc payload shape problem

*WARN* · first seen cycle 5 (2026-09-22T01:41:22Z) · last seen cycle 5 (2026-09-22T01:41:22Z) · 1 occurrence(s) · **open** · source `europepmc` · topic `ai-research-frontier`

europepmc: hitCount missing  Zero facts were taken from the affected part of the payload.

**Reproduce:** `curl -sS 'https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=artificial+intelligence&format=json&pageSize=3' | head -c 400`


## INFO (37)

### `IRR-002` — Some derived claims cannot be re-checked

*INFO* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 5 (2026-09-22T01:41:22Z) · 5 occurrence(s) · **open** · standing · topic `derived`

244 derived claim(s) use a formula whose value depends on the wall clock at read time — a repository's stars-per-day, for example, has 'now' in its denominator. They are counted as NOT RECHECKED rather than as passing, because a check that cannot be repeated is not a check.

**Reproduce:** `python3 -m msl.cli verify-claims`

### `IRR-022` — Source census_acs has never been read

*INFO* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 5 (2026-09-22T01:41:22Z) · 5 occurrence(s) · **open** · source `census_acs`

U.S. Census Bureau API (ACS 5-year) (U.S. Census Bureau) is registered with a documentation URL but no successful read has been recorded yet. No claim has been built from it. The next probe will either verify it or record why it failed.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://api.census.gov/data/2022/acs/acs5?get=NAME,B01001_001E&for=state:06'`

### `IRR-028` — mlb_statsapi is an undocumented public endpoint

*INFO* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 5 (2026-09-22T01:41:22Z) · 5 occurrence(s) · **open** · standing · source `mlb_statsapi`

No official public documentation page has been located for this endpoint.  Registered as UNDOCUMENTED so the irregularity register keeps it visible rather than the site implying a contract exists.  Claims built from it carry the same marker.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=2026-09-20'`

### `IRR-030` — nhl_web is an undocumented public endpoint

*INFO* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 5 (2026-09-22T01:41:22Z) · 5 occurrence(s) · **open** · standing · source `nhl_web`

UNDOCUMENTED public endpoint; no official contract page located.  See IRR-009.  Claims built from it carry the same marker.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://api-web.nhle.com/v1/scoreboard/now'`

### `IRR-032` — nba_cdn is an undocumented public endpoint

*INFO* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 5 (2026-09-22T01:41:22Z) · 5 occurrence(s) · **open** · standing · source `nba_cdn`

UNDOCUMENTED public endpoint; no official contract page located.  See IRR-009.  Claims built from it carry the same marker.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json'`

### `IRR-037` — Six useful sources are excluded because they need an API key

*INFO* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 5 (2026-09-22T01:41:22Z) · 5 occurrence(s) · **open** · standing

FRED, the NFL Game API, Google Trends, the X API, the YouTube Data API and the TikTok/Instagram APIs were all rejected. Obtaining a key is manual input, which the brief rules out. Each is listed with the reason in msl/sources.py → KEYED_SOURCES_EXCLUDED so the omission is a decision on the record, not a gap.

**Reproduce:** `python3 -c "import msl.sources as s; [print(x['id'], x['reason']) for x in s.KEYED_SOURCES_EXCLUDED]"`

### `IRR-038` — Three sports feeds are undocumented public endpoints

*INFO* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 5 (2026-09-22T01:41:22Z) · 5 occurrence(s) · **open** · standing · topic `sports-signals`

statsapi.mlb.com, api-web.nhle.com and cdn.nba.com are the leagues' own hosts and the same feeds the owner's sibling labs already read, but no official public documentation page was located for any of them. They are registered with an explicit UNDOCUMENTED marker, and any claim built from one carries that marker too, so nothing on the site implies a contract exists.

**Reproduce:** `grep -n 'UNDOCUMENTED' msl/sources.py`

### `IRR-039` — Frankfurter is not an official ECB endpoint

*INFO* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 5 (2026-09-22T01:41:22Z) · 5 occurrence(s) · **open** · standing · source `frankfurter` · topic `macro-signals`

frankfurter.app republishes ECB euro reference rates but is a community service. It is registered as a redundancy check against the official ECB SDMX route, and every claim it produces is labelled third-party in the statement text itself, so it can never be quoted as an ECB figure.

**Reproduce:** `grep -n 'third-party' msl/adapters.py | head`

### `IRR-040` — The reasoning stage contains no language model

*INFO* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 5 (2026-09-22T01:41:22Z) · 5 occurrence(s) · **open** · standing

Every sentence published by this project is a template whose slots are filled from claim values, and every idea comes from a fixed rule set over the verified ledger. That is a deliberate limitation: it makes the output reproducible and auditable at the cost of novelty. A model with an API key would need a secret, and adding a secret is manual input. See METHODOLOGY.md §3.

**Reproduce:** `grep -rn 'openai\|anthropic\|llm_client' msl/ || echo 'no model client present'`

### `IRR-041` — Seed captures taken by an interactive read are not wire-hash verifiable

*INFO* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 5 (2026-09-22T01:41:22Z) · 5 occurrence(s) · **open** · standing

The first captures for wikimedia_pageviews, federal_register, usgs_fdsn and hn_firebase were read through an interactive agent fetch rather than by this process, so the stored SHA-256 covers the recorded body and not the bytes on the wire. Those evidence rows carry wireHashVerifiable=false, and the first automated probe re-reads each endpoint and reports whether the values still match.

**Reproduce:** `python3 -c "import json;[print(json.loads(l)['id'], json.loads(l)['wireHashVerifiable']) for l in open('data/evidence.jsonl') if not json.loads(l)['wireHashVerifiable']]"`

### `IRR-008` — Persona S06_MemoryWeighted is UNRANKED

*INFO* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 4 (2026-09-22T01:39:14Z) · 4 occurrence(s) · **resolved** · topic `competition`

Skill-weighted memory: 0 scored forecast(s); 3 required before a rank means anything.  It is excluded from the ranked table rather than shown at 0%, because a persona that has not been scored has not been beaten.

**Reproduce:** `python3 -c "import json;print(json.load(open('data/leaderboard.json'))['qualification'])"`

### `IRR-005` — Persona S03_Acceleration is UNRANKED

*INFO* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 3 (2026-09-22T01:34:57Z) · 3 occurrence(s) · **resolved** · topic `competition`

Acceleration: 1 scored forecast(s); 3 required before a rank means anything.  It is excluded from the ranked table rather than shown at 0%, because a persona that has not been scored has not been beaten.

**Reproduce:** `python3 -c "import json;print(json.load(open('data/leaderboard.json'))['qualification'])"`

### `IRR-006` — Persona S04_ConsensusFade is UNRANKED

*INFO* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 3 (2026-09-22T01:34:57Z) · 3 occurrence(s) · **resolved** · topic `competition`

Consensus fade: 1 scored forecast(s); 3 required before a rank means anything.  It is excluded from the ranked table rather than shown at 0%, because a persona that has not been scored has not been beaten.

**Reproduce:** `python3 -c "import json;print(json.load(open('data/leaderboard.json'))['qualification'])"`

### `IRR-010` — Source arxiv has never been read

*INFO* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 3 (2026-09-22T01:34:57Z) · 3 occurrence(s) · **resolved** · source `arxiv`

arXiv API (arXiv (Cornell University)) is registered with a documentation URL but no successful read has been recorded yet. No claim has been built from it. The next probe will either verify it or record why it failed.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results=1'`

### `IRR-011` — Source pubmed has never been read

*INFO* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 3 (2026-09-22T01:34:57Z) · 3 occurrence(s) · **resolved** · source `pubmed`

NCBI PubMed E-utilities (U.S. National Library of Medicine) is registered with a documentation URL but no successful read has been recorded yet. No claim has been built from it. The next probe will either verify it or record why it failed.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=artificial+intelligence&retmax=1&retmode=json'`

### `IRR-012` — Source clinicaltrials has never been read

*INFO* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 3 (2026-09-22T01:34:57Z) · 3 occurrence(s) · **resolved** · source `clinicaltrials`

ClinicalTrials.gov API v2 (U.S. National Library of Medicine) is registered with a documentation URL but no successful read has been recorded yet. No claim has been built from it. The next probe will either verify it or record why it failed.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://clinicaltrials.gov/api/v2/studies?pageSize=1'`

### `IRR-013` — Source openalex has never been read

*INFO* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 3 (2026-09-22T01:34:57Z) · 3 occurrence(s) · **resolved** · source `openalex`

OpenAlex scholarly graph (OurResearch (open catalogue of scholarly works)) is registered with a documentation URL but no successful read has been recorded yet. No claim has been built from it. The next probe will either verify it or record why it failed.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://api.openalex.org/works?sort=publication_date:desc&per-page=1'`

### `IRR-014` — Source crossref has never been read

*INFO* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 3 (2026-09-22T01:34:57Z) · 3 occurrence(s) · **resolved** · source `crossref`

Crossref REST API (Crossref) is registered with a documentation URL but no successful read has been recorded yet. No claim has been built from it. The next probe will either verify it or record why it failed.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://api.crossref.org/works?rows=1&sort=created&order=desc'`

### `IRR-015` — Source stackexchange has never been read

*INFO* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 3 (2026-09-22T01:34:57Z) · 3 occurrence(s) · **resolved** · source `stackexchange`

Stack Exchange API 2.3 (Stack Exchange, Inc.) is registered with a documentation URL but no successful read has been recorded yet. No claim has been built from it. The next probe will either verify it or record why it failed.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://api.stackexchange.com/2.3/questions?order=desc&sort=votes&site=stackoverflow&pagesize=1'`

### `IRR-016` — Source huggingface has never been read

*INFO* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 3 (2026-09-22T01:34:57Z) · 3 occurrence(s) · **resolved** · source `huggingface`

Hugging Face Hub API (Hugging Face, Inc.) is registered with a documentation URL but no successful read has been recorded yet. No claim has been built from it. The next probe will either verify it or record why it failed.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://huggingface.co/api/models?sort=trendingScore&limit=1'`

### `IRR-017` — Source nws_alerts has never been read

*INFO* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 3 (2026-09-22T01:34:57Z) · 3 occurrence(s) · **resolved** · source `nws_alerts`

api.weather.gov — active alerts (U.S. National Weather Service (NOAA)) is registered with a documentation URL but no successful read has been recorded yet. No claim has been built from it. The next probe will either verify it or record why it failed.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://api.weather.gov/alerts/active?area=CA'`

### `IRR-018` — Source worldbank has never been read

*INFO* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 3 (2026-09-22T01:34:57Z) · 3 occurrence(s) · **resolved** · source `worldbank`

World Bank Open Data API (The World Bank) is registered with a documentation URL but no successful read has been recorded yet. No claim has been built from it. The next probe will either verify it or record why it failed.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://api.worldbank.org/v2/country/USA/indicator/NY.GDP.MKTP.CD?format=json&per_page=1'`

### `IRR-019` — Source ecb_sdmx has never been read

*INFO* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 3 (2026-09-22T01:34:57Z) · 3 occurrence(s) · **resolved** · source `ecb_sdmx`

ECB Data Portal — SDMX REST (EXR daily) (European Central Bank) is registered with a documentation URL but no successful read has been recorded yet. No claim has been built from it. The next probe will either verify it or record why it failed.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A?lastNObservations=1&format=jsondata'`

### `IRR-020` — Source frankfurter has never been read

*INFO* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 3 (2026-09-22T01:34:57Z) · 3 occurrence(s) · **resolved** · source `frankfurter`

Frankfurter FX (ECB reference rates mirror) (Community service publishing ECB reference rates) is registered with a documentation URL but no successful read has been recorded yet. No claim has been built from it. The next probe will either verify it or record why it failed.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://api.frankfurter.app/latest?from=USD&to=EUR,KRW'`

### `IRR-021` — Source sec_edgar has never been read

*INFO* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 3 (2026-09-22T01:34:57Z) · 3 occurrence(s) · **resolved** · source `sec_edgar`

SEC EDGAR — company submissions (U.S. Securities and Exchange Commission) is registered with a documentation URL but no successful read has been recorded yet. No claim has been built from it. The next probe will either verify it or record why it failed.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://data.sec.gov/submissions/CIK0000320193.json'`

### `IRR-023` — Source bls has never been read

*INFO* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 3 (2026-09-22T01:34:57Z) · 3 occurrence(s) · **resolved** · source `bls`

U.S. Bureau of Labor Statistics Public Data API v2 (U.S. Bureau of Labor Statistics) is registered with a documentation URL but no successful read has been recorded yet. No claim has been built from it. The next probe will either verify it or record why it failed.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://api.bls.gov/publicAPI/v2/timeseries/data/CUUR0000SA0'`

### `IRR-024` — Source nominatim has never been read

*INFO* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 3 (2026-09-22T01:34:57Z) · 3 occurrence(s) · **resolved** · source `nominatim`

OpenStreetMap Nominatim (OpenStreetMap Foundation) is registered with a documentation URL but no successful read has been recorded yet. No claim has been built from it. The next probe will either verify it or record why it failed.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://nominatim.openstreetmap.org/search?q=Seoul&format=json&limit=1'`

### `IRR-025` — Source europepmc has never been read

*INFO* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 3 (2026-09-22T01:34:57Z) · 3 occurrence(s) · **resolved** · source `europepmc`

Europe PMC REST (European Molecular Biology Laboratory) is registered with a documentation URL but no successful read has been recorded yet. No claim has been built from it. The next probe will either verify it or record why it failed.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=artificial+intelligence&format=json&pageSize=1'`

### `IRR-026` — Source kalshi_public has never been read

*INFO* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 3 (2026-09-22T01:34:57Z) · 3 occurrence(s) · **resolved** · source `kalshi_public`

Kalshi public market data (KalshiEX LLC) is registered with a documentation URL but no successful read has been recorded yet. No claim has been built from it. The next probe will either verify it or record why it failed.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://api.elections.kalshi.com/trade-api/v2/markets?limit=1'`

### `IRR-027` — Source mlb_statsapi has never been read

*INFO* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 3 (2026-09-22T01:34:57Z) · 3 occurrence(s) · **resolved** · source `mlb_statsapi`

MLB StatsAPI — schedule (Major League Baseball Advanced Media) is registered with a documentation URL but no successful read has been recorded yet. No claim has been built from it. The next probe will either verify it or record why it failed.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=2026-09-20'`

### `IRR-029` — Source nhl_web has never been read

*INFO* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 3 (2026-09-22T01:34:57Z) · 3 occurrence(s) · **resolved** · source `nhl_web`

NHL public web API — scoreboard (National Hockey League) is registered with a documentation URL but no successful read has been recorded yet. No claim has been built from it. The next probe will either verify it or record why it failed.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://api-web.nhle.com/v1/scoreboard/now'`

### `IRR-031` — Source nba_cdn has never been read

*INFO* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 3 (2026-09-22T01:34:57Z) · 3 occurrence(s) · **resolved** · source `nba_cdn`

NBA CDN — today's scoreboard (National Basketball Association) is registered with a documentation URL but no successful read has been recorded yet. No claim has been built from it. The next probe will either verify it or record why it failed.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json'`

### `IRR-003` — Persona S01_MomentumPersist is UNRANKED

*INFO* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 2 (2026-09-22T01:34:57Z) · 2 occurrence(s) · **resolved** · topic `competition`

Momentum persistence: 0 scored forecast(s); 3 required before a rank means anything.  It is excluded from the ranked table rather than shown at 0%, because a persona that has not been scored has not been beaten.

**Reproduce:** `python3 -c "import json;print(json.load(open('data/leaderboard.json'))['qualification'])"`

### `IRR-004` — Persona S02_MeanRevert is UNRANKED

*INFO* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 2 (2026-09-22T01:34:57Z) · 2 occurrence(s) · **resolved** · topic `competition`

Mean reversion: 0 scored forecast(s); 3 required before a rank means anything.  It is excluded from the ranked table rather than shown at 0%, because a persona that has not been scored has not been beaten.

**Reproduce:** `python3 -c "import json;print(json.load(open('data/leaderboard.json'))['qualification'])"`

### `IRR-007` — Persona S05_EvidenceDensity is UNRANKED

*INFO* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 2 (2026-09-22T01:34:57Z) · 2 occurrence(s) · **resolved** · topic `competition`

Evidence density: 0 scored forecast(s); 3 required before a rank means anything.  It is excluded from the ranked table rather than shown at 0%, because a persona that has not been scored has not been beaten.

**Reproduce:** `python3 -c "import json;print(json.load(open('data/leaderboard.json'))['qualification'])"`

### `IRR-009` — Persona S10_Persistence is UNRANKED

*INFO* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 2 (2026-09-22T01:34:57Z) · 2 occurrence(s) · **resolved** · topic `competition`

Persistence (null model): 2 scored forecast(s); 3 required before a rank means anything.  It is excluded from the ranked table rather than shown at 0%, because a persona that has not been scored has not been beaten.

**Reproduce:** `python3 -c "import json;print(json.load(open('data/leaderboard.json'))['qualification'])"`

### `IRR-001` — “Travel & Korea” has no source that can answer its question

*INFO* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 1 (2026-09-22T01:34:57Z) · 1 occurrence(s) · **open** · standing · topic `travel-korea`

No official keyless API for lodging or airfare pricing is registered; nominatim can geocode a place but cannot price it. No pricing claim is made. See ROADMAP.md.

**Reproduce:** `python3 -c "from msl.topics import FAMILY_BY_SLUG; print(FAMILY_BY_SLUG['travel-korea'].blocked_reason)"`

