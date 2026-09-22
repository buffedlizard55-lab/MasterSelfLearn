# IRREGULARITIES

Generated `2026-09-21T12:00:00Z` at cycle 1.

42 registered — 1 critical,
5 warn, 36 info.
42 open, 0 resolved,
13 standing.

**Standing** entries are structural limits of this project, not transient
failures: they do not auto-resolve, because the owner needs to keep seeing them.
A non-standing entry that stops recurring is marked `resolved` rather than
deleted, so the register keeps its history.

---

## CRITICAL (1)

### `IRR-033` — No successful read this cycle

*CRITICAL* · first seen cycle 1 (2026-09-21T12:00:00Z) · last seen cycle 1 (2026-09-21T12:00:00Z) · 1 occurrence(s) · **open**

The task plan was empty — there was nothing to read, which in offline mode means no seed capture matched a registered source.  The usual cause is egress being blocked (a TLS/SSL EOF on every host is a network policy, not a data problem) or credentials having expired. A cycle that read nothing still publishes, and publishes nothing new.

**Reproduce:** `python3 tools/probe_sources.py`


## WARN (5)

### `IRR-032` — The interest profile could not be built

*WARN* · first seen cycle 1 (2026-09-21T12:00:00Z) · last seen cycle 1 (2026-09-21T12:00:00Z) · 1 occurrence(s) · **open** · topic `owner-corpus`

missing capture /tmp/msl-test-3irs0cdy/seed/owner_repos.json  Without the owner-corpus capture the engine cannot derive interest weights, so it uses signal counts alone. No profile was invented.

**Reproduce:** `ls -l data/seed/owner_repos.json`

### `IRR-034` — The owner's source document could not be read by a machine

*WARN* · first seen cycle 1 (2026-09-21T12:00:00Z) · last seen cycle 1 (2026-09-21T12:00:00Z) · 1 occurrence(s) · **open** · standing · topic `owner-corpus`

