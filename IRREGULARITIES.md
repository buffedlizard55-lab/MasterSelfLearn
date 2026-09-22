# IRREGULARITIES

Generated `2026-09-22T04:30:49Z` at cycle 14.

104 registered — 3 critical,
60 warn, 41 info.
29 open, 75 resolved,
15 standing.

**Standing** entries are structural limits of this project, not transient
failures: they do not auto-resolve, because the owner needs to keep seeing them.
A non-standing entry that stops recurring is marked `resolved` rather than
deleted, so the register keeps its history.

---

## CRITICAL (3)

### `IRR-086` — federal_register could not be read

*CRITICAL* · first seen cycle 10 (2026-09-22T03:50:22Z) · last seen cycle 10 (2026-09-22T03:50:22Z) · 4 occurrence(s) · **resolved** · source `federal_register` · topic `ai-research-frontier`

EgressBlocked: TLS/SSL connection has been closed (EOF) (_ssl.c:992) on GET https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=transformer after 3 attempt(s). No claim was produced and no substitute value was invented.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=reasoning'`

### `IRR-093` — federal_register could not be read

*CRITICAL* · first seen cycle 10 (2026-09-22T03:50:22Z) · last seen cycle 10 (2026-09-22T03:50:22Z) · 4 occurrence(s) · **resolved** · source `federal_register` · topic `regulatory-flow`

EgressBlocked: TLS/SSL connection has been closed (EOF) (_ssl.c:992) on GET https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=security after 3 attempt(s). No claim was produced and no substitute value was invented.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=artificial%20intelligence'`

### `IRR-098` — federal_register could not be read

*CRITICAL* · first seen cycle 10 (2026-09-22T03:50:22Z) · last seen cycle 10 (2026-09-22T03:50:22Z) · 3 occurrence(s) · **resolved** · source `federal_register` · topic `public-health-policy`

EgressBlocked: TLS/SSL connection has been closed (EOF) (_ssl.c:992) on GET https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=data%20exchange after 3 attempt(s). No claim was produced and no substitute value was invented.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=public%20health'`


## WARN (60)

### `IRR-033` — The owner's source document could not be read by a machine

*WARN* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 14 (2026-09-22T04:30:49Z) · 14 occurrence(s) · **open** · standing · topic `owner-corpus`

