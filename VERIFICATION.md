# VERIFICATION — line-by-line audit ledger

Generated `2026-09-23T12:54:12Z` at cycle 27. Read-only verifiers:
`python3 -m msl.cli verify-claims` and `python3 tools/probe_sources.py`.

## 1. Claim ledger composition

| Kind | Count | What it means |
|---|---|---|
| `captured` | 16,048 | A value lifted from a payload this project read |
| `documented` | 0 | A value from the operator's own published record |
| `negative` | 29 | Proof that something does **not** exist |
| `derived` | 8,316 | Arithmetic over claims above, formula recorded |
| **Total accepted** | **24,393** | |
| Rejected by the gate | 0 | Published, not swallowed |

## 2. Source registry

31 sources. `status` comes only from conclusive cycle/probe reads
recorded in the shared health ledger, never from a hand-written registry value.

| # | Id | Name | Operator | Status | Live reads | Last read (UTC) | HTTP | Links |
|---|---|---|---|---|---|---|---|---|
| 1 | `arxiv` | arXiv API | arXiv (Cornell University) | `verified-live-read` | 28 | 2026-09-23T12:54:12Z | 200 | [docs](https://info.arxiv.org/help/api/index.html) · [probe](https://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results=1) |
| 2 | `bls` | U.S. Bureau of Labor Statistics Public Data API v2 | U.S. Bureau of Labor Statistics | `verified-live-read` | 8 | 2026-09-23T09:57:44Z | 200 | [docs](https://www.bls.gov/developers/home.htm) · [probe](https://api.bls.gov/publicAPI/v2/timeseries/data/CUUR0000SA0) |
| 3 | `census_acs` | U.S. Census Bureau API (ACS 5-year) | U.S. Census Bureau | `verified-live-read` | 9 | 2026-09-23T12:54:12Z | 200 | [docs](https://www.census.gov/data/developers/data-sets.html) · [probe](https://api.census.gov/data/2022/acs/acs5?get=NAME,B01001_001E&for=state:06) |
| 4 | `clinicaltrials` | ClinicalTrials.gov API v2 | U.S. National Library of Medicine | `blocked` | 0 | 2026-09-23T12:54:12Z | 403 | [docs](https://clinicaltrials.gov/data-api/api) · [probe](https://clinicaltrials.gov/api/v2/studies?pageSize=1&countTotal=true&query.term=artificial%20intelligence) |
| 5 | `crossref` | Crossref REST API | Crossref | `verified-live-read` | 28 | 2026-09-23T12:54:12Z | 200 | [docs](https://www.crossref.org/documentation/retrieve-metadata/rest-api/) · [probe](https://api.crossref.org/works?rows=1&sort=created&order=desc) |
| 6 | `ecb_sdmx` | ECB Data Portal — SDMX REST (EXR daily) | European Central Bank | `verified-live-read` | 28 | 2026-09-23T12:54:12Z | 200 | [docs](https://data-explorer.ecb.europa.eu/) · [probe](https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A?lastNObservations=1&format=jsondata) |
| 7 | `europepmc` | Europe PMC REST | European Molecular Biology Laboratory | `verified-live-read` | 28 | 2026-09-23T12:54:12Z | 200 | [docs](https://europepmc.org/RestfulWebService) · [probe](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=artificial+intelligence&format=json&pageSize=1) |
| 8 | `federal_register` | Federal Register API v1 | U.S. National Archives / Office of the Federal Register | `verified-live-read` | 158 | 2026-09-23T12:54:12Z | 200 | [docs](https://www.federalregister.gov/developers/documentation/api/v1) · [probe](https://www.federalregister.gov/api/v1/documents.json?per_page=1&order=newest) |
| 9 | `frankfurter` | Frankfurter FX (ECB reference rates mirror) | Community service publishing ECB reference rates | `verified-live-read` | 28 | 2026-09-23T12:54:12Z | 200 | [docs](https://www.frankfurter.app/) · [probe](https://api.frankfurter.app/latest?from=USD&to=EUR,KRW) |
| 10 | `github_releases` | GitHub Releases API — newest release | GitHub, Inc. | `verified-live-read` | 37 | 2026-09-23T12:54:12Z | 200 | [docs](https://docs.github.com/en/rest/releases/releases#list-releases) · [probe](https://api.github.com/repos/buffedlizard55-lab/MasterSelfLearn/releases?per_page=1) |
| 11 | `github_repo` | GitHub Repos API — one repository | GitHub, Inc. | `verified-live-read` | 37 | 2026-09-23T12:54:12Z | 200 | [docs](https://docs.github.com/en/rest/repos/repos#get-a-repository) · [probe](https://api.github.com/repos/buffedlizard55-lab/MasterSelfLearn) |
| 12 | `github_repos` | GitHub Repos API — owner corpus | GitHub, Inc. | `verified-live-read` | 30 | 2026-09-23T12:54:12Z | 200 | [docs](https://docs.github.com/en/rest/repos/repos) · [probe](https://api.github.com/users/buffedlizard55-lab/repos?per_page=1) |
| 13 | `github_search` | GitHub Search API — repositories | GitHub, Inc. | `verified-live-read` | 124 | 2026-09-23T12:54:12Z | 200 | [docs](https://docs.github.com/en/rest/search/search) · [probe](https://api.github.com/search/repositories?q=created:%3E=2026-09-16&sort=stars&order=desc&per_page=1) |
| 14 | `hn_firebase` | Hacker News official Firebase API | Hacker News / Y Combinator | `verified-live-read` | 15 | 2026-09-23T12:54:12Z | 200 | [docs](https://github.com/HackerNews/API) · [probe](https://hacker-news.firebaseio.com/v0/topstories.json) |
| 15 | `huggingface` | Hugging Face Hub API | Hugging Face, Inc. | `verified-live-read` | 28 | 2026-09-23T12:54:12Z | 200 | [docs](https://huggingface.co/docs/hub/api) · [probe](https://huggingface.co/api/models?sort=trendingScore&limit=1) |
| 16 | `kalshi_public` | Kalshi public market data | KalshiEX LLC | `verified-live-read` | 28 | 2026-09-23T12:54:12Z | 200 | [docs](https://trading-api.readme.io/reference/getmarkets) · [probe](https://api.elections.kalshi.com/trade-api/v2/markets?limit=1) |
| 17 | `master_site_catalog` | MasterSite verified project catalog | buffedlizard55-lab, served by GitHub Contents API | `verified-live-read` | 8 | 2026-09-23T12:54:12Z | 200 | [docs](https://docs.github.com/en/rest/repos/contents#get-repository-content) · [probe](https://api.github.com/repos/buffedlizard55-lab/MasterSite/contents/data/sites.js) |
| 18 | `mlb_statsapi` | MLB StatsAPI — schedule | Major League Baseball Advanced Media | `verified-live-read` | 19 | 2026-09-23T12:54:12Z | 200 | [docs](https://statsapi.mlb.com/) · [probe](https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=2026-09-23) |
| 19 | `nba_cdn` | NBA CDN — today's scoreboard | National Basketball Association | `blocked` | 0 | 2026-09-23T12:54:12Z | 403 | [docs](https://cdn.nba.com/) · [probe](https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json) |
| 20 | `nhl_web` | NHL public web API — scoreboard | National Hockey League | `verified-live-read` | 15 | 2026-09-23T12:54:12Z | 200 | [docs](https://api-web.nhle.com/) · [probe](https://api-web.nhle.com/v1/scoreboard/now) |
| 21 | `nominatim` | OpenStreetMap Nominatim | OpenStreetMap Foundation | `verified-live-read` | 15 | 2026-09-23T12:54:12Z | 200 | [docs](https://nominatim.org/release-docs/latest/api/Search/) · [probe](https://nominatim.openstreetmap.org/search?q=Seoul&format=json&limit=1) |
| 22 | `npm_registry` | npm Registry — package metadata | GitHub, Inc. (npm) | `verified-live-read` | 17 | 2026-09-23T12:54:12Z | 200 | [docs](https://github.com/npm/registry) · [probe](https://registry.npmjs.org/next/latest) |
| 23 | `nws_alerts` | api.weather.gov — active alerts | U.S. National Weather Service (NOAA) | `verified-live-read` | 15 | 2026-09-23T12:54:12Z | 200 | [docs](https://www.weather.gov/documentation/services-web-api) · [probe](https://api.weather.gov/alerts/active?area=CA) |
| 24 | `openalex` | OpenAlex scholarly graph | OurResearch (open catalogue of scholarly works) | `verified-live-read` | 28 | 2026-09-23T12:54:12Z | 200 | [docs](https://docs.openalex.org/) · [probe](https://api.openalex.org/works?sort=publication_date:desc&per-page=1) |
| 25 | `pubmed` | NCBI PubMed E-utilities | U.S. National Library of Medicine | `verified-live-read` | 41 | 2026-09-23T12:54:12Z | 200 | [docs](https://www.ncbi.nlm.nih.gov/books/NBK25501/) · [probe](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=artificial+intelligence&retmax=1&retmode=json) |
| 26 | `pypi_json` | PyPI JSON API | Python Software Foundation | `verified-live-read` | 17 | 2026-09-23T12:54:12Z | 200 | [docs](https://docs.pypi.org/api/json/) · [probe](https://pypi.org/pypi/requests/json) |
| 27 | `sec_edgar` | SEC EDGAR — company submissions | U.S. Securities and Exchange Commission | `blocked` | 0 | 2026-09-23T12:54:12Z | 403 | [docs](https://www.sec.gov/edgar/sec-api-documentation) · [probe](https://data.sec.gov/submissions/CIK0000320193.json) |
| 28 | `stackexchange` | Stack Exchange API 2.3 | Stack Exchange, Inc. | `verified-live-read` | 28 | 2026-09-23T12:54:12Z | 200 | [docs](https://api.stackexchange.com/docs) · [probe](https://api.stackexchange.com/2.3/questions?order=desc&sort=votes&site=stackoverflow&pagesize=1) |
| 29 | `usgs_fdsn` | USGS Earthquake Hazards — FDSN event service | U.S. Geological Survey | `verified-live-read` | 20 | 2026-09-23T12:54:12Z | 200 | [docs](https://earthquake.usgs.gov/fdsnws/event/1/) · [probe](https://earthquake.usgs.gov/fdsnws/event/1/count?format=geojson&starttime=2026-09-16&endtime=2026-09-23&minmagnitude=5.0) |
| 30 | `wikimedia_pageviews` | Wikimedia Pageviews REST API | Wikimedia Foundation | `verified-live-read` | 24 | 2026-09-23T12:54:12Z | 200 | [docs](https://wikimedia.org/api/rest_v1/) · [probe](https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/Artificial_intelligence/daily/20260914/20260920) |
| 31 | `worldbank` | World Bank Open Data API | The World Bank | `verified-live-read` | 28 | 2026-09-23T12:54:12Z | 200 | [docs](https://datahelpdesk.worldbank.org/knowledgebase/articles/889392) · [probe](https://api.worldbank.org/v2/country/USA/indicator/NY.GDP.MKTP.CD?format=json&per_page=1) |

## 3. Most recent evidence rows

Every row is one outbound read, with the hash of what came back.

| Id | Source | HTTP | Captured (UTC) | SHA-256 (16) | Bytes | Capture mode | Integrity | URL |
|---|---|---|---|---|---|---|---|---|
| `E001245` | `federal_register` | 200 | 2026-09-23T12:54:12Z | `a4d7e27245ca01ea` | 9,710 | `pipeline` | `wire` | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=transformer) |
| `E001246` | `arxiv` | 200 | 2026-09-23T12:54:12Z | `7772f41ee1dc2a16` | 22,364 | `pipeline` | `wire` | [open](https://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results=8) |
| `E001247` | `openalex` | 200 | 2026-09-23T12:54:12Z | `afc3e61a68bb11e4` | 76,265 | `pipeline` | `wire` | [open](https://api.openalex.org/works?sort=publication_date:desc&per-page=5&mailto=buffedlizard55@gmail.com) |
| `E001248` | `crossref` | 200 | 2026-09-23T12:54:12Z | `f5ab655cd675dfa4` | 11,299 | `pipeline` | `wire` | [open](https://api.crossref.org/works?rows=3&sort=created&order=desc&mailto=buffedlizard55@gmail.com) |
| `E001249` | `europepmc` | 200 | 2026-09-23T12:54:12Z | `46109a46a60e0119` | 2,545 | `pipeline` | `wire` | [open](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=artificial+intelligence&format=json&pageSize=3) |
| `E001250` | `huggingface` | 200 | 2026-09-23T12:54:12Z | `1b659d1939d0f0c6` | 4,822 | `pipeline` | `wire` | [open](https://huggingface.co/api/models?sort=trendingScore&limit=10) |
| `E001251` | `github_search` | 200 | 2026-09-23T12:54:12Z | `eaeba187d1af0c43` | 108,716 | `pipeline` | `wire` | [open](https://api.github.com/search/repositories?q=agent%20created%3A%3E%3D2026-06-25&sort=stars&order=desc&per_page=20) |
| `E001252` | `github_search` | 200 | 2026-09-23T12:54:12Z | `bbd1c804f9dbfa4a` | 110,657 | `pipeline` | `wire` | [open](https://api.github.com/search/repositories?q=framework%20created%3A%3E%3D2026-06-25&sort=stars&order=desc&per_page=20) |
| `E001253` | `github_search` | 200 | 2026-09-23T12:54:12Z | `d89bbc91d5fd511b` | 143,007 | `pipeline` | `wire` | [open](https://api.github.com/search/repositories?q=agent%20framework%20created%3A%3E%3D2026-09-16&sort=stars&order=desc&per_page=25) |
| `E001254` | `stackexchange` | 200 | 2026-09-23T12:54:12Z | `a3dc9f71c8c76c25` | 3,795 | `pipeline` | `wire` | [open](https://api.stackexchange.com/2.3/questions?order=desc&sort=votes&site=stackoverflow&pagesize=5&tagged=python) |
| `E001255` | `federal_register` | 200 | 2026-09-23T12:54:12Z | `10be73fd28ead31e` | 10,393 | `pipeline` | `wire` | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=artificial%20intelligence) |
| `E001256` | `federal_register` | 200 | 2026-09-23T12:54:12Z | `81063172d1603f3f` | 13,795 | `pipeline` | `wire` | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=health) |
| `E001257` | `federal_register` | 200 | 2026-09-23T12:54:12Z | `82d27e541bc22b9a` | 10,234 | `pipeline` | `wire` | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=energy) |
| `E001258` | `federal_register` | 200 | 2026-09-23T12:54:12Z | `9fac4845be174d47` | 12,729 | `pipeline` | `wire` | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=security) |
| `E001259` | `worldbank` | 200 | 2026-09-23T12:54:12Z | `f681cb8323b72c96` | 724 | `pipeline` | `wire` | [open](https://api.worldbank.org/v2/country/USA/indicator/NY.GDP.MKTP.CD?format=json&per_page=3) |
| `E001260` | `ecb_sdmx` | 200 | 2026-09-23T12:54:12Z | `89caffbb6eb08e94` | 3,352 | `pipeline` | `wire` | [open](https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A?lastNObservations=3&format=jsondata) |
| `E001261` | `frankfurter` | 200 | 2026-09-23T12:54:12Z | `8d7063dd6f8c194b` | 98 | `pipeline` | `wire` | [open](https://api.frankfurter.app/latest?from=USD&to=EUR,KRW,JPY) |
| `E001262` | `usgs_fdsn` | 200 | 2026-09-23T12:54:12Z | `1ce6807aff2bce3d` | 31 | `pipeline` | `wire` | [open](https://earthquake.usgs.gov/fdsnws/event/1/count?format=geojson&starttime=2026-09-16&endtime=2026-09-23&minmagnitude=5.0) |
| `E001263` | `nws_alerts` | 200 | 2026-09-23T12:54:12Z | `60173e31532af1ae` | 223 | `pipeline` | `wire` | [open](https://api.weather.gov/alerts/active?area=CA) |
| `E001264` | `pubmed` | 200 | 2026-09-23T12:54:12Z | `5a9f67394cefc10d` | 798 | `pipeline` | `wire` | [open](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=trial&retmax=1&retmode=json) |
| `E001265` | `federal_register` | 200 | 2026-09-23T12:54:12Z | `75ceb45785bc4842` | 14,065 | `pipeline` | `wire` | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=public%20health) |
| `E001266` | `federal_register` | 200 | 2026-09-23T12:54:12Z | `dbfaa004cdf49425` | 11,092 | `pipeline` | `wire` | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=surveillance) |
| `E001267` | `federal_register` | 200 | 2026-09-23T12:54:12Z | `9cb5d5106dea9fc5` | 11,353 | `pipeline` | `wire` | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=data%20exchange) |
| `E001268` | `pubmed` | 200 | 2026-09-23T12:54:12Z | `bfd0c02e0cd64501` | 783 | `pipeline` | `wire` | [open](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=cdc&retmax=1&retmode=json) |
| `E001269` | `kalshi_public` | 200 | 2026-09-23T12:54:12Z | `0f144885d87e35b7` | 22,427 | `pipeline` | `wire` | [open](https://api.elections.kalshi.com/trade-api/v2/markets?limit=5) |
| `E001270` | `mlb_statsapi` | 200 | 2026-09-23T12:54:12Z | `8121c030bec01316` | 20,323 | `pipeline` | `wire` | [open](https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=2026-09-23) |
| `E001271` | `nhl_web` | 200 | 2026-09-23T12:54:12Z | `d88c0b5e4f955e90` | 111,534 | `pipeline` | `wire` | [open](https://api-web.nhle.com/v1/scoreboard/now) |
| `E001272` | `github_search` | 200 | 2026-09-23T12:54:12Z | `a5e0a13522884845` | 119,799 | `pipeline` | `wire` | [open](https://api.github.com/search/repositories?q=kalshi%20created%3A%3E%3D2026-06-25&sort=stars&order=desc&per_page=20) |
| `E001273` | `github_search` | 200 | 2026-09-23T12:54:12Z | `d56c9ab92fd1cd71` | 118,038 | `pipeline` | `wire` | [open](https://api.github.com/search/repositories?q=prediction%20market%20created%3A%3E%3D2026-06-25&sort=stars&order=desc&per_page=20) |
| `E001274` | `github_search` | 200 | 2026-09-23T12:54:12Z | `ee0b0348c7dd0b89` | 145,523 | `pipeline` | `wire` | [open](https://api.github.com/search/repositories?q=kalshi%20prediction%20market%20created%3A%3E%3D2026-09-16&sort=stars&order=desc&per_page=25) |
| `E001275` | `github_repos` | 200 | 2026-09-23T12:54:12Z | `d44292cad75700af` | 362,446 | `pipeline` | `wire` | [open](https://api.github.com/users/buffedlizard55-lab/repos?per_page=100&sort=updated) |
| `E001276` | `nominatim` | 200 | 2026-09-23T12:54:12Z | `b00a665917081ccf` | 438 | `pipeline` | `wire` | [open](https://nominatim.openstreetmap.org/search?q=Seoul&format=json&limit=1) |
| `E001277` | `wikimedia_pageviews` | 200 | 2026-09-23T12:54:12Z | `99e147390f895ad2` | 1,138 | `pipeline` | `wire` | [open](https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/Artificial_intelligence/daily/20260915/20260921) |
| `E001278` | `github_repo` | 200 | 2026-09-23T12:54:12Z | `73e090e39e56e12d` | 6,564 | `pipeline` | `wire` | [open](https://api.github.com/repos/browser-use/jev-ultrafast) |
| `E001279` | `github_releases` | 200 | 2026-09-23T12:54:12Z | `4f53cda18c2baa0c` | 2 | `pipeline` | `wire` | [open](https://api.github.com/repos/browser-use/jev-ultrafast/releases?per_page=1) |
| `E001280` | `github_repo` | 200 | 2026-09-23T12:54:12Z | `15ab85368a75afa3` | 6,018 | `pipeline` | `wire` | [open](https://api.github.com/repos/zai-org/ZCode) |
| `E001281` | `github_releases` | 200 | 2026-09-23T12:54:12Z | `4f53cda18c2baa0c` | 2 | `pipeline` | `wire` | [open](https://api.github.com/repos/zai-org/ZCode/releases?per_page=1) |
| `E001282` | `github_repo` | 200 | 2026-09-23T12:54:12Z | `e3da67ebab5f72ab` | 5,500 | `pipeline` | `wire` | [open](https://api.github.com/repos/brayonpi/hexstellar) |
| `E001283` | `github_releases` | 200 | 2026-09-23T12:54:12Z | `2ab1e823c7832009` | 2,781 | `pipeline` | `wire` | [open](https://api.github.com/repos/brayonpi/hexstellar/releases?per_page=1) |
| `E001284` | `github_search` | 200 | 2026-09-23T12:54:12Z | `e0750d1f86820f88` | 5,655 | `pipeline` | `wire` | [open](https://api.github.com/search/repositories?q=created:%3E=2026-09-16&sort=stars&order=desc&per_page=1) |
| `E001285` | `github_repos` | 200 | 2026-09-23T12:54:12Z | `6ef46cea7e73bff1` | 5,494 | `pipeline` | `wire` | [open](https://api.github.com/users/buffedlizard55-lab/repos?per_page=1) |
| `E001286` | `github_repo` | 200 | 2026-09-23T12:54:12Z | `e3226780bf906ec8` | 5,825 | `pipeline` | `wire` | [open](https://api.github.com/repos/buffedlizard55-lab/MasterSelfLearn) |
| `E001287` | `github_releases` | 200 | 2026-09-23T12:54:12Z | `4f53cda18c2baa0c` | 2 | `pipeline` | `wire` | [open](https://api.github.com/repos/buffedlizard55-lab/MasterSelfLearn/releases?per_page=1) |
| `E001288` | `master_site_catalog` | 200 | 2026-09-23T12:54:12Z | `3128ea8ac19c752f` | 605,326 | `pipeline` | `wire` | [open](https://api.github.com/repos/buffedlizard55-lab/MasterSite/contents/data/sites.js) |
| `E001289` | `pypi_json` | 200 | 2026-09-23T12:54:12Z | `bcfc6a202592e4e9` | 192,973 | `pipeline` | `wire` | [open](https://pypi.org/pypi/requests/json) |
| `E001290` | `npm_registry` | 200 | 2026-09-23T12:54:12Z | `80fde3eccb93e473` | 3,069 | `pipeline` | `wire` | [open](https://registry.npmjs.org/next/latest) |
| `E001291` | `wikimedia_pageviews` | 200 | 2026-09-23T12:54:12Z | `8e93bdbf2af1c096` | 1,138 | `pipeline` | `wire` | [open](https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/Artificial_intelligence/daily/20260914/20260920) |
| `E001292` | `federal_register` | 200 | 2026-09-23T12:54:12Z | `ffdf2e8a04550d19` | 35,960 | `pipeline` | `wire` | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=1&order=newest) |
| `E001293` | `hn_firebase` | 200 | 2026-09-23T12:54:12Z | `fb0632873821ee26` | 4,501 | `pipeline` | `wire` | [open](https://hacker-news.firebaseio.com/v0/topstories.json) |
| `E001294` | `arxiv` | 200 | 2026-09-23T12:54:12Z | `d9605dd1d2824e15` | 3,800 | `pipeline` | `wire` | [open](https://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results=1) |
| `E001295` | `pubmed` | 200 | 2026-09-23T12:54:12Z | `831b2989eb1c2870` | 509 | `pipeline` | `wire` | [open](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=artificial+intelligence&retmax=1&retmode=json) |
| `E001296` | `openalex` | 200 | 2026-09-23T12:54:12Z | `97b98bd48bb5d07f` | 15,259 | `pipeline` | `wire` | [open](https://api.openalex.org/works?sort=publication_date:desc&per-page=1) |
| `E001297` | `crossref` | 200 | 2026-09-23T12:54:12Z | `4f2fd7e337353ee0` | 1,136 | `pipeline` | `wire` | [open](https://api.crossref.org/works?rows=1&sort=created&order=desc) |
| `E001298` | `stackexchange` | 200 | 2026-09-23T12:54:12Z | `8932866b49db4ea7` | 890 | `pipeline` | `wire` | [open](https://api.stackexchange.com/2.3/questions?order=desc&sort=votes&site=stackoverflow&pagesize=1) |
| `E001299` | `huggingface` | 200 | 2026-09-23T12:54:12Z | `9aa46f2a23640019` | 542 | `pipeline` | `wire` | [open](https://huggingface.co/api/models?sort=trendingScore&limit=1) |
| `E001300` | `worldbank` | 200 | 2026-09-23T12:54:12Z | `0302192ef40cbef6` | 302 | `pipeline` | `wire` | [open](https://api.worldbank.org/v2/country/USA/indicator/NY.GDP.MKTP.CD?format=json&per_page=1) |
| `E001301` | `ecb_sdmx` | 200 | 2026-09-23T12:54:12Z | `e1c0d0764bd0d87e` | 3,064 | `pipeline` | `wire` | [open](https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A?lastNObservations=1&format=jsondata) |
| `E001302` | `frankfurter` | 200 | 2026-09-23T12:54:12Z | `834d24f8f98686b0` | 85 | `pipeline` | `wire` | [open](https://api.frankfurter.app/latest?from=USD&to=EUR,KRW) |
| `E001303` | `europepmc` | 200 | 2026-09-23T12:54:12Z | `97b14ab7f0148cfc` | 1,100 | `pipeline` | `wire` | [open](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=artificial+intelligence&format=json&pageSize=1) |
| `E001304` | `kalshi_public` | 200 | 2026-09-23T12:54:12Z | `5cf47c1256d1be0e` | 2,609 | `pipeline` | `wire` | [open](https://api.elections.kalshi.com/trade-api/v2/markets?limit=1) |

`wire` means SHA-256 covers the exact complete bytes handed to the adapter;
`projection` means only a canonical parsed projection was retained. Projection
rows remain usable legacy evidence but are never relabelled as wire-verifiable.

## 4. Library accounting

| | |
|---|---|
| Topics tracked | 175 |
| Topics with ≥1 claim row naming them (row-provable) | 151 |
| Topics with only pre-schema-v2 credit (not row-provable) | 19 |
| Topics with neither | 5 |
| Candidate / active / retired / blocked | 7 / 168 / 0 / 0 |
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
