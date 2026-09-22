# VERIFICATION — line-by-line audit ledger

Generated `2026-09-22T01:57:26Z` at cycle 8. Read-only verifiers:
`python3 -m msl.cli verify-claims` and `python3 tools/probe_sources.py`.

## 1. Claim ledger composition

| Kind | Count | What it means |
|---|---|---|
| `captured` | 4,564 | A value lifted from a payload this project read |
| `documented` | 0 | A value from the operator's own published record |
| `negative` | 0 | Proof that something does **not** exist |
| `derived` | 1,788 | Arithmetic over claims above, formula recorded |
| **Total accepted** | **6,352** | |
| Rejected by the gate | 0 | Published, not swallowed |

## 2. Source registry

28 sources. `status` is written only by the probe.

| # | Id | Name | Operator | Status | Live reads | Last read (UTC) | HTTP | Links |
|---|---|---|---|---|---|---|---|---|
| 1 | `arxiv` | arXiv API | arXiv (Cornell University) | `verified-live-read` | 2 | 2026-09-22T01:57:26Z | 200 | [docs](https://info.arxiv.org/help/api/index.html) · [probe](https://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results=1) |
| 2 | `bls` | U.S. Bureau of Labor Statistics Public Data API v2 | U.S. Bureau of Labor Statistics | `verified-live-read` | 1 | 2026-09-22T01:57:26Z | 200 | [docs](https://www.bls.gov/developers/home.htm) · [probe](https://api.bls.gov/publicAPI/v2/timeseries/data/CUUR0000SA0) |
| 3 | `census_acs` | U.S. Census Bureau API (ACS 5-year) | U.S. Census Bureau | `registered` | 0 | — | — | [docs](https://www.census.gov/data/developers/data-sets.html) · [probe](https://api.census.gov/data/2022/acs/acs5?get=NAME,B01001_001E&for=state:06) |
| 4 | `clinicaltrials` | ClinicalTrials.gov API v2 | U.S. National Library of Medicine | `blocked` | 0 | 2026-09-22T01:57:26Z | 403 | [docs](https://clinicaltrials.gov/data-api/api) · [probe](https://clinicaltrials.gov/api/v2/studies?pageSize=1) |
| 5 | `crossref` | Crossref REST API | Crossref | `verified-live-read` | 2 | 2026-09-22T01:57:26Z | 200 | [docs](https://www.crossref.org/documentation/retrieve-metadata/rest-api/) · [probe](https://api.crossref.org/works?rows=1&sort=created&order=desc) |
| 6 | `ecb_sdmx` | ECB Data Portal — SDMX REST (EXR daily) | European Central Bank | `verified-live-read` | 2 | 2026-09-22T01:57:26Z | 200 | [docs](https://data-explorer.ecb.europa.eu/) · [probe](https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A?lastNObservations=1&format=jsondata) |
| 7 | `europepmc` | Europe PMC REST | European Molecular Biology Laboratory | `verified-live-read` | 2 | 2026-09-22T01:57:26Z | 200 | [docs](https://europepmc.org/RestfulWebService) · [probe](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=artificial+intelligence&format=json&pageSize=1) |
| 8 | `federal_register` | Federal Register API v1 | U.S. National Archives / Office of the Federal Register | `verified-live-read` | 13 | 2026-09-22T01:57:26Z | 200 | [docs](https://www.federalregister.gov/developers/documentation/api/v1) · [probe](https://www.federalregister.gov/api/v1/documents.json?per_page=1&order=newest) |
| 9 | `frankfurter` | Frankfurter FX (ECB reference rates mirror) | Community service publishing ECB reference rates | `verified-live-read` | 2 | 2026-09-22T01:57:26Z | 200 | [docs](https://www.frankfurter.app/) · [probe](https://api.frankfurter.app/latest?from=USD&to=EUR,KRW) |
| 10 | `github_repos` | GitHub Repos API — owner corpus | GitHub, Inc. | `verified-live-read` | 4 | 2026-09-22T01:57:26Z | 200 | [docs](https://docs.github.com/en/rest/repos/repos) · [probe](https://api.github.com/users/buffedlizard55-lab/repos?per_page=1) |
| 11 | `github_search` | GitHub Search API — repositories | GitHub, Inc. | `verified-live-read` | 21 | 2026-09-22T01:57:26Z | 200 | [docs](https://docs.github.com/en/rest/search/search) · [probe](https://api.github.com/search/repositories?q=created:%3E=2026-09-14&sort=stars&order=desc&per_page=1) |
| 12 | `hn_firebase` | Hacker News official Firebase API | Hacker News / Y Combinator | `verified-live-read` | 2 | 2026-09-22T01:57:26Z | 200 | [docs](https://github.com/HackerNews/API) · [probe](https://hacker-news.firebaseio.com/v0/topstories.json) |
| 13 | `huggingface` | Hugging Face Hub API | Hugging Face, Inc. | `verified-live-read` | 2 | 2026-09-22T01:57:26Z | 200 | [docs](https://huggingface.co/docs/hub/api) · [probe](https://huggingface.co/api/models?sort=trendingScore&limit=1) |
| 14 | `kalshi_public` | Kalshi public market data | KalshiEX LLC | `verified-live-read` | 2 | 2026-09-22T01:57:26Z | 200 | [docs](https://trading-api.readme.io/reference/getmarkets) · [probe](https://api.elections.kalshi.com/trade-api/v2/markets?limit=1) |
| 15 | `mlb_statsapi` | MLB StatsAPI — schedule | Major League Baseball Advanced Media | `blocked` | 1 | 2026-09-22T01:57:26Z | 400 | [docs](https://statsapi.mlb.com/) · [probe](https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=2026-09-20) |
| 16 | `nba_cdn` | NBA CDN — today's scoreboard | National Basketball Association | `blocked` | 0 | 2026-09-22T01:57:26Z | 403 | [docs](https://cdn.nba.com/) · [probe](https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json) |
| 17 | `nhl_web` | NHL public web API — scoreboard | National Hockey League | `verified-live-read` | 1 | 2026-09-22T01:57:26Z | 200 | [docs](https://api-web.nhle.com/) · [probe](https://api-web.nhle.com/v1/scoreboard/now) |
| 18 | `nominatim` | OpenStreetMap Nominatim | OpenStreetMap Foundation | `verified-live-read` | 1 | 2026-09-22T01:57:26Z | 200 | [docs](https://nominatim.org/release-docs/latest/api/Search/) · [probe](https://nominatim.openstreetmap.org/search?q=Seoul&format=json&limit=1) |
| 19 | `npm_registry` | npm Registry — package metadata | GitHub, Inc. (npm) | `verified-live-read` | 3 | 2026-09-22T01:57:26Z | 200 | [docs](https://github.com/npm/registry) · [probe](https://registry.npmjs.org/next/latest) |
| 20 | `nws_alerts` | api.weather.gov — active alerts | U.S. National Weather Service (NOAA) | `verified-live-read` | 1 | 2026-09-22T01:57:26Z | 200 | [docs](https://www.weather.gov/documentation/services-web-api) · [probe](https://api.weather.gov/alerts/active?area=CA) |
| 21 | `openalex` | OpenAlex scholarly graph | OurResearch (open catalogue of scholarly works) | `verified-live-read` | 2 | 2026-09-22T01:57:26Z | 200 | [docs](https://docs.openalex.org/) · [probe](https://api.openalex.org/works?sort=publication_date:desc&per-page=1) |
| 22 | `pubmed` | NCBI PubMed E-utilities | U.S. National Library of Medicine | `verified-live-read` | 3 | 2026-09-22T01:57:26Z | 200 | [docs](https://www.ncbi.nlm.nih.gov/books/NBK25501/) · [probe](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=artificial+intelligence&retmax=1&retmode=json) |
| 23 | `pypi_json` | PyPI JSON API | Python Software Foundation | `verified-live-read` | 5 | 2026-09-22T01:57:26Z | 200 | [docs](https://docs.pypi.org/api/json/) · [probe](https://pypi.org/pypi/requests/json) |
| 24 | `sec_edgar` | SEC EDGAR — company submissions | U.S. Securities and Exchange Commission | `blocked` | 0 | 2026-09-22T01:57:26Z | 403 | [docs](https://www.sec.gov/edgar/sec-api-documentation) · [probe](https://data.sec.gov/submissions/CIK0000320193.json) |
| 25 | `stackexchange` | Stack Exchange API 2.3 | Stack Exchange, Inc. | `verified-live-read` | 2 | 2026-09-22T01:57:26Z | 200 | [docs](https://api.stackexchange.com/docs) · [probe](https://api.stackexchange.com/2.3/questions?order=desc&sort=votes&site=stackoverflow&pagesize=1) |
| 26 | `usgs_fdsn` | USGS Earthquake Hazards — FDSN event service | U.S. Geological Survey | `verified-live-read` | 2 | 2026-09-22T01:57:26Z | 200 | [docs](https://earthquake.usgs.gov/fdsnws/event/1/) · [probe](https://earthquake.usgs.gov/fdsnws/event/1/count?format=geojson&starttime=2026-09-14&minmagnitude=5.0) |
| 27 | `wikimedia_pageviews` | Wikimedia Pageviews REST API | Wikimedia Foundation | `verified-live-read` | 3 | 2026-09-22T01:57:26Z | 200 | [docs](https://wikimedia.org/api/rest_v1/) · [probe](https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/Artificial_intelligence/daily/20260914/20260920) |
| 28 | `worldbank` | World Bank Open Data API | The World Bank | `verified-live-read` | 2 | 2026-09-22T01:57:26Z | 200 | [docs](https://datahelpdesk.worldbank.org/knowledgebase/articles/889392) · [probe](https://api.worldbank.org/v2/country/USA/indicator/NY.GDP.MKTP.CD?format=json&per_page=1) |

## 3. Most recent evidence rows

Every row is one outbound read, with the hash of what came back.

| Id | Source | HTTP | Captured (UTC) | SHA-256 (16) | Bytes | Capture mode | Wire-hash verifiable | URL |
|---|---|---|---|---|---|---|---|---|
| `E000298` | `npm_registry` | 200 | 2026-09-22T01:57:26Z | `48b5968c14c5e882` | 0 | `pipeline` | yes | [open](https://registry.npmjs.org/next/latest) |
| `E000299` | `wikimedia_pageviews` | 200 | 2026-09-22T01:57:26Z | `e60a37eff2a9a9f2` | 0 | `pipeline` | yes | [open](https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/Artificial_intelligence/daily/20260914/20260920) |
| `E000300` | `federal_register` | 200 | 2026-09-22T01:57:26Z | `67230d2e1034fbd6` | 0 | `pipeline` | yes | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=1&order=newest) |
| `E000301` | `usgs_fdsn` | 200 | 2026-09-22T01:57:26Z | `5f59622eed5c328c` | 0 | `pipeline` | yes | [open](https://earthquake.usgs.gov/fdsnws/event/1/count?format=geojson&starttime=2026-09-14&minmagnitude=5.0) |
| `E000302` | `hn_firebase` | 200 | 2026-09-22T01:57:26Z | `436d9aad9fbe54d7` | 0 | `pipeline` | yes | [open](https://hacker-news.firebaseio.com/v0/topstories.json) |
| `E000303` | `arxiv` | 200 | 2026-09-22T01:57:26Z | `9ed5c1abb5d1b078` | 3,010 | `pipeline` | yes | [open](https://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results=1) |
| `E000304` | `pubmed` | 200 | 2026-09-22T01:57:26Z | `7eff792b526f7105` | 0 | `pipeline` | yes | [open](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=artificial+intelligence&retmax=1&retmode=json) |
| `E000305` | `openalex` | 200 | 2026-09-22T01:57:26Z | `66bacc1a93782ceb` | 0 | `pipeline` | yes | [open](https://api.openalex.org/works?sort=publication_date:desc&per-page=1) |
| `E000306` | `crossref` | 200 | 2026-09-22T01:57:26Z | `e41b9085074bcbcb` | 0 | `pipeline` | yes | [open](https://api.crossref.org/works?rows=1&sort=created&order=desc) |
| `E000307` | `stackexchange` | 200 | 2026-09-22T01:57:26Z | `cab73be8d63f4259` | 0 | `pipeline` | yes | [open](https://api.stackexchange.com/2.3/questions?order=desc&sort=votes&site=stackoverflow&pagesize=1) |
| `E000308` | `huggingface` | 200 | 2026-09-22T01:57:26Z | `a3f3ed09dfd88906` | 0 | `pipeline` | yes | [open](https://huggingface.co/api/models?sort=trendingScore&limit=1) |
| `E000309` | `nws_alerts` | 200 | 2026-09-22T01:57:26Z | `e00b34776a11dab2` | 0 | `pipeline` | yes | [open](https://api.weather.gov/alerts/active?area=CA) |
| `E000310` | `worldbank` | 200 | 2026-09-22T01:57:26Z | `57ee09ac4cf11069` | 0 | `pipeline` | yes | [open](https://api.worldbank.org/v2/country/USA/indicator/NY.GDP.MKTP.CD?format=json&per_page=1) |
| `E000311` | `ecb_sdmx` | 200 | 2026-09-22T01:57:26Z | `895d227179369f34` | 0 | `pipeline` | yes | [open](https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A?lastNObservations=1&format=jsondata) |
| `E000312` | `frankfurter` | 200 | 2026-09-22T01:57:26Z | `e79810a76ada8f34` | 0 | `pipeline` | yes | [open](https://api.frankfurter.app/latest?from=USD&to=EUR,KRW) |
| `E000313` | `bls` | 200 | 2026-09-22T01:57:26Z | `e6b8b7022a08b1e0` | 0 | `pipeline` | yes | [open](https://api.bls.gov/publicAPI/v2/timeseries/data/CUUR0000SA0) |
| `E000314` | `nominatim` | 200 | 2026-09-22T01:57:26Z | `3a9d9377688b65d2` | 0 | `pipeline` | yes | [open](https://nominatim.openstreetmap.org/search?q=Seoul&format=json&limit=1) |
| `E000315` | `europepmc` | 200 | 2026-09-22T01:57:26Z | `3f6a6e567cf53956` | 0 | `pipeline` | yes | [open](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=artificial+intelligence&format=json&pageSize=1) |
| `E000316` | `kalshi_public` | 200 | 2026-09-22T01:57:26Z | `ec52bb293e9b5e85` | 0 | `pipeline` | yes | [open](https://api.elections.kalshi.com/trade-api/v2/markets?limit=1) |
| `E000317` | `mlb_statsapi` | 200 | 2026-09-22T01:57:26Z | `380848368ace97b5` | 0 | `pipeline` | yes | [open](https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=2026-09-20) |
| `E000318` | `nhl_web` | 200 | 2026-09-22T01:57:26Z | `0d8c906dfd21a0d4` | 0 | `pipeline` | yes | [open](https://api-web.nhle.com/v1/scoreboard/now) |
| `E000319` | `federal_register` | 200 | 2026-09-22T01:57:26Z | `53f39e631ee3fb13` | 0 | `pipeline` | yes | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=reasoning) |
| `E000320` | `federal_register` | 200 | 2026-09-22T01:57:26Z | `74a2f6f7a9699950` | 0 | `pipeline` | yes | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=agent) |
| `E000321` | `federal_register` | 200 | 2026-09-22T01:57:26Z | `4bc60b3b1b10cb82` | 0 | `pipeline` | yes | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=model) |
| `E000322` | `federal_register` | 200 | 2026-09-22T01:57:26Z | `c361d387d18f7856` | 0 | `pipeline` | yes | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=transformer) |
| `E000323` | `arxiv` | 200 | 2026-09-22T01:57:26Z | `56fafd096fb51e07` | 20,412 | `pipeline` | yes | [open](https://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results=8) |
| `E000324` | `openalex` | 200 | 2026-09-22T01:57:26Z | `d3007ffc3ddc93f7` | 0 | `pipeline` | yes | [open](https://api.openalex.org/works?sort=publication_date:desc&per-page=5&mailto=buffedlizard55@gmail.com) |
| `E000325` | `crossref` | 200 | 2026-09-22T01:57:26Z | `e37f116cd003dd92` | 0 | `pipeline` | yes | [open](https://api.crossref.org/works?rows=3&sort=created&order=desc&mailto=buffedlizard55@gmail.com) |
| `E000326` | `europepmc` | 200 | 2026-09-22T01:57:26Z | `7daa5f64bcd77d78` | 0 | `pipeline` | yes | [open](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=artificial+intelligence&format=json&pageSize=3) |
| `E000327` | `huggingface` | 200 | 2026-09-22T01:57:26Z | `722fe46c38263f41` | 0 | `pipeline` | yes | [open](https://huggingface.co/api/models?sort=trendingScore&limit=10) |
| `E000328` | `github_search` | 200 | 2026-09-22T01:57:26Z | `ebba9e8ea0f09652` | 0 | `pipeline` | yes | [open](https://api.github.com/search/repositories?q=agent%20created%3A%3E%3D2026-06-23&sort=stars&order=desc&per_page=20) |
| `E000329` | `github_search` | 200 | 2026-09-22T01:57:26Z | `f05745a867ae938b` | 0 | `pipeline` | yes | [open](https://api.github.com/search/repositories?q=framework%20created%3A%3E%3D2026-06-23&sort=stars&order=desc&per_page=20) |
| `E000330` | `github_search` | 200 | 2026-09-22T01:57:26Z | `2782cb2c5bc26f59` | 0 | `pipeline` | yes | [open](https://api.github.com/search/repositories?q=agent%20framework%20created%3A%3E%3D2026-09-14&sort=stars&order=desc&per_page=25) |
| `E000331` | `stackexchange` | 200 | 2026-09-22T01:57:26Z | `4d8bd1e980f7aadf` | 0 | `pipeline` | yes | [open](https://api.stackexchange.com/2.3/questions?order=desc&sort=votes&site=stackoverflow&pagesize=5&tagged=python) |
| `E000332` | `federal_register` | 200 | 2026-09-22T01:57:26Z | `65f668bf4b58b092` | 0 | `pipeline` | yes | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=artificial%20intelligence) |
| `E000333` | `federal_register` | 200 | 2026-09-22T01:57:26Z | `181976fa6d4e9e88` | 0 | `pipeline` | yes | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=health) |
| `E000334` | `federal_register` | 200 | 2026-09-22T01:57:26Z | `a3614a9f31968ad9` | 0 | `pipeline` | yes | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=energy) |
| `E000335` | `federal_register` | 200 | 2026-09-22T01:57:26Z | `1c0c66291523c7d0` | 0 | `pipeline` | yes | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=security) |
| `E000336` | `worldbank` | 200 | 2026-09-22T01:57:26Z | `6553a6ca496b6e6d` | 0 | `pipeline` | yes | [open](https://api.worldbank.org/v2/country/USA/indicator/NY.GDP.MKTP.CD?format=json&per_page=3) |
| `E000337` | `ecb_sdmx` | 200 | 2026-09-22T01:57:26Z | `00516b387b5f78a9` | 0 | `pipeline` | yes | [open](https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A?lastNObservations=3&format=jsondata) |
| `E000338` | `frankfurter` | 200 | 2026-09-22T01:57:26Z | `83d922ecbed5fd7c` | 0 | `pipeline` | yes | [open](https://api.frankfurter.app/latest?from=USD&to=EUR,KRW,JPY) |
| `E000339` | `pubmed` | 200 | 2026-09-22T01:57:26Z | `f6d93a673f9585f2` | 0 | `pipeline` | yes | [open](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=trial&retmax=1&retmode=json) |
| `E000340` | `federal_register` | 200 | 2026-09-22T01:57:26Z | `235da219d0783539` | 0 | `pipeline` | yes | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=public%20health) |
| `E000341` | `federal_register` | 200 | 2026-09-22T01:57:26Z | `b1002047cbe7e13f` | 0 | `pipeline` | yes | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=surveillance) |
| `E000342` | `federal_register` | 200 | 2026-09-22T01:57:26Z | `9134d9c48f390ed8` | 0 | `pipeline` | yes | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=data%20exchange) |
| `E000343` | `pubmed` | 200 | 2026-09-22T01:57:26Z | `53eb0d58905ad9fa` | 0 | `pipeline` | yes | [open](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=cdc&retmax=1&retmode=json) |
| `E000344` | `kalshi_public` | 200 | 2026-09-22T01:57:26Z | `01ef37851cdb516c` | 0 | `pipeline` | yes | [open](https://api.elections.kalshi.com/trade-api/v2/markets?limit=5) |
| `E000345` | `github_search` | 200 | 2026-09-22T01:57:26Z | `0cf8d029566c7ba2` | 0 | `pipeline` | yes | [open](https://api.github.com/search/repositories?q=kalshi%20created%3A%3E%3D2026-06-23&sort=stars&order=desc&per_page=20) |
| `E000346` | `github_search` | 200 | 2026-09-22T01:57:26Z | `125a9d34315e345c` | 0 | `pipeline` | yes | [open](https://api.github.com/search/repositories?q=prediction%20market%20created%3A%3E%3D2026-06-23&sort=stars&order=desc&per_page=20) |
| `E000347` | `github_search` | 200 | 2026-09-22T01:57:26Z | `40d9f6b66b5abd80` | 0 | `pipeline` | yes | [open](https://api.github.com/search/repositories?q=kalshi%20prediction%20market%20created%3A%3E%3D2026-09-14&sort=stars&order=desc&per_page=25) |
| `E000348` | `github_repos` | 200 | 2026-09-22T01:57:26Z | `912af259854cd8bb` | 0 | `pipeline` | yes | [open](https://api.github.com/users/buffedlizard55-lab/repos?per_page=100&sort=updated) |
| `E000349` | `wikimedia_pageviews` | 200 | 2026-09-22T01:57:26Z | `2cb3b522b0a3827a` | 0 | `pipeline` | yes | [open](https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/Artificial_intelligence/daily/20260909/20260915) |
| `E000350` | `github_search` | 200 | 2026-09-22T01:57:26Z | `e9a3b9367a0a4b6d` | 0 | `pipeline` | yes | [open](https://api.github.com/search/repositories?q=repo%3Azai-org/ZCode&sort=stars&order=desc&per_page=1) |
| `E000351` | `github_search` | 200 | 2026-09-22T01:57:26Z | `7c50a0d8374a0aa4` | 0 | `pipeline` | yes | [open](https://api.github.com/search/repositories?q=repo%3Abrowser-use/jev-ultrafast&sort=stars&order=desc&per_page=1) |
| `E000352` | `github_search` | 200 | 2026-09-22T01:57:26Z | `17b6bb173406ccc6` | 0 | `pipeline` | yes | [open](https://api.github.com/search/repositories?q=repo%3Abrayonpi/hexstellar&sort=stars&order=desc&per_page=1) |
| `E000353` | `github_search` | 200 | 2026-09-22T01:57:26Z | `4571e7427bc8bbb6` | 0 | `pipeline` | yes | [open](https://api.github.com/search/repositories?q=repo%3Ashadcn-ui/lint&sort=stars&order=desc&per_page=1) |
| `E000354` | `github_search` | 200 | 2026-09-22T01:57:26Z | `4b3cceac8f5ffda6` | 0 | `pipeline` | yes | [open](https://api.github.com/search/repositories?q=repo%3AZJU-REAL/Easel&sort=stars&order=desc&per_page=1) |
| `E000355` | `github_search` | 200 | 2026-09-22T01:57:26Z | `c733b7da03594c20` | 0 | `pipeline` | yes | [open](https://api.github.com/search/repositories?q=repo%3Aagentverse-os/AgentVerse-OS&sort=stars&order=desc&per_page=1) |
| `E000356` | `github_search` | 200 | 2026-09-22T01:57:26Z | `8f3f132c5efec6a0` | 0 | `pipeline` | yes | [open](https://api.github.com/search/repositories?q=repo%3AHanyuanWang/LiveStream-Agent-Studio&sort=stars&order=desc&per_page=1) |
| `E000357` | `github_search` | 200 | 2026-09-22T01:57:26Z | `02ba754e28217ac6` | 0 | `pipeline` | yes | [open](https://api.github.com/search/repositories?q=repo%3Ajtydhr88/screenwriting-skills&sort=stars&order=desc&per_page=1) |

`wire-hash verifiable = no` means the body was recorded by an interactive agent
read rather than by the pipeline, so the stored hash covers the recorded body and
not the bytes on the wire. Those rows are re-read by the next probe.

## 4. Library accounting

| | |
|---|---|
| Topics tracked | 61 |
| Topics with ≥1 verified claim | 12 |
| Topics with 0 verified claims | 49 |
| Candidate / active / retired / blocked | 9 / 51 / 0 / 1 |
| Families | 13 |

## 5. Reproducing any number on the site

```bash
python3 -m msl.cli cycle --offline   # rebuild every artifact from data/seed/, no network
python3 -m msl.cli verify-claims     # recheck every derived claim, report drift
python3 tools/probe_sources.py       # live-read every registered source
python3 -m unittest discover -s tests
```

A number on the site that you cannot reproduce with one of those four commands is
a defect. Report it as an irregularity rather than editing the number.
