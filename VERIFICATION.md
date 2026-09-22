# VERIFICATION — line-by-line audit ledger

Generated `2026-09-22T23:28:37Z` at cycle 23. Read-only verifiers:
`python3 -m msl.cli verify-claims` and `python3 tools/probe_sources.py`.

## 1. Claim ledger composition

| Kind | Count | What it means |
|---|---|---|
| `captured` | 13,121 | A value lifted from a payload this project read |
| `documented` | 0 | A value from the operator's own published record |
| `negative` | 17 | Proof that something does **not** exist |
| `derived` | 6,713 | Arithmetic over claims above, formula recorded |
| **Total accepted** | **19,851** | |
| Rejected by the gate | 0 | Published, not swallowed |

## 2. Source registry

31 sources. `status` comes only from conclusive cycle/probe reads
recorded in the shared health ledger, never from a hand-written registry value.

| # | Id | Name | Operator | Status | Live reads | Last read (UTC) | HTTP | Links |
|---|---|---|---|---|---|---|---|---|
| 1 | `arxiv` | arXiv API | arXiv (Cornell University) | `verified-live-read` | 19 | 2026-09-22T23:28:37Z | 200 | [docs](https://info.arxiv.org/help/api/index.html) · [probe](https://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results=1) |
| 2 | `bls` | U.S. Bureau of Labor Statistics Public Data API v2 | U.S. Bureau of Labor Statistics | `verified-live-read` | 7 | 2026-09-22T17:31:33Z | 200 | [docs](https://www.bls.gov/developers/home.htm) · [probe](https://api.bls.gov/publicAPI/v2/timeseries/data/CUUR0000SA0) |
| 3 | `census_acs` | U.S. Census Bureau API (ACS 5-year) | U.S. Census Bureau | `verified-live-read` | 4 | 2026-09-22T23:28:37Z | 200 | [docs](https://www.census.gov/data/developers/data-sets.html) · [probe](https://api.census.gov/data/2022/acs/acs5?get=NAME,B01001_001E&for=state:06) |
| 4 | `clinicaltrials` | ClinicalTrials.gov API v2 | U.S. National Library of Medicine | `blocked` | 0 | 2026-09-22T23:28:37Z | 403 | [docs](https://clinicaltrials.gov/data-api/api) · [probe](https://clinicaltrials.gov/api/v2/studies?pageSize=1&countTotal=true&query.term=artificial%20intelligence) |
| 5 | `crossref` | Crossref REST API | Crossref | `verified-live-read` | 19 | 2026-09-22T23:28:37Z | 200 | [docs](https://www.crossref.org/documentation/retrieve-metadata/rest-api/) · [probe](https://api.crossref.org/works?rows=1&sort=created&order=desc) |
| 6 | `ecb_sdmx` | ECB Data Portal — SDMX REST (EXR daily) | European Central Bank | `verified-live-read` | 19 | 2026-09-22T23:28:37Z | 200 | [docs](https://data-explorer.ecb.europa.eu/) · [probe](https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A?lastNObservations=1&format=jsondata) |
| 7 | `europepmc` | Europe PMC REST | European Molecular Biology Laboratory | `verified-live-read` | 19 | 2026-09-22T23:28:37Z | 200 | [docs](https://europepmc.org/RestfulWebService) · [probe](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=artificial+intelligence&format=json&pageSize=1) |
| 8 | `federal_register` | Federal Register API v1 | U.S. National Archives / Office of the Federal Register | `verified-live-read` | 109 | 2026-09-22T23:28:37Z | 200 | [docs](https://www.federalregister.gov/developers/documentation/api/v1) · [probe](https://www.federalregister.gov/api/v1/documents.json?per_page=1&order=newest) |
| 9 | `frankfurter` | Frankfurter FX (ECB reference rates mirror) | Community service publishing ECB reference rates | `verified-live-read` | 19 | 2026-09-22T23:28:37Z | 200 | [docs](https://www.frankfurter.app/) · [probe](https://api.frankfurter.app/latest?from=USD&to=EUR,KRW) |
| 10 | `github_releases` | GitHub Releases API — newest release | GitHub, Inc. | `verified-live-read` | 20 | 2026-09-22T23:28:37Z | 200 | [docs](https://docs.github.com/en/rest/releases/releases#list-releases) · [probe](https://api.github.com/repos/buffedlizard55-lab/MasterSelfLearn/releases?per_page=1) |
| 11 | `github_repo` | GitHub Repos API — one repository | GitHub, Inc. | `verified-live-read` | 20 | 2026-09-22T23:28:37Z | 200 | [docs](https://docs.github.com/en/rest/repos/repos#get-a-repository) · [probe](https://api.github.com/repos/buffedlizard55-lab/MasterSelfLearn) |
| 12 | `github_repos` | GitHub Repos API — owner corpus | GitHub, Inc. | `verified-live-read` | 21 | 2026-09-22T23:28:37Z | 200 | [docs](https://docs.github.com/en/rest/repos/repos) · [probe](https://api.github.com/users/buffedlizard55-lab/repos?per_page=1) |
| 13 | `github_search` | GitHub Search API — repositories | GitHub, Inc. | `verified-live-read` | 95 | 2026-09-22T23:28:37Z | 200 | [docs](https://docs.github.com/en/rest/search/search) · [probe](https://api.github.com/search/repositories?q=created:%3E=2026-09-15&sort=stars&order=desc&per_page=1) |
| 14 | `hn_firebase` | Hacker News official Firebase API | Hacker News / Y Combinator | `verified-live-read` | 10 | 2026-09-22T23:28:37Z | 200 | [docs](https://github.com/HackerNews/API) · [probe](https://hacker-news.firebaseio.com/v0/topstories.json) |
| 15 | `huggingface` | Hugging Face Hub API | Hugging Face, Inc. | `verified-live-read` | 19 | 2026-09-22T23:28:37Z | 200 | [docs](https://huggingface.co/docs/hub/api) · [probe](https://huggingface.co/api/models?sort=trendingScore&limit=1) |
| 16 | `kalshi_public` | Kalshi public market data | KalshiEX LLC | `verified-live-read` | 19 | 2026-09-22T23:28:37Z | 200 | [docs](https://trading-api.readme.io/reference/getmarkets) · [probe](https://api.elections.kalshi.com/trade-api/v2/markets?limit=1) |
| 17 | `master_site_catalog` | MasterSite verified project catalog | buffedlizard55-lab, served by GitHub Contents API | `verified-live-read` | 3 | 2026-09-22T23:28:37Z | 200 | [docs](https://docs.github.com/en/rest/repos/contents#get-repository-content) · [probe](https://api.github.com/repos/buffedlizard55-lab/MasterSite/contents/data/sites.js) |
| 18 | `mlb_statsapi` | MLB StatsAPI — schedule | Major League Baseball Advanced Media | `verified-live-read` | 14 | 2026-09-22T23:28:37Z | 200 | [docs](https://statsapi.mlb.com/) · [probe](https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=2026-09-22) |
| 19 | `nba_cdn` | NBA CDN — today's scoreboard | National Basketball Association | `blocked` | 0 | 2026-09-22T23:28:37Z | 403 | [docs](https://cdn.nba.com/) · [probe](https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json) |
| 20 | `nhl_web` | NHL public web API — scoreboard | National Hockey League | `verified-live-read` | 10 | 2026-09-22T23:28:37Z | 200 | [docs](https://api-web.nhle.com/) · [probe](https://api-web.nhle.com/v1/scoreboard/now) |
| 21 | `nominatim` | OpenStreetMap Nominatim | OpenStreetMap Foundation | `verified-live-read` | 10 | 2026-09-22T23:28:37Z | 200 | [docs](https://nominatim.org/release-docs/latest/api/Search/) · [probe](https://nominatim.openstreetmap.org/search?q=Seoul&format=json&limit=1) |
| 22 | `npm_registry` | npm Registry — package metadata | GitHub, Inc. (npm) | `verified-live-read` | 12 | 2026-09-22T23:28:37Z | 200 | [docs](https://github.com/npm/registry) · [probe](https://registry.npmjs.org/next/latest) |
| 23 | `nws_alerts` | api.weather.gov — active alerts | U.S. National Weather Service (NOAA) | `verified-live-read` | 10 | 2026-09-22T23:28:37Z | 200 | [docs](https://www.weather.gov/documentation/services-web-api) · [probe](https://api.weather.gov/alerts/active?area=CA) |
| 24 | `openalex` | OpenAlex scholarly graph | OurResearch (open catalogue of scholarly works) | `verified-live-read` | 19 | 2026-09-22T23:28:37Z | 200 | [docs](https://docs.openalex.org/) · [probe](https://api.openalex.org/works?sort=publication_date:desc&per-page=1) |
| 25 | `pubmed` | NCBI PubMed E-utilities | U.S. National Library of Medicine | `verified-live-read` | 28 | 2026-09-22T23:28:37Z | 200 | [docs](https://www.ncbi.nlm.nih.gov/books/NBK25501/) · [probe](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=artificial+intelligence&retmax=1&retmode=json) |
| 26 | `pypi_json` | PyPI JSON API | Python Software Foundation | `verified-live-read` | 12 | 2026-09-22T23:28:37Z | 200 | [docs](https://docs.pypi.org/api/json/) · [probe](https://pypi.org/pypi/requests/json) |
| 27 | `sec_edgar` | SEC EDGAR — company submissions | U.S. Securities and Exchange Commission | `blocked` | 0 | 2026-09-22T23:28:37Z | 403 | [docs](https://www.sec.gov/edgar/sec-api-documentation) · [probe](https://data.sec.gov/submissions/CIK0000320193.json) |
| 28 | `stackexchange` | Stack Exchange API 2.3 | Stack Exchange, Inc. | `verified-live-read` | 19 | 2026-09-22T23:28:37Z | 200 | [docs](https://api.stackexchange.com/docs) · [probe](https://api.stackexchange.com/2.3/questions?order=desc&sort=votes&site=stackoverflow&pagesize=1) |
| 29 | `usgs_fdsn` | USGS Earthquake Hazards — FDSN event service | U.S. Geological Survey | `verified-live-read` | 15 | 2026-09-22T23:28:37Z | 200 | [docs](https://earthquake.usgs.gov/fdsnws/event/1/) · [probe](https://earthquake.usgs.gov/fdsnws/event/1/count?format=geojson&starttime=2026-09-15&endtime=2026-09-22&minmagnitude=5.0) |
| 30 | `wikimedia_pageviews` | Wikimedia Pageviews REST API | Wikimedia Foundation | `verified-live-read` | 16 | 2026-09-22T23:28:37Z | 200 | [docs](https://wikimedia.org/api/rest_v1/) · [probe](https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/Artificial_intelligence/daily/20260914/20260920) |
| 31 | `worldbank` | World Bank Open Data API | The World Bank | `verified-live-read` | 19 | 2026-09-22T23:28:37Z | 200 | [docs](https://datahelpdesk.worldbank.org/knowledgebase/articles/889392) · [probe](https://api.worldbank.org/v2/country/USA/indicator/NY.GDP.MKTP.CD?format=json&per_page=1) |

## 3. Most recent evidence rows

Every row is one outbound read, with the hash of what came back.

| Id | Source | HTTP | Captured (UTC) | SHA-256 (16) | Bytes | Capture mode | Integrity | URL |
|---|---|---|---|---|---|---|---|---|
| `E000994` | `master_site_catalog` | 200 | 2026-09-22T23:28:37Z | `10ece627e9bebb5c` | 346,810 | `pipeline` | `wire` | [open](https://api.github.com/repos/buffedlizard55-lab/MasterSite/contents/data/sites.js) |
| `E000995` | `pypi_json` | 200 | 2026-09-22T23:28:37Z | `bcfc6a202592e4e9` | 192,973 | `pipeline` | `wire` | [open](https://pypi.org/pypi/requests/json) |
| `E000996` | `npm_registry` | 200 | 2026-09-22T23:28:37Z | `80fde3eccb93e473` | 3,069 | `pipeline` | `wire` | [open](https://registry.npmjs.org/next/latest) |
| `E000997` | `wikimedia_pageviews` | 200 | 2026-09-22T23:28:37Z | `8e93bdbf2af1c096` | 1,138 | `pipeline` | `wire` | [open](https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/Artificial_intelligence/daily/20260914/20260920) |
| `E000998` | `federal_register` | 200 | 2026-09-22T23:28:37Z | `d2b1771420a54c0b` | 31,543 | `pipeline` | `wire` | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=1&order=newest) |
| `E000999` | `usgs_fdsn` | 200 | 2026-09-22T23:28:37Z | `7af87b8f6b9ef606` | 31 | `pipeline` | `wire` | [open](https://earthquake.usgs.gov/fdsnws/event/1/count?format=geojson&starttime=2026-09-14&minmagnitude=5.0) |
| `E001000` | `hn_firebase` | 200 | 2026-09-22T23:28:37Z | `ec5b20d01e8daedf` | 4,501 | `pipeline` | `wire` | [open](https://hacker-news.firebaseio.com/v0/topstories.json) |
| `E001001` | `arxiv` | 200 | 2026-09-22T23:28:37Z | `d177cfcafed1e2a9` | 4,225 | `pipeline` | `wire` | [open](https://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results=1) |
| `E001002` | `pubmed` | 200 | 2026-09-22T23:28:37Z | `8c20e0d5f913c730` | 509 | `pipeline` | `wire` | [open](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=artificial+intelligence&retmax=1&retmode=json) |
| `E001003` | `openalex` | 200 | 2026-09-22T23:28:37Z | `6f9107637c1fc03d` | 15,259 | `pipeline` | `wire` | [open](https://api.openalex.org/works?sort=publication_date:desc&per-page=1) |
| `E001004` | `crossref` | 200 | 2026-09-22T23:28:37Z | `f0db5f75278fb520` | 29,601 | `pipeline` | `wire` | [open](https://api.crossref.org/works?rows=1&sort=created&order=desc) |
| `E001005` | `stackexchange` | 200 | 2026-09-22T23:28:37Z | `d339a567659ff105` | 890 | `pipeline` | `wire` | [open](https://api.stackexchange.com/2.3/questions?order=desc&sort=votes&site=stackoverflow&pagesize=1) |
| `E001006` | `huggingface` | 200 | 2026-09-22T23:28:37Z | `6b068b77e8472931` | 542 | `pipeline` | `wire` | [open](https://huggingface.co/api/models?sort=trendingScore&limit=1) |
| `E001007` | `nws_alerts` | 200 | 2026-09-22T23:28:37Z | `dbb585f05b285c27` | 223 | `pipeline` | `wire` | [open](https://api.weather.gov/alerts/active?area=CA) |
| `E001008` | `worldbank` | 200 | 2026-09-22T23:28:37Z | `0302192ef40cbef6` | 302 | `pipeline` | `wire` | [open](https://api.worldbank.org/v2/country/USA/indicator/NY.GDP.MKTP.CD?format=json&per_page=1) |
| `E001009` | `ecb_sdmx` | 200 | 2026-09-22T23:28:37Z | `e1c0d0764bd0d87e` | 3,064 | `pipeline` | `wire` | [open](https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A?lastNObservations=1&format=jsondata) |
| `E001010` | `frankfurter` | 200 | 2026-09-22T23:28:37Z | `834d24f8f98686b0` | 85 | `pipeline` | `wire` | [open](https://api.frankfurter.app/latest?from=USD&to=EUR,KRW) |
| `E001011` | `nominatim` | 200 | 2026-09-22T23:28:37Z | `c3956b8645345cb5` | 438 | `pipeline` | `wire` | [open](https://nominatim.openstreetmap.org/search?q=Seoul&format=json&limit=1) |
| `E001012` | `europepmc` | 200 | 2026-09-22T23:28:37Z | `05abd390a6dc2665` | 1,037 | `pipeline` | `wire` | [open](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=artificial+intelligence&format=json&pageSize=1) |
| `E001013` | `kalshi_public` | 200 | 2026-09-22T23:28:37Z | `1615c01cb658f151` | 4,410 | `pipeline` | `wire` | [open](https://api.elections.kalshi.com/trade-api/v2/markets?limit=1) |
| `E001014` | `mlb_statsapi` | 200 | 2026-09-22T23:28:37Z | `53eb2b692aaa9796` | 19,843 | `pipeline` | `wire` | [open](https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=2026-09-20) |
| `E001015` | `nhl_web` | 200 | 2026-09-22T23:28:37Z | `64f0594d3bbad741` | 112,704 | `pipeline` | `wire` | [open](https://api-web.nhle.com/v1/scoreboard/now) |
| `E001016` | `federal_register` | 200 | 2026-09-22T23:28:37Z | `6bba10768fba59a8` | 11,100 | `pipeline` | `wire` | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=reasoning) |
| `E001017` | `federal_register` | 200 | 2026-09-22T23:28:37Z | `4bdcbe8b20a6704e` | 9,490 | `pipeline` | `wire` | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=agent) |
| `E001018` | `federal_register` | 200 | 2026-09-22T23:28:37Z | `eaca7e365b385675` | 10,599 | `pipeline` | `wire` | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=model) |
| `E001019` | `federal_register` | 200 | 2026-09-22T23:28:37Z | `a4d7e27245ca01ea` | 9,710 | `pipeline` | `wire` | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=transformer) |
| `E001020` | `arxiv` | 200 | 2026-09-22T23:28:37Z | `93b2b7de353311ab` | 21,957 | `pipeline` | `wire` | [open](https://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results=8) |
| `E001021` | `openalex` | 200 | 2026-09-22T23:28:37Z | `8b2ccde67080eef3` | 76,265 | `pipeline` | `wire` | [open](https://api.openalex.org/works?sort=publication_date:desc&per-page=5&mailto=buffedlizard55@gmail.com) |
| `E001022` | `crossref` | 200 | 2026-09-22T23:28:37Z | `228beb11d9b12796` | 39,220 | `pipeline` | `wire` | [open](https://api.crossref.org/works?rows=3&sort=created&order=desc&mailto=buffedlizard55@gmail.com) |
| `E001023` | `europepmc` | 200 | 2026-09-22T23:28:37Z | `6417c45aae878ff7` | 17 | `pipeline` | `wire` | [open](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=artificial+intelligence&format=json&pageSize=3) |
| `E001024` | `huggingface` | 200 | 2026-09-22T23:28:37Z | `42052357090c7972` | 4,846 | `pipeline` | `wire` | [open](https://huggingface.co/api/models?sort=trendingScore&limit=10) |
| `E001025` | `github_search` | 200 | 2026-09-22T23:28:37Z | `1efd00c43c44ea37` | 108,716 | `pipeline` | `wire` | [open](https://api.github.com/search/repositories?q=agent%20created%3A%3E%3D2026-06-24&sort=stars&order=desc&per_page=20) |
| `E001026` | `github_search` | 200 | 2026-09-22T23:28:37Z | `b9d0e156248970a1` | 111,138 | `pipeline` | `wire` | [open](https://api.github.com/search/repositories?q=framework%20created%3A%3E%3D2026-06-24&sort=stars&order=desc&per_page=20) |
| `E001027` | `github_search` | 200 | 2026-09-22T23:28:37Z | `46d5416282fa858d` | 145,847 | `pipeline` | `wire` | [open](https://api.github.com/search/repositories?q=agent%20framework%20created%3A%3E%3D2026-09-15&sort=stars&order=desc&per_page=25) |
| `E001028` | `stackexchange` | 200 | 2026-09-22T23:28:37Z | `10a2a875d717bf0a` | 3,795 | `pipeline` | `wire` | [open](https://api.stackexchange.com/2.3/questions?order=desc&sort=votes&site=stackoverflow&pagesize=5&tagged=python) |
| `E001029` | `federal_register` | 200 | 2026-09-22T23:28:37Z | `10be73fd28ead31e` | 10,393 | `pipeline` | `wire` | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=artificial%20intelligence) |
| `E001030` | `federal_register` | 200 | 2026-09-22T23:28:37Z | `4189e96a19401036` | 10,225 | `pipeline` | `wire` | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=health) |
| `E001031` | `federal_register` | 200 | 2026-09-22T23:28:37Z | `0f4c38bd793a8551` | 10,739 | `pipeline` | `wire` | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=energy) |
| `E001032` | `federal_register` | 200 | 2026-09-22T23:28:37Z | `3662c1cd8bf1e6da` | 10,937 | `pipeline` | `wire` | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=security) |
| `E001033` | `worldbank` | 200 | 2026-09-22T23:28:37Z | `f681cb8323b72c96` | 724 | `pipeline` | `wire` | [open](https://api.worldbank.org/v2/country/USA/indicator/NY.GDP.MKTP.CD?format=json&per_page=3) |
| `E001034` | `ecb_sdmx` | 200 | 2026-09-22T23:28:37Z | `b2db4c90250a1605` | 3,352 | `pipeline` | `wire` | [open](https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A?lastNObservations=3&format=jsondata) |
| `E001035` | `frankfurter` | 200 | 2026-09-22T23:28:37Z | `8d7063dd6f8c194b` | 98 | `pipeline` | `wire` | [open](https://api.frankfurter.app/latest?from=USD&to=EUR,KRW,JPY) |
| `E001036` | `usgs_fdsn` | 200 | 2026-09-22T23:28:37Z | `28aa33c7803ef1e2` | 31 | `pipeline` | `wire` | [open](https://earthquake.usgs.gov/fdsnws/event/1/count?format=geojson&starttime=2026-09-15&endtime=2026-09-22&minmagnitude=5.0) |
| `E001037` | `pubmed` | 200 | 2026-09-22T23:28:37Z | `dc17f80f2f8f5bb1` | 798 | `pipeline` | `wire` | [open](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=trial&retmax=1&retmode=json) |
| `E001038` | `federal_register` | 200 | 2026-09-22T23:28:37Z | `126eb4408299a5fa` | 10,519 | `pipeline` | `wire` | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=public%20health) |
| `E001039` | `federal_register` | 200 | 2026-09-22T23:28:37Z | `5cbfd8ac9de93abd` | 11,216 | `pipeline` | `wire` | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=surveillance) |
| `E001040` | `federal_register` | 200 | 2026-09-22T23:28:37Z | `87eb19d32115a5fe` | 9,378 | `pipeline` | `wire` | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=data%20exchange) |
| `E001041` | `pubmed` | 200 | 2026-09-22T23:28:37Z | `b27ac5b524f47ade` | 783 | `pipeline` | `wire` | [open](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=cdc&retmax=1&retmode=json) |
| `E001042` | `kalshi_public` | 200 | 2026-09-22T23:28:37Z | `01d566d8e1b4dc54` | 16,496 | `pipeline` | `wire` | [open](https://api.elections.kalshi.com/trade-api/v2/markets?limit=5) |
| `E001043` | `mlb_statsapi` | 200 | 2026-09-22T23:28:37Z | `1f1da1057a916b24` | 20,723 | `pipeline` | `wire` | [open](https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=2026-09-22) |
| `E001044` | `github_search` | 200 | 2026-09-22T23:28:37Z | `3ae30a8133bf939b` | 120,273 | `pipeline` | `wire` | [open](https://api.github.com/search/repositories?q=kalshi%20created%3A%3E%3D2026-06-24&sort=stars&order=desc&per_page=20) |
| `E001045` | `github_search` | 200 | 2026-09-22T23:28:37Z | `4d5b8f33f295032f` | 118,038 | `pipeline` | `wire` | [open](https://api.github.com/search/repositories?q=prediction%20market%20created%3A%3E%3D2026-06-24&sort=stars&order=desc&per_page=20) |
| `E001046` | `github_search` | 200 | 2026-09-22T23:28:37Z | `ec37518f88e4d093` | 145,210 | `pipeline` | `wire` | [open](https://api.github.com/search/repositories?q=kalshi%20prediction%20market%20created%3A%3E%3D2026-09-15&sort=stars&order=desc&per_page=25) |
| `E001047` | `github_repos` | 200 | 2026-09-22T23:28:37Z | `e115bbfaa50ed56f` | 356,501 | `pipeline` | `wire` | [open](https://api.github.com/users/buffedlizard55-lab/repos?per_page=100&sort=updated) |
| `E001048` | `github_repo` | 200 | 2026-09-22T23:28:37Z | `01e2ebe8a72012d6` | 6,564 | `pipeline` | `wire` | [open](https://api.github.com/repos/browser-use/jev-ultrafast) |
| `E001049` | `github_releases` | 200 | 2026-09-22T23:28:37Z | `4f53cda18c2baa0c` | 2 | `pipeline` | `wire` | [open](https://api.github.com/repos/browser-use/jev-ultrafast/releases?per_page=1) |
| `E001050` | `github_repo` | 200 | 2026-09-22T23:28:37Z | `4e9474eb7ca3f3f9` | 6,018 | `pipeline` | `wire` | [open](https://api.github.com/repos/zai-org/ZCode) |
| `E001051` | `github_releases` | 200 | 2026-09-22T23:28:37Z | `4f53cda18c2baa0c` | 2 | `pipeline` | `wire` | [open](https://api.github.com/repos/zai-org/ZCode/releases?per_page=1) |
| `E001052` | `github_repo` | 200 | 2026-09-22T23:28:37Z | `d69d031bde3b41b9` | 5,500 | `pipeline` | `wire` | [open](https://api.github.com/repos/brayonpi/hexstellar) |
| `E001053` | `github_releases` | 200 | 2026-09-22T23:28:37Z | `2ab1e823c7832009` | 2,781 | `pipeline` | `wire` | [open](https://api.github.com/repos/brayonpi/hexstellar/releases?per_page=1) |

`wire` means SHA-256 covers the exact complete bytes handed to the adapter;
`projection` means only a canonical parsed projection was retained. Projection
rows remain usable legacy evidence but are never relabelled as wire-verifiable.

## 4. Library accounting

| | |
|---|---|
| Topics tracked | 151 |
| Topics with ≥1 claim row naming them (row-provable) | 125 |
| Topics with only pre-schema-v2 credit (not row-provable) | 19 |
| Topics with neither | 7 |
| Candidate / active / retired / blocked | 11 / 139 / 0 / 1 |
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