The brief points at a shared ChatGPT transcript (https://chatgpt.com/share/6ab1612a-2f14-83e8-9de6-808d21a48e53). A GET of that URL returns an HTML shell whose body is rendered client-side; the only server-supplied content is the <title>, “Design Autonomous Research System”. No requirement in this repository is sourced from that transcript. The design was derived instead from the written brief and from the owner's own published corpus, which is readable. If the transcript contains requirements that are missing here, they are missing.

**Reproduce:** `curl -s https://chatgpt.com/share/6ab1612a-2f14-83e8-9de6-808d21a48e53 | grep -o '<title>[^<]*'`

### `IRR-034` — GitHub publishes no trending API

*WARN* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 14 (2026-09-22T04:30:49Z) · 14 occurrence(s) · **open** · standing · source `github_search` · topic `open-source-momentum`

The obvious “trending repositories” signal has no official endpoint: https://github.com/trending returns HTML only, and GitHub's REST API exposes no trending route. The engine substitutes the official Search API sorted by stars over a created:>= window, which is reproducible and documented, and says so wherever the number appears. A trending *page* is a curated list with an undisclosed ranking; a search result is not, and the two are not equivalent.

**Reproduce:** `curl -s -o /dev/null -w '%{http_code} %{content_type}\n' https://github.com/trending`

### `IRR-035` — npm's documented media type is rejected by its own dist-tags endpoint

*WARN* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 14 (2026-09-22T04:30:49Z) · 14 occurrence(s) · **open** · standing · source `npm_registry` · topic `open-source-momentum`

GET https://registry.npmjs.org/-/package/next/dist-tags answers 200 for Accept: application/json and HTTP 406 Not Acceptable for Accept: application/vnd.npm.install-v1+json — the media type the registry documents for package metadata. Observed 2026-09-21 from two independent hosts. The engine therefore sends Accept: application/json for this route. This is recorded rather than quietly worked around so the next reader does not rediscover it.

**Reproduce:** `curl -s -o /dev/null -w '%{http_code}\n' -H 'Accept: application/vnd.npm.install-v1+json' https://registry.npmjs.org/-/package/next/dist-tags   # -> 406`

### `IRR-036` — Three interest categories have no registered source that can serve them

*WARN* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 14 (2026-09-22T04:30:49Z) · 14 occurrence(s) · **open** · standing · topic `travel-korea`

Travel & Korea Trip, Social & Creator Data, Elections & Civic Data, Gaming & Guides appear in the owner's verified corpus (https://buffedlizard55-lab.github.io/MasterSite/), but no official keyless API is registered that can answer their questions, so no claim is made about any of them. Per category: • Travel & Korea Trip: No official keyless API for hotel pricing or airfare is registered.  nominatim can place-geocode but cannot price anything. • Social & Creator Data: Every official creator API is keyed (see KEYED_SOURCES_EXCLUDED).  No verified signal exists, so no claim is made about this category. • Elections & Civic Data: federal_register covers federal rulemaking, but the FEC API needs a key for most endpoints and state results are per-jurisdiction.  Partial coverage only. • Gaming & Guides: The owner's master directory (https://buffedlizard55-lab.github.io/MasterSite/) publishes this category, but no source serving it is registered and no candidate endpoint has been confirmed by a recorded live read from this project.  Keyless game-metadata endpoints exist but are undocumented, and registering one without a recorded read would be an unverified claim.  No claim is made about this category. See KEYED_SOURCES_EXCLUDED and INTEREST_CATEGORIES_WITHOUT_A_SOURCE in msl/sources.py and ROADMAP.md.

**Reproduce:** `python3 -c "import msl.sources as s; print(s.INTEREST_CATEGORIES_WITHOUT_A_SOURCE)"`

### `IRR-042` — Topics with no verified claims behind them

*WARN* · first seen cycle 3 (2026-09-22T01:34:57Z) · last seen cycle 14 (2026-09-22T04:30:49Z) · 12 occurrence(s) · **open** · topic `library`

73 tracked topic(s) were proposed at least two cycles ago and still have zero verified claims: agency:health-and-human-services-department, agency:securities-and-exchange-commission, agency:centers-for-disease-control-and-prevention, frdoc:2026-19271, repo:zai-org/zcode, frdoc:2026-19148, sf-local, repo:brayonpi/hexstellar, repo:shadcn-ui/lint, repo:hanyuanwang/livestream-agent-studio, repo:jtydhr88/screenwriting-skills, repo:nanako0129/sepia (+61 more).  They are listed as unsupported rather than described, and each will be retired after 96 cycles without a signal. If a topic matters, the fix is to register a source that can answer it — not to write prose about it.

**Reproduce:** `python3 -c "import json;[print(t['slug']) for t in json.load(open('data/library.json'))['topics'] if t['claims']==0]"`

### `IRR-043` — clinicaltrials could not be read

*WARN* · first seen cycle 4 (2026-09-22T01:39:14Z) · last seen cycle 14 (2026-09-22T04:30:49Z) · 8 occurrence(s) · **open** · source `clinicaltrials` · topic `source-health`

HTTPError: HTTP 403 Forbidden on GET https://clinicaltrials.gov/api/v2/studies?pageSize=1 after 3 attempt(s). No claim was produced and no substitute value was invented.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://clinicaltrials.gov/api/v2/studies?pageSize=1'`

### `IRR-044` — clinicaltrials rate-limited this cycle

*WARN* · first seen cycle 4 (2026-09-22T01:39:14Z) · last seen cycle 14 (2026-09-22T04:30:49Z) · 13 occurrence(s) · **open** · source `clinicaltrials`

HTTP 403 on https://clinicaltrials.gov/api/v2/studies?pageSize=1. The engine backs off rather than retrying, and produces no claim from this source this cycle.

**Reproduce:** `curl -sSI 'https://clinicaltrials.gov/api/v2/studies?pageSize=1' | head -5`

### `IRR-045` — ecb_sdmx payload shape problem

*WARN* · first seen cycle 4 (2026-09-22T01:39:14Z) · last seen cycle 14 (2026-09-22T04:30:49Z) · 7 occurrence(s) · **open** · source `ecb_sdmx` · topic `source-health`

ecb_sdmx: unexpected jsondata shape (KeyError: 'data')  Zero facts were taken from the affected part of the payload.

**Reproduce:** `curl -sS 'https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A?lastNObservations=1&format=jsondata' | head -c 400`

### `IRR-046` — sec_edgar could not be read

*WARN* · first seen cycle 4 (2026-09-22T01:39:14Z) · last seen cycle 14 (2026-09-22T04:30:49Z) · 8 occurrence(s) · **open** · source `sec_edgar` · topic `source-health`

HTTPError: HTTP 403 Forbidden on GET https://data.sec.gov/submissions/CIK0000320193.json after 3 attempt(s). No claim was produced and no substitute value was invented.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://data.sec.gov/submissions/CIK0000320193.json'`

### `IRR-047` — sec_edgar rate-limited this cycle

*WARN* · first seen cycle 4 (2026-09-22T01:39:14Z) · last seen cycle 14 (2026-09-22T04:30:49Z) · 7 occurrence(s) · **open** · source `sec_edgar`

HTTP 403 on https://data.sec.gov/submissions/CIK0000320193.json. The engine backs off rather than retrying, and produces no claim from this source this cycle.

**Reproduce:** `curl -sSI 'https://data.sec.gov/submissions/CIK0000320193.json' | head -5`

### `IRR-048` — nhl_web payload shape problem

*WARN* · first seen cycle 4 (2026-09-22T01:39:14Z) · last seen cycle 14 (2026-09-22T04:30:49Z) · 7 occurrence(s) · **open** · source `nhl_web` · topic `source-health`

nhl_web: games is not a list  Zero facts were taken from the affected part of the payload.

**Reproduce:** `curl -sS 'https://api-web.nhle.com/v1/scoreboard/now' | head -c 400`

### `IRR-049` — nba_cdn could not be read

*WARN* · first seen cycle 4 (2026-09-22T01:39:14Z) · last seen cycle 14 (2026-09-22T04:30:49Z) · 8 occurrence(s) · **open** · source `nba_cdn` · topic `source-health`

HTTPError: HTTP 403 Forbidden on GET https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json after 3 attempt(s). No claim was produced and no substitute value was invented.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json'`

### `IRR-050` — nba_cdn rate-limited this cycle

*WARN* · first seen cycle 4 (2026-09-22T01:39:14Z) · last seen cycle 14 (2026-09-22T04:30:49Z) · 7 occurrence(s) · **open** · source `nba_cdn`

HTTP 403 on https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json. The engine backs off rather than retrying, and produces no claim from this source this cycle.

**Reproduce:** `curl -sSI 'https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json' | head -5`

### `IRR-051` — ecb_sdmx payload shape problem

*WARN* · first seen cycle 4 (2026-09-22T01:39:14Z) · last seen cycle 14 (2026-09-22T04:30:49Z) · 7 occurrence(s) · **open** · source `ecb_sdmx` · topic `macro-signals`

ecb_sdmx: unexpected jsondata shape (KeyError: 'data')  Zero facts were taken from the affected part of the payload.

**Reproduce:** `curl -sS 'https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A?lastNObservations=3&format=jsondata' | head -c 400`

### `IRR-057` — github_search could not be read

*WARN* · first seen cycle 6 (2026-09-22T01:47:08Z) · last seen cycle 14 (2026-09-22T04:30:49Z) · 5 occurrence(s) · **open** · source `github_search` · topic `open-source-momentum`

HTTPError: HTTP 403 rate limit exceeded on GET https://api.github.com/search/repositories?q=repo%3Ashadcn-ui/lint&sort=stars&order=desc&per_page=1 after 3 attempt(s). No claim was produced and no substitute value was invented.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://api.github.com/search/repositories?q=repo%3AHanyuanWang/LiveStream-Agent-Studio&sort=stars&order=desc&per_page=1'`

### `IRR-058` — github_search rate-limited this cycle

*WARN* · first seen cycle 6 (2026-09-22T01:47:08Z) · last seen cycle 14 (2026-09-22T04:30:49Z) · 5 occurrence(s) · **open** · source `github_search`

HTTP 403 on https://api.github.com/search/repositories?q=repo%3Ashadcn-ui/lint&sort=stars&order=desc&per_page=1. The engine backs off rather than retrying, and produces no claim from this source this cycle.

**Reproduce:** `curl -sSI 'https://api.github.com/search/repositories?q=repo%3AHanyuanWang/LiveStream-Agent-Studio&sort=stars&order=desc&per_page=1' | head -5`

### `IRR-060` — Retracted: wiki[artificial_intelligence]

*WARN* · first seen cycle 8 (2026-09-22T01:57:26Z) · last seen cycle 14 (2026-09-22T04:30:49Z) · 14 occurrence(s) · **open** · standing

3 claim(s) in the append-only ledger match this retracted field prefix and are no longer published or reasoned from. Derived from retracted pageview claims for the lowercased slug, so the trend describes the wrong page.  Recomputed from the canonical title instead. Superseded by `trend[wiki:Artificial_intelligence]`. The rows are kept, with their hashes, because the ledger is a record and not a view; deleting them would make the original error unauditable. First seen cycle 5, corrected in cycle 7.

**Reproduce:** `grep -n 'wiki[artificial_intelligence]' data/claims.jsonl | head`

### `IRR-104` — 4 of 70 planned reads failed

*WARN* · first seen cycle 14 (2026-09-22T04:30:49Z) · last seen cycle 14 (2026-09-22T04:30:49Z) · 1 occurrence(s) · **open**

4 read(s) failed while 66 succeeded. Each failure is listed separately with its HTTP status or transport error and a reproduction command. A partial cycle is still published, but every figure that would have come from a failed source is absent rather than carried forward silently.

**Reproduce:** `python3 tools/probe_sources.py`

### `IRR-052` — clinicaltrials could not be read

*WARN* · first seen cycle 4 (2026-09-22T01:39:14Z) · last seen cycle 13 (2026-09-22T04:15:17Z) · 7 occurrence(s) · **resolved** · source `clinicaltrials` · topic `clinical-evidence`

HTTPError: HTTP 403 Forbidden on GET https://clinicaltrials.gov/api/v2/studies?pageSize=5 after 3 attempt(s). No claim was produced and no substitute value was invented.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://clinicaltrials.gov/api/v2/studies?pageSize=5'`

### `IRR-053` — mlb_statsapi could not be read

*WARN* · first seen cycle 4 (2026-09-22T01:39:14Z) · last seen cycle 13 (2026-09-22T04:15:17Z) · 7 occurrence(s) · **resolved** · source `mlb_statsapi` · topic `sports-signals`

HTTPError: HTTP 400 Bad Request on GET https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=20260915 after 3 attempt(s). No claim was produced and no substitute value was invented.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=20260915'`

### `IRR-059` — 6 of 70 planned reads failed

*WARN* · first seen cycle 6 (2026-09-22T01:47:08Z) · last seen cycle 13 (2026-09-22T04:15:17Z) · 4 occurrence(s) · **resolved**

6 read(s) failed while 64 succeeded. Each failure is listed separately with its HTTP status or transport error and a reproduction command. A partial cycle is still published, but every figure that would have come from a failed source is absent rather than carried forward silently.

**Reproduce:** `python3 tools/probe_sources.py`

### `IRR-065` — wikimedia_pageviews unreadable; seed capture substituted

*WARN* · first seen cycle 10 (2026-09-22T03:50:22Z) · last seen cycle 11 (2026-09-22T03:58:55Z) · 2 occurrence(s) · **resolved** · source `wikimedia_pageviews` · topic `source-health`

EgressBlocked: TLS/SSL connection has been closed (EOF) (_ssl.c:992) on GET https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/Artificial_intelligence/daily/20260914/20260920. The recorded seed capture from 2026-09-21T22:58:00Z was used instead so the cycle still produces claims, and every claim from it is marked captureMode=seed-fallback. This is a substitute, not a fresh read.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}' 'https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/Artificial_intelligence/daily/20260914/20260920'`

### `IRR-067` — usgs_fdsn unreadable; seed capture substituted

*WARN* · first seen cycle 10 (2026-09-22T03:50:22Z) · last seen cycle 11 (2026-09-22T03:58:55Z) · 2 occurrence(s) · **resolved** · source `usgs_fdsn` · topic `source-health`

EgressBlocked: TLS/SSL connection has been closed (EOF) (_ssl.c:992) on GET https://earthquake.usgs.gov/fdsnws/event/1/count?format=geojson&starttime=2026-09-14&minmagnitude=5.0. The recorded seed capture from 2026-09-21T22:56:00Z was used instead so the cycle still produces claims, and every claim from it is marked captureMode=seed-fallback. This is a substitute, not a fresh read.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}' 'https://earthquake.usgs.gov/fdsnws/event/1/count?format=geojson&starttime=2026-09-14&minmagnitude=5.0'`

### `IRR-068` — hn_firebase unreadable; seed capture substituted

*WARN* · first seen cycle 10 (2026-09-22T03:50:22Z) · last seen cycle 11 (2026-09-22T03:58:55Z) · 2 occurrence(s) · **resolved** · source `hn_firebase` · topic `source-health`

EgressBlocked: TLS/SSL connection has been closed (EOF) (_ssl.c:992) on GET https://hacker-news.firebaseio.com/v0/topstories.json. The recorded seed capture from 2026-09-21T22:48:00Z was used instead so the cycle still produces claims, and every claim from it is marked captureMode=seed-fallback. This is a substitute, not a fresh read.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}' 'https://hacker-news.firebaseio.com/v0/topstories.json'`

### `IRR-102` — 50 of 70 planned reads failed

*WARN* · first seen cycle 10 (2026-09-22T03:50:22Z) · last seen cycle 11 (2026-09-22T03:58:55Z) · 2 occurrence(s) · **resolved**

50 read(s) failed while 20 succeeded. Each failure is listed separately with its HTTP status or transport error and a reproduction command. A partial cycle is still published, but every figure that would have come from a failed source is absent rather than carried forward silently.

**Reproduce:** `python3 tools/probe_sources.py`

### `IRR-103` — This runner could not egress to some sources

*WARN* · first seen cycle 11 (2026-09-22T03:58:55Z) · last seen cycle 11 (2026-09-22T03:58:55Z) · 1 occurrence(s) · **resolved** · source `federal_register`

22 source(s) could not be reached because the TLS session was closed before any HTTP status arrived: federal_register, arxiv, pubmed, clinicaltrials, openalex, crossref, stackexchange, huggingface, nws_alerts, worldbank, ecb_sdmx, frankfurter, sec_edgar, census_acs, bls, nominatim, europepmc, kalshi_public, mlb_statsapi, nhl_web, nba_cdn, wikimedia_pageviews. Hosts: api-web.nhle.com, api.bls.gov, api.census.gov, api.crossref.org, api.elections.kalshi.com, api.frankfurter.app, api.openalex.org, api.stackexchange.com, api.weather.gov, api.worldbank.org, cdn.nba.com, clinicaltrials.gov, data-api.ecb.europa.eu, data.sec.gov, eutils.ncbi.nlm.nih.gov, export.arxiv.org, huggingface.co, nominatim.openstreetmap.org, statsapi.mlb.com, wikimedia.org, www.ebi.ac.uk, www.federalregister.gov. This is a property of the machine running the cycle, not of those services, so NONE of them is marked blocked and no claim is made that any of them is down. No claim was produced from them and no substitute value was invented. Some other host was read successfully in this same cycle, which is what distinguishes an egress allowlist from an outage.

**Reproduce:** `python3 tools/probe_sources.py federal_register arxiv pubmed clinicaltrials   # from a runner with unrestricted egress`

### `IRR-066` — federal_register could not be read

*WARN* · first seen cycle 10 (2026-09-22T03:50:22Z) · last seen cycle 10 (2026-09-22T03:50:22Z) · 1 occurrence(s) · **resolved** · source `federal_register` · topic `source-health`

EgressBlocked: TLS/SSL connection has been closed (EOF) (_ssl.c:992) on GET https://www.federalregister.gov/api/v1/documents.json?per_page=1&order=newest after 3 attempt(s). No claim was produced and no substitute value was invented.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://www.federalregister.gov/api/v1/documents.json?per_page=1&order=newest'`

### `IRR-069` — arxiv could not be read

*WARN* · first seen cycle 10 (2026-09-22T03:50:22Z) · last seen cycle 10 (2026-09-22T03:50:22Z) · 1 occurrence(s) · **resolved** · source `arxiv` · topic `source-health`

EgressBlocked: TLS/SSL connection has been closed (EOF) (_ssl.c:992) on GET https://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results=1 after 3 attempt(s). No claim was produced and no substitute value was invented.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results=1'`

### `IRR-070` — pubmed could not be read

*WARN* · first seen cycle 10 (2026-09-22T03:50:22Z) · last seen cycle 10 (2026-09-22T03:50:22Z) · 1 occurrence(s) · **resolved** · source `pubmed` · topic `source-health`

EgressBlocked: TLS/SSL connection has been closed (EOF) (_ssl.c:992) on GET https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=artificial+intelligence&retmax=1&retmode=json after 3 attempt(s). No claim was produced and no substitute value was invented.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=artificial+intelligence&retmax=1&retmode=json'`

### `IRR-071` — openalex could not be read

*WARN* · first seen cycle 10 (2026-09-22T03:50:22Z) · last seen cycle 10 (2026-09-22T03:50:22Z) · 1 occurrence(s) · **resolved** · source `openalex` · topic `source-health`

EgressBlocked: TLS/SSL connection has been closed (EOF) (_ssl.c:992) on GET https://api.openalex.org/works?sort=publication_date:desc&per-page=1 after 3 attempt(s). No claim was produced and no substitute value was invented.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://api.openalex.org/works?sort=publication_date:desc&per-page=1'`

### `IRR-072` — crossref could not be read

*WARN* · first seen cycle 10 (2026-09-22T03:50:22Z) · last seen cycle 10 (2026-09-22T03:50:22Z) · 1 occurrence(s) · **resolved** · source `crossref` · topic `source-health`

EgressBlocked: TLS/SSL connection has been closed (EOF) (_ssl.c:992) on GET https://api.crossref.org/works?rows=1&sort=created&order=desc after 3 attempt(s). No claim was produced and no substitute value was invented.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://api.crossref.org/works?rows=1&sort=created&order=desc'`

### `IRR-073` — stackexchange could not be read

*WARN* · first seen cycle 10 (2026-09-22T03:50:22Z) · last seen cycle 10 (2026-09-22T03:50:22Z) · 1 occurrence(s) · **resolved** · source `stackexchange` · topic `source-health`

EgressBlocked: TLS/SSL connection has been closed (EOF) (_ssl.c:992) on GET https://api.stackexchange.com/2.3/questions?order=desc&sort=votes&site=stackoverflow&pagesize=1 after 3 attempt(s). No claim was produced and no substitute value was invented.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://api.stackexchange.com/2.3/questions?order=desc&sort=votes&site=stackoverflow&pagesize=1'`

### `IRR-074` — huggingface could not be read

*WARN* · first seen cycle 10 (2026-09-22T03:50:22Z) · last seen cycle 10 (2026-09-22T03:50:22Z) · 1 occurrence(s) · **resolved** · source `huggingface` · topic `source-health`

EgressBlocked: TLS/SSL connection has been closed (EOF) (_ssl.c:992) on GET https://huggingface.co/api/models?sort=trendingScore&limit=1 after 3 attempt(s). No claim was produced and no substitute value was invented.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://huggingface.co/api/models?sort=trendingScore&limit=1'`

### `IRR-075` — nws_alerts could not be read

*WARN* · first seen cycle 10 (2026-09-22T03:50:22Z) · last seen cycle 10 (2026-09-22T03:50:22Z) · 1 occurrence(s) · **resolved** · source `nws_alerts` · topic `source-health`

EgressBlocked: TLS/SSL connection has been closed (EOF) (_ssl.c:992) on GET https://api.weather.gov/alerts/active?area=CA after 3 attempt(s). No claim was produced and no substitute value was invented.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://api.weather.gov/alerts/active?area=CA'`

### `IRR-076` — worldbank could not be read

*WARN* · first seen cycle 10 (2026-09-22T03:50:22Z) · last seen cycle 10 (2026-09-22T03:50:22Z) · 1 occurrence(s) · **resolved** · source `worldbank` · topic `source-health`

EgressBlocked: TLS/SSL connection has been closed (EOF) (_ssl.c:992) on GET https://api.worldbank.org/v2/country/USA/indicator/NY.GDP.MKTP.CD?format=json&per_page=1 after 3 attempt(s). No claim was produced and no substitute value was invented.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://api.worldbank.org/v2/country/USA/indicator/NY.GDP.MKTP.CD?format=json&per_page=1'`

### `IRR-077` — ecb_sdmx could not be read

*WARN* · first seen cycle 10 (2026-09-22T03:50:22Z) · last seen cycle 10 (2026-09-22T03:50:22Z) · 1 occurrence(s) · **resolved** · source `ecb_sdmx` · topic `source-health`

EgressBlocked: TLS/SSL connection has been closed (EOF) (_ssl.c:992) on GET https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A?lastNObservations=1&format=jsondata after 3 attempt(s). No claim was produced and no substitute value was invented.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A?lastNObservations=1&format=jsondata'`

### `IRR-078` — frankfurter could not be read

*WARN* · first seen cycle 10 (2026-09-22T03:50:22Z) · last seen cycle 10 (2026-09-22T03:50:22Z) · 1 occurrence(s) · **resolved** · source `frankfurter` · topic `source-health`

EgressBlocked: TLS/SSL connection has been closed (EOF) (_ssl.c:992) on GET https://api.frankfurter.app/latest?from=USD&to=EUR,KRW after 3 attempt(s). No claim was produced and no substitute value was invented.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://api.frankfurter.app/latest?from=USD&to=EUR,KRW'`

### `IRR-079` — census_acs could not be read

*WARN* · first seen cycle 10 (2026-09-22T03:50:22Z) · last seen cycle 10 (2026-09-22T03:50:22Z) · 1 occurrence(s) · **resolved** · source `census_acs` · topic `source-health`

EgressBlocked: TLS/SSL connection has been closed (EOF) (_ssl.c:992) on GET https://api.census.gov/data/2022/acs/acs5?get=NAME,B01001_001E&for=state:06 after 3 attempt(s). No claim was produced and no substitute value was invented.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://api.census.gov/data/2022/acs/acs5?get=NAME,B01001_001E&for=state:06'`

### `IRR-080` — bls could not be read

*WARN* · first seen cycle 10 (2026-09-22T03:50:22Z) · last seen cycle 10 (2026-09-22T03:50:22Z) · 1 occurrence(s) · **resolved** · source `bls` · topic `source-health`

EgressBlocked: TLS/SSL connection has been closed (EOF) (_ssl.c:992) on GET https://api.bls.gov/publicAPI/v2/timeseries/data/CUUR0000SA0 after 3 attempt(s). No claim was produced and no substitute value was invented.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://api.bls.gov/publicAPI/v2/timeseries/data/CUUR0000SA0'`

### `IRR-081` — nominatim could not be read

*WARN* · first seen cycle 10 (2026-09-22T03:50:22Z) · last seen cycle 10 (2026-09-22T03:50:22Z) · 1 occurrence(s) · **resolved** · source `nominatim` · topic `source-health`

EgressBlocked: TLS/SSL connection has been closed (EOF) (_ssl.c:992) on GET https://nominatim.openstreetmap.org/search?q=Seoul&format=json&limit=1 after 3 attempt(s). No claim was produced and no substitute value was invented.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://nominatim.openstreetmap.org/search?q=Seoul&format=json&limit=1'`

### `IRR-082` — europepmc could not be read

*WARN* · first seen cycle 10 (2026-09-22T03:50:22Z) · last seen cycle 10 (2026-09-22T03:50:22Z) · 1 occurrence(s) · **resolved** · source `europepmc` · topic `source-health`

EgressBlocked: TLS/SSL connection has been closed (EOF) (_ssl.c:992) on GET https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=artificial+intelligence&format=json&pageSize=1 after 3 attempt(s). No claim was produced and no substitute value was invented.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=artificial+intelligence&format=json&pageSize=1'`

### `IRR-083` — kalshi_public could not be read

*WARN* · first seen cycle 10 (2026-09-22T03:50:22Z) · last seen cycle 10 (2026-09-22T03:50:22Z) · 1 occurrence(s) · **resolved** · source `kalshi_public` · topic `source-health`

EgressBlocked: TLS/SSL connection has been closed (EOF) (_ssl.c:992) on GET https://api.elections.kalshi.com/trade-api/v2/markets?limit=1 after 3 attempt(s). No claim was produced and no substitute value was invented.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://api.elections.kalshi.com/trade-api/v2/markets?limit=1'`

### `IRR-084` — mlb_statsapi could not be read

*WARN* · first seen cycle 10 (2026-09-22T03:50:22Z) · last seen cycle 10 (2026-09-22T03:50:22Z) · 1 occurrence(s) · **resolved** · source `mlb_statsapi` · topic `source-health`

EgressBlocked: TLS/SSL connection has been closed (EOF) (_ssl.c:992) on GET https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=2026-09-20 after 3 attempt(s). No claim was produced and no substitute value was invented.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=2026-09-20'`

### `IRR-085` — nhl_web could not be read

*WARN* · first seen cycle 10 (2026-09-22T03:50:22Z) · last seen cycle 10 (2026-09-22T03:50:22Z) · 1 occurrence(s) · **resolved** · source `nhl_web` · topic `source-health`

EgressBlocked: TLS/SSL connection has been closed (EOF) (_ssl.c:992) on GET https://api-web.nhle.com/v1/scoreboard/now after 3 attempt(s). No claim was produced and no substitute value was invented.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://api-web.nhle.com/v1/scoreboard/now'`

### `IRR-087` — arxiv could not be read

*WARN* · first seen cycle 10 (2026-09-22T03:50:22Z) · last seen cycle 10 (2026-09-22T03:50:22Z) · 1 occurrence(s) · **resolved** · source `arxiv` · topic `ai-research-frontier`

EgressBlocked: TLS/SSL connection has been closed (EOF) (_ssl.c:992) on GET https://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results=8 after 3 attempt(s). No claim was produced and no substitute value was invented.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results=8'`

### `IRR-088` — openalex could not be read

*WARN* · first seen cycle 10 (2026-09-22T03:50:22Z) · last seen cycle 10 (2026-09-22T03:50:22Z) · 1 occurrence(s) · **resolved** · source `openalex` · topic `ai-research-frontier`

EgressBlocked: TLS/SSL connection has been closed (EOF) (_ssl.c:992) on GET https://api.openalex.org/works?sort=publication_date:desc&per-page=5&mailto=buffedlizard55@gmail.com after 3 attempt(s). No claim was produced and no substitute value was invented.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://api.openalex.org/works?sort=publication_date:desc&per-page=5&mailto=buffedlizard55@gmail.com'`

### `IRR-089` — crossref could not be read

*WARN* · first seen cycle 10 (2026-09-22T03:50:22Z) · last seen cycle 10 (2026-09-22T03:50:22Z) · 1 occurrence(s) · **resolved** · source `crossref` · topic `ai-research-frontier`

EgressBlocked: TLS/SSL connection has been closed (EOF) (_ssl.c:992) on GET https://api.crossref.org/works?rows=3&sort=created&order=desc&mailto=buffedlizard55@gmail.com after 3 attempt(s). No claim was produced and no substitute value was invented.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://api.crossref.org/works?rows=3&sort=created&order=desc&mailto=buffedlizard55@gmail.com'`

### `IRR-090` — europepmc could not be read

*WARN* · first seen cycle 10 (2026-09-22T03:50:22Z) · last seen cycle 10 (2026-09-22T03:50:22Z) · 1 occurrence(s) · **resolved** · source `europepmc` · topic `ai-research-frontier`

EgressBlocked: TLS/SSL connection has been closed (EOF) (_ssl.c:992) on GET https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=artificial+intelligence&format=json&pageSize=3 after 3 attempt(s). No claim was produced and no substitute value was invented.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=artificial+intelligence&format=json&pageSize=3'`

### `IRR-091` — huggingface could not be read

*WARN* · first seen cycle 10 (2026-09-22T03:50:22Z) · last seen cycle 10 (2026-09-22T03:50:22Z) · 1 occurrence(s) · **resolved** · source `huggingface` · topic `ai-research-frontier`

EgressBlocked: TLS/SSL connection has been closed (EOF) (_ssl.c:992) on GET https://huggingface.co/api/models?sort=trendingScore&limit=10 after 3 attempt(s). No claim was produced and no substitute value was invented.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://huggingface.co/api/models?sort=trendingScore&limit=10'`

### `IRR-092` — stackexchange could not be read

*WARN* · first seen cycle 10 (2026-09-22T03:50:22Z) · last seen cycle 10 (2026-09-22T03:50:22Z) · 1 occurrence(s) · **resolved** · source `stackexchange` · topic `open-source-momentum`

EgressBlocked: TLS/SSL connection has been closed (EOF) (_ssl.c:992) on GET https://api.stackexchange.com/2.3/questions?order=desc&sort=votes&site=stackoverflow&pagesize=5&tagged=python after 3 attempt(s). No claim was produced and no substitute value was invented.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://api.stackexchange.com/2.3/questions?order=desc&sort=votes&site=stackoverflow&pagesize=5&tagged=python'`

### `IRR-094` — worldbank could not be read

*WARN* · first seen cycle 10 (2026-09-22T03:50:22Z) · last seen cycle 10 (2026-09-22T03:50:22Z) · 1 occurrence(s) · **resolved** · source `worldbank` · topic `macro-signals`

EgressBlocked: TLS/SSL connection has been closed (EOF) (_ssl.c:992) on GET https://api.worldbank.org/v2/country/USA/indicator/NY.GDP.MKTP.CD?format=json&per_page=3 after 3 attempt(s). No claim was produced and no substitute value was invented.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://api.worldbank.org/v2/country/USA/indicator/NY.GDP.MKTP.CD?format=json&per_page=3'`

### `IRR-095` — ecb_sdmx could not be read

*WARN* · first seen cycle 10 (2026-09-22T03:50:22Z) · last seen cycle 10 (2026-09-22T03:50:22Z) · 1 occurrence(s) · **resolved** · source `ecb_sdmx` · topic `macro-signals`

EgressBlocked: TLS/SSL connection has been closed (EOF) (_ssl.c:992) on GET https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A?lastNObservations=3&format=jsondata after 3 attempt(s). No claim was produced and no substitute value was invented.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A?lastNObservations=3&format=jsondata'`

### `IRR-096` — frankfurter could not be read

*WARN* · first seen cycle 10 (2026-09-22T03:50:22Z) · last seen cycle 10 (2026-09-22T03:50:22Z) · 1 occurrence(s) · **resolved** · source `frankfurter` · topic `macro-signals`

EgressBlocked: TLS/SSL connection has been closed (EOF) (_ssl.c:992) on GET https://api.frankfurter.app/latest?from=USD&to=EUR,KRW,JPY after 3 attempt(s). No claim was produced and no substitute value was invented.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://api.frankfurter.app/latest?from=USD&to=EUR,KRW,JPY'`

### `IRR-097` — pubmed could not be read

*WARN* · first seen cycle 10 (2026-09-22T03:50:22Z) · last seen cycle 10 (2026-09-22T03:50:22Z) · 1 occurrence(s) · **resolved** · source `pubmed` · topic `clinical-evidence`

EgressBlocked: TLS/SSL connection has been closed (EOF) (_ssl.c:992) on GET https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=trial&retmax=1&retmode=json after 3 attempt(s). No claim was produced and no substitute value was invented.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=trial&retmax=1&retmode=json'`

### `IRR-099` — pubmed could not be read

*WARN* · first seen cycle 10 (2026-09-22T03:50:22Z) · last seen cycle 10 (2026-09-22T03:50:22Z) · 1 occurrence(s) · **resolved** · source `pubmed` · topic `public-health-policy`

EgressBlocked: TLS/SSL connection has been closed (EOF) (_ssl.c:992) on GET https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=cdc&retmax=1&retmode=json after 3 attempt(s). No claim was produced and no substitute value was invented.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=cdc&retmax=1&retmode=json'`

### `IRR-100` — kalshi_public could not be read

*WARN* · first seen cycle 10 (2026-09-22T03:50:22Z) · last seen cycle 10 (2026-09-22T03:50:22Z) · 1 occurrence(s) · **resolved** · source `kalshi_public` · topic `sports-signals`

EgressBlocked: TLS/SSL connection has been closed (EOF) (_ssl.c:992) on GET https://api.elections.kalshi.com/trade-api/v2/markets?limit=5 after 3 attempt(s). No claim was produced and no substitute value was invented.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://api.elections.kalshi.com/trade-api/v2/markets?limit=5'`

### `IRR-101` — wikimedia_pageviews could not be read

*WARN* · first seen cycle 10 (2026-09-22T03:50:22Z) · last seen cycle 10 (2026-09-22T03:50:22Z) · 1 occurrence(s) · **resolved** · source `wikimedia_pageviews` · topic `public-attention`

EgressBlocked: TLS/SSL connection has been closed (EOF) (_ssl.c:992) on GET https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/Artificial_intelligence/daily/20260909/20260915 after 3 attempt(s). No claim was produced and no substitute value was invented.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/Artificial_intelligence/daily/20260909/20260915'`

### `IRR-056` — europepmc payload shape problem

*WARN* · first seen cycle 5 (2026-09-22T01:41:22Z) · last seen cycle 8 (2026-09-22T01:57:26Z) · 2 occurrence(s) · **resolved** · source `europepmc` · topic `ai-research-frontier`

europepmc: hitCount missing  Zero facts were taken from the affected part of the payload.

**Reproduce:** `curl -sS 'https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=artificial+intelligence&format=json&pageSize=3' | head -c 400`

### `IRR-054` — 5 of 70 planned reads failed

*WARN* · first seen cycle 4 (2026-09-22T01:39:14Z) · last seen cycle 5 (2026-09-22T01:41:22Z) · 2 occurrence(s) · **resolved**

5 read(s) failed while 65 succeeded. Each failure is listed separately with its HTTP status or transport error and a reproduction command. A partial cycle is still published, but every figure that would have come from a failed source is absent rather than carried forward silently.

**Reproduce:** `python3 tools/probe_sources.py`

### `IRR-055` — europepmc payload shape problem

*WARN* · first seen cycle 5 (2026-09-22T01:41:22Z) · last seen cycle 5 (2026-09-22T01:41:22Z) · 1 occurrence(s) · **resolved** · source `europepmc` · topic `source-health`

europepmc: hitCount missing  Zero facts were taken from the affected part of the payload.

**Reproduce:** `curl -sS 'https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=artificial+intelligence&format=json&pageSize=1' | head -c 400`


## INFO (41)

### `IRR-002` — Some derived claims cannot be re-checked

*INFO* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 14 (2026-09-22T04:30:49Z) · 14 occurrence(s) · **open** · standing · topic `derived`

244 derived claim(s) use a formula whose value depends on the wall clock at read time — a repository's stars-per-day, for example, has 'now' in its denominator. They are counted as NOT RECHECKED rather than as passing, because a check that cannot be repeated is not a check.

**Reproduce:** `python3 -m msl.cli verify-claims`

### `IRR-022` — Source census_acs has never been read

*INFO* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 14 (2026-09-22T04:30:49Z) · 13 occurrence(s) · **open** · source `census_acs`

U.S. Census Bureau API (ACS 5-year) (U.S. Census Bureau) is registered with a documentation URL but no successful read has been recorded yet. No claim has been built from it. The next probe will either verify it or record why it failed.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://api.census.gov/data/2022/acs/acs5?get=NAME,B01001_001E&for=state:06'`

### `IRR-028` — mlb_statsapi is an undocumented public endpoint

*INFO* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 14 (2026-09-22T04:30:49Z) · 14 occurrence(s) · **open** · standing · source `mlb_statsapi`

No official public documentation page has been located for this endpoint.  Registered as UNDOCUMENTED so the irregularity register keeps it visible rather than the site implying a contract exists.  Claims built from it carry the same marker.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=2026-09-20'`

### `IRR-030` — nhl_web is an undocumented public endpoint

*INFO* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 14 (2026-09-22T04:30:49Z) · 14 occurrence(s) · **open** · standing · source `nhl_web`

UNDOCUMENTED public endpoint; no official contract page located.  See IRR-009.  Claims built from it carry the same marker.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://api-web.nhle.com/v1/scoreboard/now'`

### `IRR-032` — nba_cdn is an undocumented public endpoint

*INFO* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 14 (2026-09-22T04:30:49Z) · 14 occurrence(s) · **open** · standing · source `nba_cdn`

UNDOCUMENTED public endpoint; no official contract page located.  See IRR-009.  Claims built from it carry the same marker.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json'`

### `IRR-037` — Six useful sources are excluded because they need an API key

*INFO* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 14 (2026-09-22T04:30:49Z) · 14 occurrence(s) · **open** · standing

FRED (St. Louis Fed) series observations, NFL Game API (api.nfl.com), Google Trends, X / Twitter API, YouTube Data API v3, TikTok / Instagram official APIs were all rejected. Obtaining a key is manual input, which the brief rules out. Each is listed with the reason in msl/sources.py → KEYED_SOURCES_EXCLUDED so the omission is a decision on the record, not a gap.

**Reproduce:** `python3 -c "import msl.sources as s; [print(x['id'], x['reason']) for x in s.KEYED_SOURCES_EXCLUDED]"`

### `IRR-038` — Three sports feeds are undocumented public endpoints

*INFO* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 14 (2026-09-22T04:30:49Z) · 14 occurrence(s) · **open** · standing · topic `sports-signals`

statsapi.mlb.com, api-web.nhle.com, cdn.nba.com are the leagues' own hosts and the same feeds the owner's sibling labs already read, but no official public documentation page was located for any of them. They are registered with an explicit UNDOCUMENTED marker, and any claim built from one carries that marker too, so nothing on the site implies a contract exists.

**Reproduce:** `grep -n 'UNDOCUMENTED' msl/sources.py`

### `IRR-039` — Frankfurter is not an official ECB endpoint

*INFO* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 14 (2026-09-22T04:30:49Z) · 14 occurrence(s) · **open** · standing · source `frankfurter` · topic `macro-signals`

frankfurter.app republishes ECB euro reference rates but is a community service. It is registered as a redundancy check against the official ECB SDMX route, and every claim it produces is labelled third-party in the statement text itself, so it can never be quoted as an ECB figure.

**Reproduce:** `grep -n 'third-party' msl/adapters.py | head`

### `IRR-040` — The reasoning stage contains no language model

*INFO* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 14 (2026-09-22T04:30:49Z) · 14 occurrence(s) · **open** · standing

Every sentence published by this project is a template whose slots are filled from claim values, and every idea comes from a fixed rule set over the verified ledger. That is a deliberate limitation: it makes the output reproducible and auditable at the cost of novelty. A model with an API key would need a secret, and adding a secret is manual input. See METHODOLOGY.md §3.

**Reproduce:** `grep -rn 'openai\|anthropic\|llm_client' msl/ || echo 'no model client present'`

### `IRR-041` — Seed captures taken by an interactive read are not wire-hash verifiable

*INFO* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 14 (2026-09-22T04:30:49Z) · 14 occurrence(s) · **open** · standing

The first captures for wikimedia_pageviews, federal_register, usgs_fdsn and hn_firebase were read through an interactive agent fetch rather than by this process, so the stored SHA-256 covers the recorded body and not the bytes on the wire. Those evidence rows carry wireHashVerifiable=false, and the first automated probe re-reads each endpoint and reports whether the values still match.

**Reproduce:** `python3 -c "import json;[print(json.loads(l)['id'], json.loads(l)['wireHashVerifiable']) for l in open('data/evidence.jsonl') if not json.loads(l)['wireHashVerifiable']]"`

### `IRR-010` — Source arxiv has never been read

*INFO* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 12 (2026-09-22T04:12:37Z) · 6 occurrence(s) · **resolved** · source `arxiv`

arXiv API (arXiv (Cornell University)) is registered with a documentation URL but no successful read has been recorded yet. No claim has been built from it. The next probe will either verify it or record why it failed.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results=1'`

### `IRR-011` — Source pubmed has never been read

*INFO* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 12 (2026-09-22T04:12:37Z) · 6 occurrence(s) · **resolved** · source `pubmed`

NCBI PubMed E-utilities (U.S. National Library of Medicine) is registered with a documentation URL but no successful read has been recorded yet. No claim has been built from it. The next probe will either verify it or record why it failed.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=artificial+intelligence&retmax=1&retmode=json'`

### `IRR-012` — Source clinicaltrials has never been read

*INFO* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 12 (2026-09-22T04:12:37Z) · 6 occurrence(s) · **resolved** · source `clinicaltrials`

ClinicalTrials.gov API v2 (U.S. National Library of Medicine) is registered with a documentation URL but no successful read has been recorded yet. No claim has been built from it. The next probe will either verify it or record why it failed.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://clinicaltrials.gov/api/v2/studies?pageSize=1'`

### `IRR-013` — Source openalex has never been read

*INFO* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 12 (2026-09-22T04:12:37Z) · 6 occurrence(s) · **resolved** · source `openalex`

OpenAlex scholarly graph (OurResearch (open catalogue of scholarly works)) is registered with a documentation URL but no successful read has been recorded yet. No claim has been built from it. The next probe will either verify it or record why it failed.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://api.openalex.org/works?sort=publication_date:desc&per-page=1'`

### `IRR-014` — Source crossref has never been read

*INFO* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 12 (2026-09-22T04:12:37Z) · 6 occurrence(s) · **resolved** · source `crossref`

Crossref REST API (Crossref) is registered with a documentation URL but no successful read has been recorded yet. No claim has been built from it. The next probe will either verify it or record why it failed.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://api.crossref.org/works?rows=1&sort=created&order=desc'`

### `IRR-015` — Source stackexchange has never been read

*INFO* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 12 (2026-09-22T04:12:37Z) · 6 occurrence(s) · **resolved** · source `stackexchange`

Stack Exchange API 2.3 (Stack Exchange, Inc.) is registered with a documentation URL but no successful read has been recorded yet. No claim has been built from it. The next probe will either verify it or record why it failed.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://api.stackexchange.com/2.3/questions?order=desc&sort=votes&site=stackoverflow&pagesize=1'`

### `IRR-016` — Source huggingface has never been read

*INFO* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 12 (2026-09-22T04:12:37Z) · 6 occurrence(s) · **resolved** · source `huggingface`

Hugging Face Hub API (Hugging Face, Inc.) is registered with a documentation URL but no successful read has been recorded yet. No claim has been built from it. The next probe will either verify it or record why it failed.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://huggingface.co/api/models?sort=trendingScore&limit=1'`

### `IRR-017` — Source nws_alerts has never been read

*INFO* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 12 (2026-09-22T04:12:37Z) · 6 occurrence(s) · **resolved** · source `nws_alerts`

api.weather.gov — active alerts (U.S. National Weather Service (NOAA)) is registered with a documentation URL but no successful read has been recorded yet. No claim has been built from it. The next probe will either verify it or record why it failed.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://api.weather.gov/alerts/active?area=CA'`

### `IRR-018` — Source worldbank has never been read

*INFO* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 12 (2026-09-22T04:12:37Z) · 6 occurrence(s) · **resolved** · source `worldbank`

World Bank Open Data API (The World Bank) is registered with a documentation URL but no successful read has been recorded yet. No claim has been built from it. The next probe will either verify it or record why it failed.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://api.worldbank.org/v2/country/USA/indicator/NY.GDP.MKTP.CD?format=json&per_page=1'`

### `IRR-019` — Source ecb_sdmx has never been read

*INFO* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 12 (2026-09-22T04:12:37Z) · 6 occurrence(s) · **resolved** · source `ecb_sdmx`

ECB Data Portal — SDMX REST (EXR daily) (European Central Bank) is registered with a documentation URL but no successful read has been recorded yet. No claim has been built from it. The next probe will either verify it or record why it failed.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A?lastNObservations=1&format=jsondata'`

### `IRR-020` — Source frankfurter has never been read

*INFO* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 12 (2026-09-22T04:12:37Z) · 6 occurrence(s) · **resolved** · source `frankfurter`

Frankfurter FX (ECB reference rates mirror) (Community service publishing ECB reference rates) is registered with a documentation URL but no successful read has been recorded yet. No claim has been built from it. The next probe will either verify it or record why it failed.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://api.frankfurter.app/latest?from=USD&to=EUR,KRW'`

### `IRR-021` — Source sec_edgar has never been read

*INFO* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 12 (2026-09-22T04:12:37Z) · 6 occurrence(s) · **resolved** · source `sec_edgar`

SEC EDGAR — company submissions (U.S. Securities and Exchange Commission) is registered with a documentation URL but no successful read has been recorded yet. No claim has been built from it. The next probe will either verify it or record why it failed.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://data.sec.gov/submissions/CIK0000320193.json'`

### `IRR-023` — Source bls has never been read

*INFO* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 12 (2026-09-22T04:12:37Z) · 6 occurrence(s) · **resolved** · source `bls`

U.S. Bureau of Labor Statistics Public Data API v2 (U.S. Bureau of Labor Statistics) is registered with a documentation URL but no successful read has been recorded yet. No claim has been built from it. The next probe will either verify it or record why it failed.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://api.bls.gov/publicAPI/v2/timeseries/data/CUUR0000SA0'`

### `IRR-024` — Source nominatim has never been read

*INFO* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 12 (2026-09-22T04:12:37Z) · 6 occurrence(s) · **resolved** · source `nominatim`

OpenStreetMap Nominatim (OpenStreetMap Foundation) is registered with a documentation URL but no successful read has been recorded yet. No claim has been built from it. The next probe will either verify it or record why it failed.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://nominatim.openstreetmap.org/search?q=Seoul&format=json&limit=1'`

### `IRR-025` — Source europepmc has never been read

*INFO* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 12 (2026-09-22T04:12:37Z) · 6 occurrence(s) · **resolved** · source `europepmc`

Europe PMC REST (European Molecular Biology Laboratory) is registered with a documentation URL but no successful read has been recorded yet. No claim has been built from it. The next probe will either verify it or record why it failed.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=artificial+intelligence&format=json&pageSize=1'`

### `IRR-026` — Source kalshi_public has never been read

*INFO* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 12 (2026-09-22T04:12:37Z) · 6 occurrence(s) · **resolved** · source `kalshi_public`

Kalshi public market data (KalshiEX LLC) is registered with a documentation URL but no successful read has been recorded yet. No claim has been built from it. The next probe will either verify it or record why it failed.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://api.elections.kalshi.com/trade-api/v2/markets?limit=1'`

### `IRR-027` — Source mlb_statsapi has never been read

*INFO* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 12 (2026-09-22T04:12:37Z) · 6 occurrence(s) · **resolved** · source `mlb_statsapi`

MLB StatsAPI — schedule (Major League Baseball Advanced Media) is registered with a documentation URL but no successful read has been recorded yet. No claim has been built from it. The next probe will either verify it or record why it failed.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=2026-09-20'`

### `IRR-029` — Source nhl_web has never been read

*INFO* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 12 (2026-09-22T04:12:37Z) · 6 occurrence(s) · **resolved** · source `nhl_web`

NHL public web API — scoreboard (National Hockey League) is registered with a documentation URL but no successful read has been recorded yet. No claim has been built from it. The next probe will either verify it or record why it failed.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://api-web.nhle.com/v1/scoreboard/now'`

### `IRR-031` — Source nba_cdn has never been read

*INFO* · first seen cycle 1 (2026-09-22T01:34:57Z) · last seen cycle 12 (2026-09-22T04:12:37Z) · 6 occurrence(s) · **resolved** · source `nba_cdn`

NBA CDN — today's scoreboard (National Basketball Association) is registered with a documentation URL but no successful read has been recorded yet. No claim has been built from it. The next probe will either verify it or record why it failed.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json'`

### `IRR-061` — Source wikimedia_pageviews has never been read

*INFO* · first seen cycle 9 (2026-09-22T03:49:52Z) · last seen cycle 12 (2026-09-22T04:12:37Z) · 3 occurrence(s) · **resolved** · source `wikimedia_pageviews`

Wikimedia Pageviews REST API (Wikimedia Foundation) is registered with a documentation URL but no successful read has been recorded yet. No claim has been built from it. The next probe will either verify it or record why it failed.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/Artificial_intelligence/daily/20260914/20260920'`

### `IRR-062` — Source federal_register has never been read

*INFO* · first seen cycle 9 (2026-09-22T03:49:52Z) · last seen cycle 12 (2026-09-22T04:12:37Z) · 3 occurrence(s) · **resolved** · source `federal_register`

Federal Register API v1 (U.S. National Archives / Office of the Federal Register) is registered with a documentation URL but no successful read has been recorded yet. No claim has been built from it. The next probe will either verify it or record why it failed.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://www.federalregister.gov/api/v1/documents.json?per_page=1&order=newest'`

### `IRR-063` — Source usgs_fdsn has never been read

*INFO* · first seen cycle 9 (2026-09-22T03:49:52Z) · last seen cycle 12 (2026-09-22T04:12:37Z) · 4 occurrence(s) · **resolved** · source `usgs_fdsn`

USGS Earthquake Hazards — FDSN event service (U.S. Geological Survey) is registered with a documentation URL but no successful read has been recorded yet. No claim has been built from it. The next probe will either verify it or record why it failed.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://earthquake.usgs.gov/fdsnws/event/1/count?format=geojson&starttime=2026-09-14&minmagnitude=5.0'`

### `IRR-064` — Source hn_firebase has never been read

*INFO* · first seen cycle 9 (2026-09-22T03:49:52Z) · last seen cycle 12 (2026-09-22T04:12:37Z) · 4 occurrence(s) · **resolved** · source `hn_firebase`

Hacker News official Firebase API (Hacker News / Y Combinator) is registered with a documentation URL but no successful read has been recorded yet. No claim has been built from it. The next probe will either verify it or record why it failed.

**Reproduce:** `curl -sS -o /dev/null -w '%{http_code}\n' 'https://hacker-news.firebaseio.com/v0/topstories.json'`

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

