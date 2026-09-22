# VERIFICATION — line-by-line audit ledger

Generated `2026-09-22T17:24:28Z` at cycle 17. Read-only verifiers:
`python3 -m msl.cli verify-claims` and `python3 tools/probe_sources.py`.

## 1. Claim ledger composition

| Kind | Count | What it means |
|---|---|---|
| `captured` | 9,310 | A value lifted from a payload this project read |
| `documented` | 0 | A value from the operator's own published record |
| `negative` | 3 | Proof that something does **not** exist |
| `derived` | 4,729 | Arithmetic over claims above, formula recorded |
| **Total accepted** | **14,042** | |
| Rejected by the gate | 0 | Published, not swallowed |

## 2. Source registry

30 sources. `status` is written only by the probe.

| # | Id | Name | Operator | Status | Live reads | Last read (UTC) | HTTP | Links |
|---|---|---|---|---|---|---|---|---|
| 1 | `arxiv` | arXiv API | arXiv (Cornell University) | `verified-live-read` | 11 | 2026-09-22T17:24:28Z | 200 | [docs](https://info.arxiv.org/help/api/index.html) · [probe](https://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results=1) |
| 2 | `bls` | U.S. Bureau of Labor Statistics Public Data API v2 | U.S. Bureau of Labor Statistics | `verified-live-read` | 6 | 2026-09-22T17:24:28Z | 200 | [docs](https://www.bls.gov/developers/home.htm) · [probe](https://api.bls.gov/publicAPI/v2/timeseries/data/CUUR0000SA0) |
| 3 | `census_acs` | U.S. Census Bureau API (ACS 5-year) | U.S. Census Bureau | `verified-live-read` | 1 | 2026-09-22T12:45:18Z | 200 | [docs](https://www.census.gov/data/developers/data-sets.html) · [probe](https://api.census.gov/data/2022/acs/acs5?get=NAME,B01001_001E&for=state:06) |
| 4 | `clinicaltrials` | ClinicalTrials.gov API v2 | U.S. National Library of Medicine | `blocked` | 0 | 2026-09-22T17:24:28Z | 403 | [docs](https://clinicaltrials.gov/data-api/api) · [probe](https://clinicaltrials.gov/api/v2/studies?pageSize=1) |
| 5 | `crossref` | Crossref REST API | Crossref | `verified-live-read` | 11 | 2026-09-22T17:24:28Z | 200 | [docs](https://www.crossref.org/documentation/retrieve-metadata/rest-api/) · [probe](https://api.crossref.org/works?rows=1&sort=created&order=desc) |
| 6 | `ecb_sdmx` | ECB Data Portal — SDMX REST (EXR daily) | European Central Bank | `verified-live-read` | 11 | 2026-09-22T17:24:28Z | 200 | [docs](https://data-explorer.ecb.europa.eu/) · [probe](https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A?lastNObservations=1&format=jsondata) |
| 7 | `europepmc` | Europe PMC REST | European Molecular Biology Laboratory | `verified-live-read` | 11 | 2026-09-22T17:24:28Z | 200 | [docs](https://europepmc.org/RestfulWebService) · [probe](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=artificial+intelligence&format=json&pageSize=1) |
| 8 | `federal_register` | Federal Register API v1 | U.S. National Archives / Office of the Federal Register | `verified-live-read` | 61 | 2026-09-22T17:24:28Z | 200 | [docs](https://www.federalregister.gov/developers/documentation/api/v1) · [probe](https://www.federalregister.gov/api/v1/documents.json?per_page=1&order=newest) |
| 9 | `frankfurter` | Frankfurter FX (ECB reference rates mirror) | Community service publishing ECB reference rates | `verified-live-read` | 11 | 2026-09-22T17:24:28Z | 200 | [docs](https://www.frankfurter.app/) · [probe](https://api.frankfurter.app/latest?from=USD&to=EUR,KRW) |
| 10 | `github_releases` | GitHub Releases API — newest release | GitHub, Inc. | `verified-live-read` | 4 | 2026-09-22T17:24:28Z | 200 | [docs](https://docs.github.com/en/rest/releases/releases#list-releases) · [probe](https://api.github.com/repos/buffedlizard55-lab/MasterSelfLearn/releases?per_page=1) |
| 11 | `github_repo` | GitHub Repos API — one repository | GitHub, Inc. | `verified-live-read` | 4 | 2026-09-22T17:24:28Z | 200 | [docs](https://docs.github.com/en/rest/repos/repos#get-a-repository) · [probe](https://api.github.com/repos/buffedlizard55-lab/MasterSelfLearn) |
| 12 | `github_repos` | GitHub Repos API — owner corpus | GitHub, Inc. | `verified-live-read` | 13 | 2026-09-22T17:24:28Z | 200 | [docs](https://docs.github.com/en/rest/repos/repos) · [probe](https://api.github.com/users/buffedlizard55-lab/repos?per_page=1) |
| 13 | `github_search` | GitHub Search API — repositories | GitHub, Inc. | `verified-live-read` | 67 | 2026-09-22T17:24:28Z | 200 | [docs](https://docs.github.com/en/rest/search/search) · [probe](https://api.github.com/search/repositories?q=created:%3E=2026-09-14&sort=stars&order=desc&per_page=1) |
| 14 | `hn_firebase` | Hacker News official Firebase API | Hacker News / Y Combinator | `verified-live-read` | 6 | 2026-09-22T17:24:28Z | 200 | [docs](https://github.com/HackerNews/API) · [probe](https://hacker-news.firebaseio.com/v0/topstories.json) |
| 15 | `huggingface` | Hugging Face Hub API | Hugging Face, Inc. | `verified-live-read` | 11 | 2026-09-22T17:24:28Z | 200 | [docs](https://huggingface.co/docs/hub/api) · [probe](https://huggingface.co/api/models?sort=trendingScore&limit=1) |
| 16 | `kalshi_public` | Kalshi public market data | KalshiEX LLC | `verified-live-read` | 11 | 2026-09-22T17:24:28Z | 200 | [docs](https://trading-api.readme.io/reference/getmarkets) · [probe](https://api.elections.kalshi.com/trade-api/v2/markets?limit=1) |
| 17 | `mlb_statsapi` | MLB StatsAPI — schedule | Major League Baseball Advanced Media | `verified-live-read` | 6 | 2026-09-22T17:24:28Z | 200 | [docs](https://statsapi.mlb.com/) · [probe](https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=2026-09-20) |
| 18 | `nba_cdn` | NBA CDN — today's scoreboard | National Basketball Association | `blocked` | 0 | 2026-09-22T17:24:28Z | 403 | [docs](https://cdn.nba.com/) · [probe](https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json) |
| 19 | `nhl_web` | NHL public web API — scoreboard | National Hockey League | `verified-live-read` | 6 | 2026-09-22T17:24:28Z | 200 | [docs](https://api-web.nhle.com/) · [probe](https://api-web.nhle.com/v1/scoreboard/now) |
| 20 | `nominatim` | OpenStreetMap Nominatim | OpenStreetMap Foundation | `verified-live-read` | 6 | 2026-09-22T17:24:28Z | 200 | [docs](https://nominatim.org/release-docs/latest/api/Search/) · [probe](https://nominatim.openstreetmap.org/search?q=Seoul&format=json&limit=1) |
| 21 | `npm_registry` | npm Registry — package metadata | GitHub, Inc. (npm) | `verified-live-read` | 8 | 2026-09-22T17:24:28Z | 200 | [docs](https://github.com/npm/registry) · [probe](https://registry.npmjs.org/next/latest) |
| 22 | `nws_alerts` | api.weather.gov — active alerts | U.S. National Weather Service (NOAA) | `verified-live-read` | 6 | 2026-09-22T17:24:28Z | 200 | [docs](https://www.weather.gov/documentation/services-web-api) · [probe](https://api.weather.gov/alerts/active?area=CA) |
| 23 | `openalex` | OpenAlex scholarly graph | OurResearch (open catalogue of scholarly works) | `verified-live-read` | 11 | 2026-09-22T17:24:28Z | 200 | [docs](https://docs.openalex.org/) · [probe](https://api.openalex.org/works?sort=publication_date:desc&per-page=1) |
| 24 | `pubmed` | NCBI PubMed E-utilities | U.S. National Library of Medicine | `verified-live-read` | 16 | 2026-09-22T17:24:28Z | 200 | [docs](https://www.ncbi.nlm.nih.gov/books/NBK25501/) · [probe](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=artificial+intelligence&retmax=1&retmode=json) |
| 25 | `pypi_json` | PyPI JSON API | Python Software Foundation | `verified-live-read` | 8 | 2026-09-22T17:24:28Z | 200 | [docs](https://docs.pypi.org/api/json/) · [probe](https://pypi.org/pypi/requests/json) |
| 26 | `sec_edgar` | SEC EDGAR — company submissions | U.S. Securities and Exchange Commission | `blocked` | 0 | 2026-09-22T17:24:28Z | 403 | [docs](https://www.sec.gov/edgar/sec-api-documentation) · [probe](https://data.sec.gov/submissions/CIK0000320193.json) |
| 27 | `stackexchange` | Stack Exchange API 2.3 | Stack Exchange, Inc. | `verified-live-read` | 11 | 2026-09-22T17:24:28Z | 200 | [docs](https://api.stackexchange.com/docs) · [probe](https://api.stackexchange.com/2.3/questions?order=desc&sort=votes&site=stackoverflow&pagesize=1) |
| 28 | `usgs_fdsn` | USGS Earthquake Hazards — FDSN event service | U.S. Geological Survey | `verified-live-read` | 7 | 2026-09-22T17:24:28Z | 200 | [docs](https://earthquake.usgs.gov/fdsnws/event/1/) · [probe](https://earthquake.usgs.gov/fdsnws/event/1/count?format=geojson&starttime=2026-09-14&minmagnitude=5.0) |
| 29 | `wikimedia_pageviews` | Wikimedia Pageviews REST API | Wikimedia Foundation | `verified-live-read` | 11 | 2026-09-22T17:24:28Z | 200 | [docs](https://wikimedia.org/api/rest_v1/) · [probe](https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/Artificial_intelligence/daily/20260914/20260920) |
| 30 | `worldbank` | World Bank Open Data API | The World Bank | `verified-live-read` | 11 | 2026-09-22T17:24:28Z | 200 | [docs](https://datahelpdesk.worldbank.org/knowledgebase/articles/889392) · [probe](https://api.worldbank.org/v2/country/USA/indicator/NY.GDP.MKTP.CD?format=json&per_page=1) |

## 3. Most recent evidence rows

Every row is one outbound read, with the hash of what came back.

| Id | Source | HTTP | Captured (UTC) | SHA-256 (16) | Bytes | Capture mode | Wire-hash verifiable | URL |
|---|---|---|---|---|---|---|---|---|
| `E000693` | `github_search` | 200 | 2026-09-22T12:45:18Z | `17127b3a0afa636e` | 0 | `pipeline` | yes | [open](https://api.github.com/search/repositories?q=repo%3Ajtydhr88/screenwriting-skills&sort=stars&order=desc&per_page=1) |
| `E000694` | `github_search` | 200 | 2026-09-22T12:45:18Z | `1bf0100f8af35db1` | 0 | `pipeline` | yes | [open](https://api.github.com/search/repositories?q=repo%3ANanako0129/sepia&sort=stars&order=desc&per_page=1) |
| `E000695` | `github_search` | 200 | 2026-09-22T17:24:28Z | `60523656b53bd5f8` | 0 | `pipeline` | yes | [open](https://api.github.com/search/repositories?q=created:%3E=2026-09-14&sort=stars&order=desc&per_page=1) |
| `E000696` | `github_repos` | 200 | 2026-09-22T17:24:28Z | `bd608c826d2654a8` | 0 | `pipeline` | yes | [open](https://api.github.com/users/buffedlizard55-lab/repos?per_page=1) |
| `E000697` | `github_repo` | 200 | 2026-09-22T17:24:28Z | `fda8f61627ab8315` | 0 | `pipeline` | yes | [open](https://api.github.com/repos/buffedlizard55-lab/MasterSelfLearn) |
| `E000698` | `github_releases` | 200 | 2026-09-22T17:24:28Z | `4f53cda18c2baa0c` | 0 | `pipeline` | yes | [open](https://api.github.com/repos/buffedlizard55-lab/MasterSelfLearn/releases?per_page=1) |
| `E000699` | `pypi_json` | 200 | 2026-09-22T17:24:28Z | `3820597ab3eceed4` | 0 | `pipeline` | yes | [open](https://pypi.org/pypi/requests/json) |
| `E000700` | `npm_registry` | 200 | 2026-09-22T17:24:28Z | `e4cd043c8c51480b` | 0 | `pipeline` | yes | [open](https://registry.npmjs.org/next/latest) |
| `E000701` | `wikimedia_pageviews` | 200 | 2026-09-22T17:24:28Z | `e60a37eff2a9a9f2` | 0 | `pipeline` | yes | [open](https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/Artificial_intelligence/daily/20260914/20260920) |
| `E000702` | `federal_register` | 200 | 2026-09-22T17:24:28Z | `e0c2219928591dcd` | 0 | `pipeline` | yes | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=1&order=newest) |
| `E000703` | `usgs_fdsn` | 200 | 2026-09-22T17:24:28Z | `e03d2fd1c6c497e9` | 0 | `pipeline` | yes | [open](https://earthquake.usgs.gov/fdsnws/event/1/count?format=geojson&starttime=2026-09-14&minmagnitude=5.0) |
| `E000704` | `hn_firebase` | 200 | 2026-09-22T17:24:28Z | `a9217ae07f612597` | 0 | `pipeline` | yes | [open](https://hacker-news.firebaseio.com/v0/topstories.json) |
| `E000705` | `arxiv` | 200 | 2026-09-22T17:24:28Z | `0425092b419b8660` | 4,225 | `pipeline` | yes | [open](https://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results=1) |
| `E000706` | `pubmed` | 200 | 2026-09-22T17:24:28Z | `b06ef3a5d29eb9b9` | 0 | `pipeline` | yes | [open](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=artificial+intelligence&retmax=1&retmode=json) |
| `E000707` | `openalex` | 200 | 2026-09-22T17:24:28Z | `7fc6b03508943fba` | 0 | `pipeline` | yes | [open](https://api.openalex.org/works?sort=publication_date:desc&per-page=1) |
| `E000708` | `crossref` | 200 | 2026-09-22T17:24:28Z | `0a5b4879a257f26c` | 0 | `pipeline` | yes | [open](https://api.crossref.org/works?rows=1&sort=created&order=desc) |
| `E000709` | `stackexchange` | 200 | 2026-09-22T17:24:28Z | `ffba2060c91399fe` | 0 | `pipeline` | yes | [open](https://api.stackexchange.com/2.3/questions?order=desc&sort=votes&site=stackoverflow&pagesize=1) |
| `E000710` | `huggingface` | 200 | 2026-09-22T17:24:28Z | `b4852539fa07c1b8` | 0 | `pipeline` | yes | [open](https://huggingface.co/api/models?sort=trendingScore&limit=1) |
| `E000711` | `nws_alerts` | 200 | 2026-09-22T17:24:28Z | `0eae52d9e746a376` | 0 | `pipeline` | yes | [open](https://api.weather.gov/alerts/active?area=CA) |
| `E000712` | `worldbank` | 200 | 2026-09-22T17:24:28Z | `57ee09ac4cf11069` | 0 | `pipeline` | yes | [open](https://api.worldbank.org/v2/country/USA/indicator/NY.GDP.MKTP.CD?format=json&per_page=1) |
| `E000713` | `ecb_sdmx` | 200 | 2026-09-22T17:24:28Z | `c5c45d6920d8d496` | 0 | `pipeline` | yes | [open](https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A?lastNObservations=1&format=jsondata) |
| `E000714` | `frankfurter` | 200 | 2026-09-22T17:24:28Z | `381be2b6421062ad` | 0 | `pipeline` | yes | [open](https://api.frankfurter.app/latest?from=USD&to=EUR,KRW) |
| `E000715` | `bls` | 200 | 2026-09-22T17:24:28Z | `68f5d04c8148950b` | 0 | `pipeline` | yes | [open](https://api.bls.gov/publicAPI/v2/timeseries/data/CUUR0000SA0) |
| `E000716` | `nominatim` | 200 | 2026-09-22T17:24:28Z | `9d37c36d1474d973` | 0 | `pipeline` | yes | [open](https://nominatim.openstreetmap.org/search?q=Seoul&format=json&limit=1) |
| `E000717` | `europepmc` | 200 | 2026-09-22T17:24:28Z | `8598902f5db9ea30` | 0 | `pipeline` | yes | [open](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=artificial+intelligence&format=json&pageSize=1) |
| `E000718` | `kalshi_public` | 200 | 2026-09-22T17:24:28Z | `2cc7b74774eedc9e` | 0 | `pipeline` | yes | [open](https://api.elections.kalshi.com/trade-api/v2/markets?limit=1) |
| `E000719` | `mlb_statsapi` | 200 | 2026-09-22T17:24:28Z | `380848368ace97b5` | 0 | `pipeline` | yes | [open](https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=2026-09-20) |
| `E000720` | `nhl_web` | 200 | 2026-09-22T17:24:28Z | `c8466c2c5de84065` | 0 | `pipeline` | yes | [open](https://api-web.nhle.com/v1/scoreboard/now) |
| `E000721` | `federal_register` | 200 | 2026-09-22T17:24:28Z | `07411d02f41e7b80` | 0 | `pipeline` | yes | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=reasoning) |
| `E000722` | `federal_register` | 200 | 2026-09-22T17:24:28Z | `78a7e5434d1dd48c` | 0 | `pipeline` | yes | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=agent) |
| `E000723` | `federal_register` | 200 | 2026-09-22T17:24:28Z | `fe3c47d93b552160` | 0 | `pipeline` | yes | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=model) |
| `E000724` | `federal_register` | 200 | 2026-09-22T17:24:28Z | `c361d387d18f7856` | 0 | `pipeline` | yes | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=transformer) |
| `E000725` | `arxiv` | 200 | 2026-09-22T17:24:28Z | `f5caa8ed115321eb` | 21,957 | `pipeline` | yes | [open](https://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results=8) |
| `E000726` | `openalex` | 200 | 2026-09-22T17:24:28Z | `126f309754fb054c` | 0 | `pipeline` | yes | [open](https://api.openalex.org/works?sort=publication_date:desc&per-page=5&mailto=buffedlizard55@gmail.com) |
| `E000727` | `crossref` | 200 | 2026-09-22T17:24:28Z | `d471158ee46dfbfe` | 0 | `pipeline` | yes | [open](https://api.crossref.org/works?rows=3&sort=created&order=desc&mailto=buffedlizard55@gmail.com) |
| `E000728` | `europepmc` | 200 | 2026-09-22T17:24:28Z | `4d17a06ffd5d967b` | 0 | `pipeline` | yes | [open](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=artificial+intelligence&format=json&pageSize=3) |
| `E000729` | `huggingface` | 200 | 2026-09-22T17:24:28Z | `59f8162b7fe7a44e` | 0 | `pipeline` | yes | [open](https://huggingface.co/api/models?sort=trendingScore&limit=10) |
| `E000730` | `stackexchange` | 200 | 2026-09-22T17:24:28Z | `9601100fd21905e4` | 0 | `pipeline` | yes | [open](https://api.stackexchange.com/2.3/questions?order=desc&sort=votes&site=stackoverflow&pagesize=5&tagged=python) |
| `E000731` | `federal_register` | 200 | 2026-09-22T17:24:28Z | `e4ae05a508f6710a` | 0 | `pipeline` | yes | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=artificial%20intelligence) |
| `E000732` | `federal_register` | 200 | 2026-09-22T17:24:28Z | `18dfef318fcab5ef` | 0 | `pipeline` | yes | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=health) |
| `E000733` | `federal_register` | 200 | 2026-09-22T17:24:28Z | `30106a6c299648e4` | 0 | `pipeline` | yes | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=energy) |
| `E000734` | `federal_register` | 200 | 2026-09-22T17:24:28Z | `c860bf76459fa921` | 0 | `pipeline` | yes | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=security) |
| `E000735` | `worldbank` | 200 | 2026-09-22T17:24:28Z | `6553a6ca496b6e6d` | 0 | `pipeline` | yes | [open](https://api.worldbank.org/v2/country/USA/indicator/NY.GDP.MKTP.CD?format=json&per_page=3) |
| `E000736` | `ecb_sdmx` | 200 | 2026-09-22T17:24:28Z | `3d37e0bddf51e2cd` | 0 | `pipeline` | yes | [open](https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A?lastNObservations=3&format=jsondata) |
| `E000737` | `frankfurter` | 200 | 2026-09-22T17:24:28Z | `9eacd95b762066bd` | 0 | `pipeline` | yes | [open](https://api.frankfurter.app/latest?from=USD&to=EUR,KRW,JPY) |
| `E000738` | `usgs_fdsn` | 200 | 2026-09-22T17:24:28Z | `22a174c8d56b27a6` | 0 | `pipeline` | yes | [open](https://earthquake.usgs.gov/fdsnws/event/1/count?format=geojson&starttime=2026-09-09&endtime=2026-09-15&minmagnitude=5.0) |
| `E000739` | `pubmed` | 200 | 2026-09-22T17:24:28Z | `14398236a7e8b413` | 0 | `pipeline` | yes | [open](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=trial&retmax=1&retmode=json) |
| `E000740` | `federal_register` | 200 | 2026-09-22T17:24:28Z | `e58059054f6d29f8` | 0 | `pipeline` | yes | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=public%20health) |
| `E000741` | `federal_register` | 200 | 2026-09-22T17:24:28Z | `f86462d8803caf8a` | 0 | `pipeline` | yes | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=surveillance) |
| `E000742` | `federal_register` | 200 | 2026-09-22T17:24:28Z | `b510a7e519653cde` | 0 | `pipeline` | yes | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=data%20exchange) |
| `E000743` | `pubmed` | 200 | 2026-09-22T17:24:28Z | `2817f2beb6de6333` | 0 | `pipeline` | yes | [open](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=cdc&retmax=1&retmode=json) |
| `E000744` | `kalshi_public` | 200 | 2026-09-22T17:24:28Z | `eecd3e0114ace4e2` | 0 | `pipeline` | yes | [open](https://api.elections.kalshi.com/trade-api/v2/markets?limit=5) |
| `E000745` | `github_repos` | 200 | 2026-09-22T17:24:28Z | `a3a12a7414db763a` | 0 | `pipeline` | yes | [open](https://api.github.com/users/buffedlizard55-lab/repos?per_page=100&sort=updated) |
| `E000746` | `wikimedia_pageviews` | 200 | 2026-09-22T17:24:28Z | `2cb3b522b0a3827a` | 0 | `pipeline` | yes | [open](https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/Artificial_intelligence/daily/20260909/20260915) |
| `E000747` | `github_repo` | 200 | 2026-09-22T17:24:28Z | `c6bf3a3a0b99f1a6` | 0 | `pipeline` | yes | [open](https://api.github.com/repos/browser-use/jev-ultrafast) |
| `E000748` | `github_releases` | 200 | 2026-09-22T17:24:28Z | `4f53cda18c2baa0c` | 0 | `pipeline` | yes | [open](https://api.github.com/repos/browser-use/jev-ultrafast/releases?per_page=1) |
| `E000749` | `github_repo` | 200 | 2026-09-22T17:24:28Z | `02a1085ecf8394f6` | 0 | `pipeline` | yes | [open](https://api.github.com/repos/zai-org/ZCode) |
| `E000750` | `github_releases` | 200 | 2026-09-22T17:24:28Z | `4f53cda18c2baa0c` | 0 | `pipeline` | yes | [open](https://api.github.com/repos/zai-org/ZCode/releases?per_page=1) |
| `E000751` | `github_repo` | 200 | 2026-09-22T17:24:28Z | `10b6e01f64b6c2bc` | 0 | `pipeline` | yes | [open](https://api.github.com/repos/brayonpi/hexstellar) |
| `E000752` | `github_releases` | 200 | 2026-09-22T17:24:28Z | `e37e72a0a81dbbf4` | 0 | `pipeline` | yes | [open](https://api.github.com/repos/brayonpi/hexstellar/releases?per_page=1) |

`wire-hash verifiable = no` means the body was recorded by an interactive agent
read rather than by the pipeline, so the stored hash covers the recorded body and
not the bytes on the wire. Those rows are re-read by the next probe.

## 4. Library accounting

| | |
|---|---|
| Topics tracked | 115 |
| Topics with ≥1 verified claim | 12 |
| Topics with 0 verified claims | 103 |
| Candidate / active / retired / blocked | 4 / 110 / 0 / 1 |
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
