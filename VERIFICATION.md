# VERIFICATION — line-by-line audit ledger

Generated `2026-09-22T04:15:17Z` at cycle 13. Read-only verifiers:
`python3 -m msl.cli verify-claims` and `python3 tools/probe_sources.py`.

## 1. Claim ledger composition

| Kind | Count | What it means |
|---|---|---|
| `captured` | 7,006 | A value lifted from a payload this project read |
| `documented` | 0 | A value from the operator's own published record |
| `negative` | 0 | Proof that something does **not** exist |
| `derived` | 3,328 | Arithmetic over claims above, formula recorded |
| **Total accepted** | **10,334** | |
| Rejected by the gate | 0 | Published, not swallowed |

## 2. Source registry

28 sources. `status` is written only by the probe.

| # | Id | Name | Operator | Status | Live reads | Last read (UTC) | HTTP | Links |
|---|---|---|---|---|---|---|---|---|
| 1 | `arxiv` | arXiv API | arXiv (Cornell University) | `verified-live-read` | 2 | 2026-09-22T04:15:17Z | 200 | [docs](https://info.arxiv.org/help/api/index.html) · [probe](https://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results=1) |
| 2 | `bls` | U.S. Bureau of Labor Statistics Public Data API v2 | U.S. Bureau of Labor Statistics | `verified-live-read` | 1 | 2026-09-22T04:15:17Z | 200 | [docs](https://www.bls.gov/developers/home.htm) · [probe](https://api.bls.gov/publicAPI/v2/timeseries/data/CUUR0000SA0) |
| 3 | `census_acs` | U.S. Census Bureau API (ACS 5-year) | U.S. Census Bureau | `registered` | 0 | 2026-09-22T03:42:39Z | — | [docs](https://www.census.gov/data/developers/data-sets.html) · [probe](https://api.census.gov/data/2022/acs/acs5?get=NAME,B01001_001E&for=state:06) |
| 4 | `clinicaltrials` | ClinicalTrials.gov API v2 | U.S. National Library of Medicine | `blocked` | 0 | 2026-09-22T04:15:17Z | 403 | [docs](https://clinicaltrials.gov/data-api/api) · [probe](https://clinicaltrials.gov/api/v2/studies?pageSize=1) |
| 5 | `crossref` | Crossref REST API | Crossref | `verified-live-read` | 2 | 2026-09-22T04:15:17Z | 200 | [docs](https://www.crossref.org/documentation/retrieve-metadata/rest-api/) · [probe](https://api.crossref.org/works?rows=1&sort=created&order=desc) |
| 6 | `ecb_sdmx` | ECB Data Portal — SDMX REST (EXR daily) | European Central Bank | `verified-live-read` | 2 | 2026-09-22T04:15:17Z | 200 | [docs](https://data-explorer.ecb.europa.eu/) · [probe](https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A?lastNObservations=1&format=jsondata) |
| 7 | `europepmc` | Europe PMC REST | European Molecular Biology Laboratory | `verified-live-read` | 2 | 2026-09-22T04:15:17Z | 200 | [docs](https://europepmc.org/RestfulWebService) · [probe](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=artificial+intelligence&format=json&pageSize=1) |
| 8 | `federal_register` | Federal Register API v1 | U.S. National Archives / Office of the Federal Register | `verified-live-read` | 12 | 2026-09-22T04:15:17Z | 200 | [docs](https://www.federalregister.gov/developers/documentation/api/v1) · [probe](https://www.federalregister.gov/api/v1/documents.json?per_page=1&order=newest) |
| 9 | `frankfurter` | Frankfurter FX (ECB reference rates mirror) | Community service publishing ECB reference rates | `verified-live-read` | 2 | 2026-09-22T04:15:17Z | 200 | [docs](https://www.frankfurter.app/) · [probe](https://api.frankfurter.app/latest?from=USD&to=EUR,KRW) |
| 10 | `github_repos` | GitHub Repos API — owner corpus | GitHub, Inc. | `verified-live-read` | 4 | 2026-09-22T04:15:17Z | 200 | [docs](https://docs.github.com/en/rest/repos/repos) · [probe](https://api.github.com/users/buffedlizard55-lab/repos?per_page=1) |
| 11 | `github_search` | GitHub Search API — repositories | GitHub, Inc. | `verified-live-read` | 17 | 2026-09-22T04:15:17Z | 200 | [docs](https://docs.github.com/en/rest/search/search) · [probe](https://api.github.com/search/repositories?q=created:%3E=2026-09-14&sort=stars&order=desc&per_page=1) |
| 12 | `hn_firebase` | Hacker News official Firebase API | Hacker News / Y Combinator | `verified-live-read` | 1 | 2026-09-22T04:15:17Z | 200 | [docs](https://github.com/HackerNews/API) · [probe](https://hacker-news.firebaseio.com/v0/topstories.json) |
| 13 | `huggingface` | Hugging Face Hub API | Hugging Face, Inc. | `verified-live-read` | 2 | 2026-09-22T04:15:17Z | 200 | [docs](https://huggingface.co/docs/hub/api) · [probe](https://huggingface.co/api/models?sort=trendingScore&limit=1) |
| 14 | `kalshi_public` | Kalshi public market data | KalshiEX LLC | `verified-live-read` | 2 | 2026-09-22T04:15:17Z | 200 | [docs](https://trading-api.readme.io/reference/getmarkets) · [probe](https://api.elections.kalshi.com/trade-api/v2/markets?limit=1) |
| 15 | `mlb_statsapi` | MLB StatsAPI — schedule | Major League Baseball Advanced Media | `blocked` | 1 | 2026-09-22T04:15:17Z | 400 | [docs](https://statsapi.mlb.com/) · [probe](https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=2026-09-20) |
| 16 | `nba_cdn` | NBA CDN — today's scoreboard | National Basketball Association | `blocked` | 0 | 2026-09-22T04:15:17Z | 403 | [docs](https://cdn.nba.com/) · [probe](https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json) |
| 17 | `nhl_web` | NHL public web API — scoreboard | National Hockey League | `verified-live-read` | 1 | 2026-09-22T04:15:17Z | 200 | [docs](https://api-web.nhle.com/) · [probe](https://api-web.nhle.com/v1/scoreboard/now) |
| 18 | `nominatim` | OpenStreetMap Nominatim | OpenStreetMap Foundation | `verified-live-read` | 1 | 2026-09-22T04:15:17Z | 200 | [docs](https://nominatim.org/release-docs/latest/api/Search/) · [probe](https://nominatim.openstreetmap.org/search?q=Seoul&format=json&limit=1) |
| 19 | `npm_registry` | npm Registry — package metadata | GitHub, Inc. (npm) | `verified-live-read` | 3 | 2026-09-22T04:15:17Z | 200 | [docs](https://github.com/npm/registry) · [probe](https://registry.npmjs.org/next/latest) |
| 20 | `nws_alerts` | api.weather.gov — active alerts | U.S. National Weather Service (NOAA) | `verified-live-read` | 1 | 2026-09-22T04:15:17Z | 200 | [docs](https://www.weather.gov/documentation/services-web-api) · [probe](https://api.weather.gov/alerts/active?area=CA) |
| 21 | `openalex` | OpenAlex scholarly graph | OurResearch (open catalogue of scholarly works) | `verified-live-read` | 2 | 2026-09-22T04:15:17Z | 200 | [docs](https://docs.openalex.org/) · [probe](https://api.openalex.org/works?sort=publication_date:desc&per-page=1) |
| 22 | `pubmed` | NCBI PubMed E-utilities | U.S. National Library of Medicine | `verified-live-read` | 3 | 2026-09-22T04:15:17Z | 200 | [docs](https://www.ncbi.nlm.nih.gov/books/NBK25501/) · [probe](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=artificial+intelligence&retmax=1&retmode=json) |
| 23 | `pypi_json` | PyPI JSON API | Python Software Foundation | `verified-live-read` | 3 | 2026-09-22T04:15:17Z | 200 | [docs](https://docs.pypi.org/api/json/) · [probe](https://pypi.org/pypi/requests/json) |
| 24 | `sec_edgar` | SEC EDGAR — company submissions | U.S. Securities and Exchange Commission | `blocked` | 0 | 2026-09-22T04:15:17Z | 403 | [docs](https://www.sec.gov/edgar/sec-api-documentation) · [probe](https://data.sec.gov/submissions/CIK0000320193.json) |
| 25 | `stackexchange` | Stack Exchange API 2.3 | Stack Exchange, Inc. | `verified-live-read` | 2 | 2026-09-22T04:15:17Z | 200 | [docs](https://api.stackexchange.com/docs) · [probe](https://api.stackexchange.com/2.3/questions?order=desc&sort=votes&site=stackoverflow&pagesize=1) |
| 26 | `usgs_fdsn` | USGS Earthquake Hazards — FDSN event service | U.S. Geological Survey | `verified-live-read` | 1 | 2026-09-22T04:15:17Z | 200 | [docs](https://earthquake.usgs.gov/fdsnws/event/1/) · [probe](https://earthquake.usgs.gov/fdsnws/event/1/count?format=geojson&starttime=2026-09-14&minmagnitude=5.0) |
| 27 | `wikimedia_pageviews` | Wikimedia Pageviews REST API | Wikimedia Foundation | `verified-live-read` | 2 | 2026-09-22T04:15:17Z | 200 | [docs](https://wikimedia.org/api/rest_v1/) · [probe](https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/Artificial_intelligence/daily/20260914/20260920) |
| 28 | `worldbank` | World Bank Open Data API | The World Bank | `verified-live-read` | 2 | 2026-09-22T04:15:17Z | 200 | [docs](https://datahelpdesk.worldbank.org/knowledgebase/articles/889392) · [probe](https://api.worldbank.org/v2/country/USA/indicator/NY.GDP.MKTP.CD?format=json&per_page=1) |

## 3. Most recent evidence rows

Every row is one outbound read, with the hash of what came back.

| Id | Source | HTTP | Captured (UTC) | SHA-256 (16) | Bytes | Capture mode | Wire-hash verifiable | URL |
|---|---|---|---|---|---|---|---|---|
| `E000443` | `npm_registry` | 200 | 2026-09-22T04:15:17Z | `48b5968c14c5e882` | 0 | `pipeline` | yes | [open](https://registry.npmjs.org/next/latest) |
| `E000444` | `wikimedia_pageviews` | 200 | 2026-09-22T04:15:17Z | `e60a37eff2a9a9f2` | 0 | `pipeline` | yes | [open](https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/Artificial_intelligence/daily/20260914/20260920) |
| `E000445` | `federal_register` | 200 | 2026-09-22T04:15:17Z | `67230d2e1034fbd6` | 0 | `pipeline` | yes | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=1&order=newest) |
| `E000446` | `usgs_fdsn` | 200 | 2026-09-22T04:15:17Z | `5f59622eed5c328c` | 0 | `pipeline` | yes | [open](https://earthquake.usgs.gov/fdsnws/event/1/count?format=geojson&starttime=2026-09-14&minmagnitude=5.0) |
| `E000447` | `hn_firebase` | 200 | 2026-09-22T04:15:17Z | `03109001f8cf0527` | 0 | `pipeline` | yes | [open](https://hacker-news.firebaseio.com/v0/topstories.json) |
| `E000448` | `arxiv` | 200 | 2026-09-22T04:15:17Z | `f7945e262d6af835` | 4,225 | `pipeline` | yes | [open](https://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results=1) |
| `E000449` | `pubmed` | 200 | 2026-09-22T04:15:17Z | `d3f1731ab6fed7f5` | 0 | `pipeline` | yes | [open](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=artificial+intelligence&retmax=1&retmode=json) |
| `E000450` | `openalex` | 200 | 2026-09-22T04:15:17Z | `41fe39a76ff2641d` | 0 | `pipeline` | yes | [open](https://api.openalex.org/works?sort=publication_date:desc&per-page=1) |
| `E000451` | `crossref` | 200 | 2026-09-22T04:15:17Z | `5493340b211326a0` | 0 | `pipeline` | yes | [open](https://api.crossref.org/works?rows=1&sort=created&order=desc) |
| `E000452` | `stackexchange` | 200 | 2026-09-22T04:15:17Z | `13ff487985080ed0` | 0 | `pipeline` | yes | [open](https://api.stackexchange.com/2.3/questions?order=desc&sort=votes&site=stackoverflow&pagesize=1) |
| `E000453` | `huggingface` | 200 | 2026-09-22T04:15:17Z | `e6926e2dc6a70997` | 0 | `pipeline` | yes | [open](https://huggingface.co/api/models?sort=trendingScore&limit=1) |
| `E000454` | `nws_alerts` | 200 | 2026-09-22T04:15:17Z | `9fb9615ebf8db881` | 0 | `pipeline` | yes | [open](https://api.weather.gov/alerts/active?area=CA) |
| `E000455` | `worldbank` | 200 | 2026-09-22T04:15:17Z | `57ee09ac4cf11069` | 0 | `pipeline` | yes | [open](https://api.worldbank.org/v2/country/USA/indicator/NY.GDP.MKTP.CD?format=json&per_page=1) |
| `E000456` | `ecb_sdmx` | 200 | 2026-09-22T04:15:17Z | `895d227179369f34` | 0 | `pipeline` | yes | [open](https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A?lastNObservations=1&format=jsondata) |
| `E000457` | `frankfurter` | 200 | 2026-09-22T04:15:17Z | `e79810a76ada8f34` | 0 | `pipeline` | yes | [open](https://api.frankfurter.app/latest?from=USD&to=EUR,KRW) |
| `E000458` | `bls` | 200 | 2026-09-22T04:15:17Z | `68f5d04c8148950b` | 0 | `pipeline` | yes | [open](https://api.bls.gov/publicAPI/v2/timeseries/data/CUUR0000SA0) |
| `E000459` | `nominatim` | 200 | 2026-09-22T04:15:17Z | `9d37c36d1474d973` | 0 | `pipeline` | yes | [open](https://nominatim.openstreetmap.org/search?q=Seoul&format=json&limit=1) |
| `E000460` | `europepmc` | 200 | 2026-09-22T04:15:17Z | `83253cb1b977bbdc` | 0 | `pipeline` | yes | [open](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=artificial+intelligence&format=json&pageSize=1) |
| `E000461` | `kalshi_public` | 200 | 2026-09-22T04:15:17Z | `8a4faa0b1e71a3fb` | 0 | `pipeline` | yes | [open](https://api.elections.kalshi.com/trade-api/v2/markets?limit=1) |
| `E000462` | `mlb_statsapi` | 200 | 2026-09-22T04:15:17Z | `380848368ace97b5` | 0 | `pipeline` | yes | [open](https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=2026-09-20) |
| `E000463` | `nhl_web` | 200 | 2026-09-22T04:15:17Z | `1af571f463e2c467` | 0 | `pipeline` | yes | [open](https://api-web.nhle.com/v1/scoreboard/now) |
| `E000464` | `federal_register` | 200 | 2026-09-22T04:15:17Z | `53f39e631ee3fb13` | 0 | `pipeline` | yes | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=reasoning) |
| `E000465` | `federal_register` | 200 | 2026-09-22T04:15:17Z | `74a2f6f7a9699950` | 0 | `pipeline` | yes | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=agent) |
| `E000466` | `federal_register` | 200 | 2026-09-22T04:15:17Z | `4bc60b3b1b10cb82` | 0 | `pipeline` | yes | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=model) |
| `E000467` | `federal_register` | 200 | 2026-09-22T04:15:17Z | `c361d387d18f7856` | 0 | `pipeline` | yes | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=transformer) |
| `E000468` | `arxiv` | 200 | 2026-09-22T04:15:17Z | `c316ea1e4706c065` | 21,957 | `pipeline` | yes | [open](https://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results=8) |
| `E000469` | `openalex` | 200 | 2026-09-22T04:15:17Z | `fb6e77d8b73103ef` | 0 | `pipeline` | yes | [open](https://api.openalex.org/works?sort=publication_date:desc&per-page=5&mailto=buffedlizard55@gmail.com) |
| `E000470` | `crossref` | 200 | 2026-09-22T04:15:17Z | `3ab1a4db4b8a92b5` | 0 | `pipeline` | yes | [open](https://api.crossref.org/works?rows=3&sort=created&order=desc&mailto=buffedlizard55@gmail.com) |
| `E000471` | `europepmc` | 200 | 2026-09-22T04:15:17Z | `44f0239c16aec872` | 0 | `pipeline` | yes | [open](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=artificial+intelligence&format=json&pageSize=3) |
| `E000472` | `huggingface` | 200 | 2026-09-22T04:15:17Z | `241c5c4acfd5a7dd` | 0 | `pipeline` | yes | [open](https://huggingface.co/api/models?sort=trendingScore&limit=10) |
| `E000473` | `github_search` | 200 | 2026-09-22T04:15:17Z | `292e542b53dac15a` | 0 | `pipeline` | yes | [open](https://api.github.com/search/repositories?q=agent%20created%3A%3E%3D2026-06-23&sort=stars&order=desc&per_page=20) |
| `E000474` | `github_search` | 200 | 2026-09-22T04:15:17Z | `7e9209b45a07b2ca` | 0 | `pipeline` | yes | [open](https://api.github.com/search/repositories?q=framework%20created%3A%3E%3D2026-06-23&sort=stars&order=desc&per_page=20) |
| `E000475` | `github_search` | 200 | 2026-09-22T04:15:17Z | `a8483be9f88394e7` | 0 | `pipeline` | yes | [open](https://api.github.com/search/repositories?q=agent%20framework%20created%3A%3E%3D2026-09-14&sort=stars&order=desc&per_page=25) |
| `E000476` | `stackexchange` | 200 | 2026-09-22T04:15:17Z | `d08ddc1153a33734` | 0 | `pipeline` | yes | [open](https://api.stackexchange.com/2.3/questions?order=desc&sort=votes&site=stackoverflow&pagesize=5&tagged=python) |
| `E000477` | `federal_register` | 200 | 2026-09-22T04:15:17Z | `65f668bf4b58b092` | 0 | `pipeline` | yes | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=artificial%20intelligence) |
| `E000478` | `federal_register` | 200 | 2026-09-22T04:15:17Z | `181976fa6d4e9e88` | 0 | `pipeline` | yes | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=health) |
| `E000479` | `federal_register` | 200 | 2026-09-22T04:15:17Z | `a3614a9f31968ad9` | 0 | `pipeline` | yes | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=energy) |
| `E000480` | `federal_register` | 200 | 2026-09-22T04:15:17Z | `1c0c66291523c7d0` | 0 | `pipeline` | yes | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=security) |
| `E000481` | `worldbank` | 200 | 2026-09-22T04:15:17Z | `6553a6ca496b6e6d` | 0 | `pipeline` | yes | [open](https://api.worldbank.org/v2/country/USA/indicator/NY.GDP.MKTP.CD?format=json&per_page=3) |
| `E000482` | `ecb_sdmx` | 200 | 2026-09-22T04:15:17Z | `00516b387b5f78a9` | 0 | `pipeline` | yes | [open](https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A?lastNObservations=3&format=jsondata) |
| `E000483` | `frankfurter` | 200 | 2026-09-22T04:15:17Z | `83d922ecbed5fd7c` | 0 | `pipeline` | yes | [open](https://api.frankfurter.app/latest?from=USD&to=EUR,KRW,JPY) |
| `E000484` | `pubmed` | 200 | 2026-09-22T04:15:17Z | `e5cbe405dbaf6995` | 0 | `pipeline` | yes | [open](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=trial&retmax=1&retmode=json) |
| `E000485` | `federal_register` | 200 | 2026-09-22T04:15:17Z | `235da219d0783539` | 0 | `pipeline` | yes | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=public%20health) |
| `E000486` | `federal_register` | 200 | 2026-09-22T04:15:17Z | `b1002047cbe7e13f` | 0 | `pipeline` | yes | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=surveillance) |
| `E000487` | `federal_register` | 200 | 2026-09-22T04:15:17Z | `9134d9c48f390ed8` | 0 | `pipeline` | yes | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=data%20exchange) |
| `E000488` | `pubmed` | 200 | 2026-09-22T04:15:17Z | `d3a2f01c31bf104f` | 0 | `pipeline` | yes | [open](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=cdc&retmax=1&retmode=json) |
| `E000489` | `kalshi_public` | 200 | 2026-09-22T04:15:17Z | `6282b1c7f3815d83` | 0 | `pipeline` | yes | [open](https://api.elections.kalshi.com/trade-api/v2/markets?limit=5) |
| `E000490` | `github_search` | 200 | 2026-09-22T04:15:17Z | `9f4b90f152b54868` | 0 | `pipeline` | yes | [open](https://api.github.com/search/repositories?q=kalshi%20created%3A%3E%3D2026-06-23&sort=stars&order=desc&per_page=20) |
| `E000491` | `github_search` | 200 | 2026-09-22T04:15:17Z | `ff35bbb8f76fd588` | 0 | `pipeline` | yes | [open](https://api.github.com/search/repositories?q=prediction%20market%20created%3A%3E%3D2026-06-23&sort=stars&order=desc&per_page=20) |
| `E000492` | `github_search` | 200 | 2026-09-22T04:15:17Z | `b3e024f3bd5f3e1d` | 0 | `pipeline` | yes | [open](https://api.github.com/search/repositories?q=kalshi%20prediction%20market%20created%3A%3E%3D2026-09-14&sort=stars&order=desc&per_page=25) |
| `E000493` | `github_repos` | 200 | 2026-09-22T04:15:17Z | `5947fe94968ce559` | 0 | `pipeline` | yes | [open](https://api.github.com/users/buffedlizard55-lab/repos?per_page=100&sort=updated) |
| `E000494` | `wikimedia_pageviews` | 200 | 2026-09-22T04:15:17Z | `2cb3b522b0a3827a` | 0 | `pipeline` | yes | [open](https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/Artificial_intelligence/daily/20260909/20260915) |
| `E000495` | `github_search` | 200 | 2026-09-22T04:15:17Z | `047da289b91f8d94` | 0 | `pipeline` | yes | [open](https://api.github.com/search/repositories?q=repo%3Azai-org/ZCode&sort=stars&order=desc&per_page=1) |
| `E000496` | `github_search` | 200 | 2026-09-22T04:15:17Z | `87df6028a5554e35` | 0 | `pipeline` | yes | [open](https://api.github.com/search/repositories?q=repo%3Abrowser-use/jev-ultrafast&sort=stars&order=desc&per_page=1) |
| `E000497` | `github_search` | 200 | 2026-09-22T04:15:17Z | `9737e6d0603b5a1c` | 0 | `pipeline` | yes | [open](https://api.github.com/search/repositories?q=repo%3Abrayonpi/hexstellar&sort=stars&order=desc&per_page=1) |
| `E000498` | `github_search` | 200 | 2026-09-22T04:15:17Z | `1d762a8d25905c3e` | 0 | `pipeline` | yes | [open](https://api.github.com/search/repositories?q=repo%3Ashadcn-ui/lint&sort=stars&order=desc&per_page=1) |
| `E000499` | `github_search` | 200 | 2026-09-22T04:15:17Z | `49f17c6269a75ff5` | 0 | `pipeline` | yes | [open](https://api.github.com/search/repositories?q=repo%3Aagentverse-os/AgentVerse-OS&sort=stars&order=desc&per_page=1) |
| `E000500` | `github_search` | 200 | 2026-09-22T04:15:17Z | `8f3f132c5efec6a0` | 0 | `pipeline` | yes | [open](https://api.github.com/search/repositories?q=repo%3AHanyuanWang/LiveStream-Agent-Studio&sort=stars&order=desc&per_page=1) |
| `E000501` | `github_search` | 200 | 2026-09-22T04:15:17Z | `99ef2fd1e3b26eb2` | 0 | `pipeline` | yes | [open](https://api.github.com/search/repositories?q=repo%3Ajtydhr88/screenwriting-skills&sort=stars&order=desc&per_page=1) |
| `E000502` | `github_search` | 200 | 2026-09-22T04:15:17Z | `d2529c3e28a69ee1` | 0 | `pipeline` | yes | [open](https://api.github.com/search/repositories?q=repo%3ANanako0129/sepia&sort=stars&order=desc&per_page=1) |

`wire-hash verifiable = no` means the body was recorded by an interactive agent
read rather than by the pipeline, so the stored hash covers the recorded body and
not the bytes on the wire. Those rows are re-read by the next probe.

## 4. Library accounting

| | |
|---|---|
| Topics tracked | 91 |
| Topics with ≥1 verified claim | 12 |
| Topics with 0 verified claims | 79 |
| Candidate / active / retired / blocked | 2 / 88 / 0 / 1 |
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