The brief points at a shared ChatGPT transcript (https://chatgpt.com/share/6ab1612a-2f14-83e8-9de6-808d21a48e53). A GET of that URL returns an HTML shell whose body is rendered client-side; the only server-supplied content is the <title>, “Design Autonomous Research System”. No requirement in this repository is sourced from that transcript. The design was derived instead from the written brief and from the owner's own published corpus, which is readable. If the transcript contains requirements that are missing here, they are missing.

**Reproduce:** `curl -s https://chatgpt.com/share/6ab1612a-2f14-83e8-9de6-808d21a48e53 | grep -o '<title>[^<]*'`

### `IRR-035` — GitHub publishes no trending API

*WARN* · first seen cycle 1 (2026-09-21T12:00:00Z) · last seen cycle 1 (2026-09-21T12:00:00Z) · 1 occurrence(s) · **open** · standing · source `github_search` · topic `open-source-momentum`

The obvious “trending repositories” signal has no official endpoint: https://github.com/trending returns HTML only, and GitHub's REST API exposes no trending route. The engine substitutes the official Search API sorted by stars over a created:>= window, which is reproducible and documented, and says so wherever the number appears. A trending *page* is a curated list with an undisclosed ranking; a search result is not, and the two are not equivalent.

**Reproduce:** `curl -s -o /dev/null -w '%{http_code} %{content_type}\n' https://github.com/trending`

### `IRR-036` — npm's documented media type is rejected by its own dist-tags endpoint

*WARN* · first seen cycle 1 (2026-09-21T12:00:00Z) · last seen cycle 1 (2026-09-21T12:00:00Z) · 1 occurrence(s) · **open** · standing · source `npm_registry` · topic `open-source-momentum`

GET https://registry.npmjs.org/-/package/next/dist-tags answers 200 for Accept: application/json and HTTP 406 Not Acceptable for Accept: application/vnd.npm.install-v1+json — the media type the registry documents for package metadata. Observed 2026-09-21 from two independent hosts. The engine therefore sends Accept: application/json for this route. This is recorded rather than quietly worked around so the next reader does not rediscover it.

**Reproduce:** `curl -s -o /dev/null -w '%{http_code}\n' -H 'Accept: application/vnd.npm.install-v1+json' https://registry.npmjs.org/-/package/next/dist-tags   # -> 406`

### `IRR-037` — Three interest categories have no registered source that can serve them

*WARN* · first seen cycle 1 (2026-09-21T12:00:00Z) · last seen cycle 1 (2026-09-21T12:00:00Z) · 1 occurrence(s) · **open** · standing · topic `travel-korea`

Travel & Korea Trip, Social & Creator Data, and Elections & Civic Data appear in the owner's verified corpus, but no official keyless API is registered that can answer their questions: hotel and airfare pricing has no keyless official API at all; every creator platform API is keyed; the FEC API requires a key for most routes and state results are per-jurisdiction. No claim is made about these categories. See KEYED_SOURCES_EXCLUDED in msl/sources.py and ROADMAP.md.

**Reproduce:** `python3 -c "import msl.sources as s; print(s.INTEREST_CATEGORIES_WITHOUT_A_SOURCE)"`


## INFO (36)

### `IRR-001` — “Travel & Korea” has no source that can answer its question

*INFO* · first seen cycle 1 (2026-09-21T12:00:00Z) · last seen cycle 1 (2026-09-21T12:00:00Z) · 1 occurrence(s) · **open** · standing · topic `travel-korea`

No official keyless API for lodging or airfare pricing is registered; nominatim can geocode a place but cannot price it. No pricing claim is made. See ROADMAP.md.

**Reproduce:** `python3 -c "from msl.topics import FAMILY_BY_SLUG; print(FAMILY_BY_SLUG['travel-korea'].blocked_reason)"`

### `IRR-002` — Persona S01_MomentumPersist is UNRANKED

*INFO* · first seen cycle 1 (2026-09-21T12:00:00Z) · last seen cycle 1 (2026-09-21T12:00:00Z) · 1 occurrence(s) · **open** · topic `competition`

Momentum persistence: 0 scored forecast(s); 3 required before a rank means anything.  It is excluded from the ranked table rather than shown at 0%, because a persona that has not been scored has not been beaten.

**Reproduce:** `python3 -c "import json;print(json.load(open('data/leaderboard.json'))['qualification'])"`

### `IRR-003` — Persona S02_MeanRevert is UNRANKED

*INFO* · first seen cycle 1 (2026-09-21T12:00:00Z) · last seen cycle 1 (2026-09-21T12:00:00Z) · 1 occurrence(s) · **open** · topic `competition`

Mean reversion: 0 scored forecast(s); 3 required before a rank means anything.  It is excluded from the ranked table rather than shown at 0%, because a persona that has not been scored has not been beaten.

**Reproduce:** `python3 -c "import json;print(json.load(open('data/leaderboard.json'))['qualification'])"`

### `IRR-004` — Persona S03_Acceleration is UNRANKED

*INFO* · first seen cycle 1 (2026-09-21T12:00:00Z) · last seen cycle 1 (2026-09-21T12:00:00Z) · 1 occurrence(s) · **open** · topic `competition`

Acceleration: 0 scored forecast(s); 3 required before a rank means anything.  It is excluded from the ranked table rather than shown at 0%, because a persona that has not been scored has not been beaten.

**Reproduce:** `python3 -c "import json;print(json.load(open('data/leaderboard.json'))['qualification'])"`

### `IRR-005` — Persona S04_ConsensusFade is UNRANKED

*INFO* · first seen cycle 1 (2026-09-21T12:00:00Z) · last seen cycle 1 (2026-09-21T12:00:00Z) · 1 occurrence(s) · **open** · topic `competition`

Consensus fade: 0 scored forecast(s); 3 required before a rank means anything.  It is excluded from the ranked table rather than shown at 0%, because a persona that has not been scored has not been beaten.

**Reproduce:** `python3 -c "import json;print(json.load(open('data/leaderboard.json'))['qualification'])"`

### `IRR-006` — Persona S05_EvidenceDensity is UNRANKED

*INFO* · first seen cycle 1 (2026-09-21T12:00:00Z) · last seen cycle 1 (2026-09-21T12:00:00Z) · 1 occurrence(s) · **open** · topic `competition`

Evidence density: 0 scored forecast(s); 3 required before a rank means anything.  It is excluded from the ranked table rather than shown at 0%, because a persona that has not been scored has not been beaten.

**Reproduce:** `python3 -c "import json;print(json.load(open('data/leaderboard.json'))['qualification'])"`

### `IRR-007` — Persona S06_MemoryWeighted is UNRANKED

*INFO* · first seen cycle 1 (2026-09-21T12:00:00Z) · last seen cycle 1 (2026-09-21T12:00:00Z) · 1 occurrence(s) · **open** · topic `competition`

Skill-weighted memory: 0 scored forecast(s); 3 required before a rank means anything.  It is excluded from the ranked table rather than shown at 0%, because a persona that has not been scored has not been beaten.

**Reproduce:** `python3 -c "import json;print(json.load(open('data/leaderboard.json'))['qualification'])"`

### `IRR-008` — Persona S10_Persistence is UNRANKED

*INFO* · first seen cycle 1 (2026-09-21T12:00:00Z) · last seen cycle 1 (2026-09-21T12:00:00Z) · 1 occurrence(s) · **open** · topic `competition`

Persistence (null model): 0 scored forecast(s); 3 required before a rank means anything.  It is excluded from the ranked table rather than shown at 0%, because a persona that has not been scored has not been beaten.

**Reproduce:** `python3 -c "import json;print(json.load(open('data/leaderboard.json'))['qualification'])"`

### `IRR-009` — Source arxiv has never been read

*INFO* · first seen cycle 1 (2026-09-21T12:00:00Z) · last seen cycle 1 (2026-09-21T12:00:00Z) · 1 occurrence(s) · **open** · source `arxiv`

arXiv API (arXiv (Cornell University)) is registered with a documentation URL but no successful read has been recorded yet. No claim has been built from it. The next probe will either verify it or record why it failed.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results=1'`

### `IRR-010` — Source pubmed has never been read

*INFO* · first seen cycle 1 (2026-09-21T12:00:00Z) · last seen cycle 1 (2026-09-21T12:00:00Z) · 1 occurrence(s) · **open** · source `pubmed`

NCBI PubMed E-utilities (U.S. National Library of Medicine) is registered with a documentation URL but no successful read has been recorded yet. No claim has been built from it. The next probe will either verify it or record why it failed.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=artificial+intelligence&retmax=1&retmode=json'`

### `IRR-011` — Source clinicaltrials has never been read

*INFO* · first seen cycle 1 (2026-09-21T12:00:00Z) · last seen cycle 1 (2026-09-21T12:00:00Z) · 1 occurrence(s) · **open** · source `clinicaltrials`

ClinicalTrials.gov API v2 (U.S. National Library of Medicine) is registered with a documentation URL but no successful read has been recorded yet. No claim has been built from it. The next probe will either verify it or record why it failed.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://clinicaltrials.gov/api/v2/studies?pageSize=1'`

### `IRR-012` — Source openalex has never been read

*INFO* · first seen cycle 1 (2026-09-21T12:00:00Z) · last seen cycle 1 (2026-09-21T12:00:00Z) · 1 occurrence(s) · **open** · source `openalex`

OpenAlex scholarly graph (OurResearch (open catalogue of scholarly works)) is registered with a documentation URL but no successful read has been recorded yet. No claim has been built from it. The next probe will either verify it or record why it failed.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://api.openalex.org/works?sort=publication_date:desc&per-page=1'`

### `IRR-013` — Source crossref has never been read

*INFO* · first seen cycle 1 (2026-09-21T12:00:00Z) · last seen cycle 1 (2026-09-21T12:00:00Z) · 1 occurrence(s) · **open** · source `crossref`

Crossref REST API (Crossref) is registered with a documentation URL but no successful read has been recorded yet. No claim has been built from it. The next probe will either verify it or record why it failed.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://api.crossref.org/works?rows=1&sort=created&order=desc'`

### `IRR-014` — Source stackexchange has never been read

*INFO* · first seen cycle 1 (2026-09-21T12:00:00Z) · last seen cycle 1 (2026-09-21T12:00:00Z) · 1 occurrence(s) · **open** · source `stackexchange`

Stack Exchange API 2.3 (Stack Exchange, Inc.) is registered with a documentation URL but no successful read has been recorded yet. No claim has been built from it. The next probe will either verify it or record why it failed.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://api.stackexchange.com/2.3/questions?order=desc&sort=votes&site=stackoverflow&pagesize=1'`

### `IRR-015` — Source huggingface has never been read

*INFO* · first seen cycle 1 (2026-09-21T12:00:00Z) · last seen cycle 1 (2026-09-21T12:00:00Z) · 1 occurrence(s) · **open** · source `huggingface`

Hugging Face Hub API (Hugging Face, Inc.) is registered with a documentation URL but no successful read has been recorded yet. No claim has been built from it. The next probe will either verify it or record why it failed.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://huggingface.co/api/models?sort=trendingScore&limit=1'`

### `IRR-016` — Source nws_alerts has never been read

*INFO* · first seen cycle 1 (2026-09-21T12:00:00Z) · last seen cycle 1 (2026-09-21T12:00:00Z) · 1 occurrence(s) · **open** · source `nws_alerts`

api.weather.gov — active alerts (U.S. National Weather Service (NOAA)) is registered with a documentation URL but no successful read has been recorded yet. No claim has been built from it. The next probe will either verify it or record why it failed.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://api.weather.gov/alerts/active?area=CA'`

### `IRR-017` — Source worldbank has never been read

*INFO* · first seen cycle 1 (2026-09-21T12:00:00Z) · last seen cycle 1 (2026-09-21T12:00:00Z) · 1 occurrence(s) · **open** · source `worldbank`

World Bank Open Data API (The World Bank) is registered with a documentation URL but no successful read has been recorded yet. No claim has been built from it. The next probe will either verify it or record why it failed.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://api.worldbank.org/v2/country/USA/indicator/NY.GDP.MKTP.CD?format=json&per_page=1'`

### `IRR-018` — Source ecb_sdmx has never been read

*INFO* · first seen cycle 1 (2026-09-21T12:00:00Z) · last seen cycle 1 (2026-09-21T12:00:00Z) · 1 occurrence(s) · **open** · source `ecb_sdmx`

ECB Data Portal — SDMX REST (EXR daily) (European Central Bank) is registered with a documentation URL but no successful read has been recorded yet. No claim has been built from it. The next probe will either verify it or record why it failed.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A?lastNObservations=1&format=jsondata'`

### `IRR-019` — Source frankfurter has never been read

*INFO* · first seen cycle 1 (2026-09-21T12:00:00Z) · last seen cycle 1 (2026-09-21T12:00:00Z) · 1 occurrence(s) · **open** · source `frankfurter`

Frankfurter FX (ECB reference rates mirror) (Community service publishing ECB reference rates) is registered with a documentation URL but no successful read has been recorded yet. No claim has been built from it. The next probe will either verify it or record why it failed.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://api.frankfurter.app/latest?from=USD&to=EUR,KRW'`

### `IRR-020` — Source sec_edgar has never been read

*INFO* · first seen cycle 1 (2026-09-21T12:00:00Z) · last seen cycle 1 (2026-09-21T12:00:00Z) · 1 occurrence(s) · **open** · source `sec_edgar`

SEC EDGAR — company submissions (U.S. Securities and Exchange Commission) is registered with a documentation URL but no successful read has been recorded yet. No claim has been built from it. The next probe will either verify it or record why it failed.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://data.sec.gov/submissions/CIK0000320193.json'`

### `IRR-021` — Source census_acs has never been read

*INFO* · first seen cycle 1 (2026-09-21T12:00:00Z) · last seen cycle 1 (2026-09-21T12:00:00Z) · 1 occurrence(s) · **open** · source `census_acs`

U.S. Census Bureau API (ACS 5-year) (U.S. Census Bureau) is registered with a documentation URL but no successful read has been recorded yet. No claim has been built from it. The next probe will either verify it or record why it failed.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://api.census.gov/data/2022/acs/acs5?get=NAME,B01001_001E&for=state:06'`

### `IRR-022` — Source bls has never been read

*INFO* · first seen cycle 1 (2026-09-21T12:00:00Z) · last seen cycle 1 (2026-09-21T12:00:00Z) · 1 occurrence(s) · **open** · source `bls`

U.S. Bureau of Labor Statistics Public Data API v2 (U.S. Bureau of Labor Statistics) is registered with a documentation URL but no successful read has been recorded yet. No claim has been built from it. The next probe will either verify it or record why it failed.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://api.bls.gov/publicAPI/v2/timeseries/data/CUUR0000SA0'`

### `IRR-023` — Source nominatim has never been read

*INFO* · first seen cycle 1 (2026-09-21T12:00:00Z) · last seen cycle 1 (2026-09-21T12:00:00Z) · 1 occurrence(s) · **open** · source `nominatim`

OpenStreetMap Nominatim (OpenStreetMap Foundation) is registered with a documentation URL but no successful read has been recorded yet. No claim has been built from it. The next probe will either verify it or record why it failed.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://nominatim.openstreetmap.org/search?q=Seoul&format=json&limit=1'`

### `IRR-024` — Source europepmc has never been read

*INFO* · first seen cycle 1 (2026-09-21T12:00:00Z) · last seen cycle 1 (2026-09-21T12:00:00Z) · 1 occurrence(s) · **open** · source `europepmc`

Europe PMC REST (European Molecular Biology Laboratory) is registered with a documentation URL but no successful read has been recorded yet. No claim has been built from it. The next probe will either verify it or record why it failed.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=artificial+intelligence&format=json&pageSize=1'`

### `IRR-025` — Source kalshi_public has never been read

*INFO* · first seen cycle 1 (2026-09-21T12:00:00Z) · last seen cycle 1 (2026-09-21T12:00:00Z) · 1 occurrence(s) · **open** · source `kalshi_public`

Kalshi public market data (KalshiEX LLC) is registered with a documentation URL but no successful read has been recorded yet. No claim has been built from it. The next probe will either verify it or record why it failed.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://api.elections.kalshi.com/trade-api/v2/markets?limit=1'`

### `IRR-026` — Source mlb_statsapi has never been read

*INFO* · first seen cycle 1 (2026-09-21T12:00:00Z) · last seen cycle 1 (2026-09-21T12:00:00Z) · 1 occurrence(s) · **open** · source `mlb_statsapi`

MLB StatsAPI — schedule (Major League Baseball Advanced Media) is registered with a documentation URL but no successful read has been recorded yet. No claim has been built from it. The next probe will either verify it or record why it failed.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=2026-09-20'`

### `IRR-027` — mlb_statsapi is an undocumented public endpoint

*INFO* · first seen cycle 1 (2026-09-21T12:00:00Z) · last seen cycle 1 (2026-09-21T12:00:00Z) · 1 occurrence(s) · **open** · standing · source `mlb_statsapi`

No official public documentation page has been located for this endpoint.  Registered as UNDOCUMENTED so the irregularity register keeps it visible rather than the site implying a contract exists.  Claims built from it carry the same marker.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=2026-09-20'`

### `IRR-028` — Source nhl_web has never been read

*INFO* · first seen cycle 1 (2026-09-21T12:00:00Z) · last seen cycle 1 (2026-09-21T12:00:00Z) · 1 occurrence(s) · **open** · source `nhl_web`

NHL public web API — scoreboard (National Hockey League) is registered with a documentation URL but no successful read has been recorded yet. No claim has been built from it. The next probe will either verify it or record why it failed.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://api-web.nhle.com/v1/scoreboard/now'`

### `IRR-029` — nhl_web is an undocumented public endpoint

*INFO* · first seen cycle 1 (2026-09-21T12:00:00Z) · last seen cycle 1 (2026-09-21T12:00:00Z) · 1 occurrence(s) · **open** · standing · source `nhl_web`

UNDOCUMENTED public endpoint; no official contract page located.  See IRR-009.  Claims built from it carry the same marker.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://api-web.nhle.com/v1/scoreboard/now'`

### `IRR-030` — Source nba_cdn has never been read

*INFO* · first seen cycle 1 (2026-09-21T12:00:00Z) · last seen cycle 1 (2026-09-21T12:00:00Z) · 1 occurrence(s) · **open** · source `nba_cdn`

NBA CDN — today's scoreboard (National Basketball Association) is registered with a documentation URL but no successful read has been recorded yet. No claim has been built from it. The next probe will either verify it or record why it failed.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json'`

### `IRR-031` — nba_cdn is an undocumented public endpoint

*INFO* · first seen cycle 1 (2026-09-21T12:00:00Z) · last seen cycle 1 (2026-09-21T12:00:00Z) · 1 occurrence(s) · **open** · standing · source `nba_cdn`

UNDOCUMENTED public endpoint; no official contract page located.  See IRR-009.  Claims built from it carry the same marker.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json'`

### `IRR-038` — Six useful sources are excluded because they need an API key

*INFO* · first seen cycle 1 (2026-09-21T12:00:00Z) · last seen cycle 1 (2026-09-21T12:00:00Z) · 1 occurrence(s) · **open** · standing

FRED, the NFL Game API, Google Trends, the X API, the YouTube Data API and the TikTok/Instagram APIs were all rejected. Obtaining a key is manual input, which the brief rules out. Each is listed with the reason in msl/sources.py → KEYED_SOURCES_EXCLUDED so the omission is a decision on the record, not a gap.

**Reproduce:** `python3 -c "import msl.sources as s; [print(x['id'], x['reason']) for x in s.KEYED_SOURCES_EXCLUDED]"`

### `IRR-039` — Three sports feeds are undocumented public endpoints

*INFO* · first seen cycle 1 (2026-09-21T12:00:00Z) · last seen cycle 1 (2026-09-21T12:00:00Z) · 1 occurrence(s) · **open** · standing · topic `sports-signals`

statsapi.mlb.com, api-web.nhle.com and cdn.nba.com are the leagues' own hosts and the same feeds the owner's sibling labs already read, but no official public documentation page was located for any of them. They are registered with an explicit UNDOCUMENTED marker, and any claim built from one carries that marker too, so nothing on the site implies a contract exists.

**Reproduce:** `grep -n 'UNDOCUMENTED' msl/sources.py`

### `IRR-040` — Frankfurter is not an official ECB endpoint

*INFO* · first seen cycle 1 (2026-09-21T12:00:00Z) · last seen cycle 1 (2026-09-21T12:00:00Z) · 1 occurrence(s) · **open** · standing · source `frankfurter` · topic `macro-signals`

frankfurter.app republishes ECB euro reference rates but is a community service. It is registered as a redundancy check against the official ECB SDMX route, and every claim it produces is labelled third-party in the statement text itself, so it can never be quoted as an ECB figure.

**Reproduce:** `grep -n 'third-party' msl/adapters.py | head`

### `IRR-041` — The reasoning stage contains no language model

*INFO* · first seen cycle 1 (2026-09-21T12:00:00Z) · last seen cycle 1 (2026-09-21T12:00:00Z) · 1 occurrence(s) · **open** · standing

Every sentence published by this project is a template whose slots are filled from claim values, and every idea comes from a fixed rule set over the verified ledger. That is a deliberate limitation: it makes the output reproducible and auditable at the cost of novelty. A model with an API key would need a secret, and adding a secret is manual input. See METHODOLOGY.md §3.

**Reproduce:** `grep -rn 'openai\|anthropic\|llm_client' msl/ || echo 'no model client present'`

### `IRR-042` — Seed captures taken by an interactive read are not wire-hash verifiable

*INFO* · first seen cycle 1 (2026-09-21T12:00:00Z) · last seen cycle 1 (2026-09-21T12:00:00Z) · 1 occurrence(s) · **open** · standing

The first captures for wikimedia_pageviews, federal_register, usgs_fdsn and hn_firebase were read through an interactive agent fetch rather than by this process, so the stored SHA-256 covers the recorded body and not the bytes on the wire. Those evidence rows carry wireHashVerifiable=false, and the first automated probe re-reads each endpoint and reports whether the values still match.

**Reproduce:** `python3 -c "import json;[print(json.loads(l)['id'], json.loads(l)['wireHashVerifiable']) for l in open('data/evidence.jsonl') if not json.loads(l)['wireHashVerifiable']]"`

