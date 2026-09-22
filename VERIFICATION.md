# VERIFICATION — line-by-line audit ledger

Generated `2026-09-22T23:43:29Z` at cycle 24. Read-only verifiers:
`python3 -m msl.cli verify-claims` and `python3 tools/probe_sources.py`.

## 1. Claim ledger composition

| Kind | Count | What it means |
|---|---|---|
| `captured` | 13,842 | A value lifted from a payload this project read |
| `documented` | 0 | A value from the operator's own published record |
| `negative` | 20 | Proof that something does **not** exist |
| `derived` | 7,085 | Arithmetic over claims above, formula recorded |
| **Total accepted** | **20,947** | |
| Rejected by the gate | 0 | Published, not swallowed |

## 2. Source registry

31 sources. `status` comes only from conclusive cycle/probe reads
recorded in the shared health ledger, never from a hand-written registry value.

| # | Id | Name | Operator | Status | Live reads | Last read (UTC) | HTTP | Links |
|---|---|---|---|---|---|---|---|---|
| 1 | `arxiv` | arXiv API | arXiv (Cornell University) | `verified-live-read` | 21 | 2026-09-22T23:43:29Z | 200 | [docs](https://info.arxiv.org/help/api/index.html) · [probe](https://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results=1) |
| 2 | `bls` | U.S. Bureau of Labor Statistics Public Data API v2 | U.S. Bureau of Labor Statistics | `verified-live-read` | 7 | 2026-09-22T17:31:33Z | 200 | [docs](https://www.bls.gov/developers/home.htm) · [probe](https://api.bls.gov/publicAPI/v2/timeseries/data/CUUR0000SA0) |
| 3 | `census_acs` | U.S. Census Bureau API (ACS 5-year) | U.S. Census Bureau | `verified-live-read` | 5 | 2026-09-22T23:43:29Z | 200 | [docs](https://www.census.gov/data/developers/data-sets.html) · [probe](https://api.census.gov/data/2022/acs/acs5?get=NAME,B01001_001E&for=state:06) |
| 4 | `clinicaltrials` | ClinicalTrials.gov API v2 | U.S. National Library of Medicine | `blocked` | 0 | 2026-09-22T23:43:29Z | 403 | [docs](https://clinicaltrials.gov/data-api/api) · [probe](https://clinicaltrials.gov/api/v2/studies?pageSize=1&countTotal=true&query.term=artificial%20intelligence) |
| 5 | `crossref` | Crossref REST API | Crossref | `verified-live-read` | 21 | 2026-09-22T23:43:29Z | 200 | [docs](https://www.crossref.org/documentation/retrieve-metadata/rest-api/) · [probe](https://api.crossref.org/works?rows=1&sort=created&order=desc) |
| 6 | `ecb_sdmx` | ECB Data Portal — SDMX REST (EXR daily) | European Central Bank | `verified-live-read` | 21 | 2026-09-22T23:43:29Z | 200 | [docs](https://data-explorer.ecb.europa.eu/) · [probe](https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A?lastNObservations=1&format=jsondata) |
| 7 | `europepmc` | Europe PMC REST | European Molecular Biology Laboratory | `verified-live-read` | 21 | 2026-09-22T23:43:29Z | 200 | [docs](https://europepmc.org/RestfulWebService) · [probe](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=artificial+intelligence&format=json&pageSize=1) |
| 8 | `federal_register` | Federal Register API v1 | U.S. National Archives / Office of the Federal Register | `verified-live-read` | 121 | 2026-09-22T23:43:29Z | 200 | [docs](https://www.federalregister.gov/developers/documentation/api/v1) · [probe](https://www.federalregister.gov/api/v1/documents.json?per_page=1&order=newest) |
| 9 | `frankfurter` | Frankfurter FX (ECB reference rates mirror) | Community service publishing ECB reference rates | `verified-live-read` | 21 | 2026-09-22T23:43:29Z | 200 | [docs](https://www.frankfurter.app/) · [probe](https://api.frankfurter.app/latest?from=USD&to=EUR,KRW) |
| 10 | `github_releases` | GitHub Releases API — newest release | GitHub, Inc. | `verified-live-read` | 24 | 2026-09-22T23:43:29Z | 200 | [docs](https://docs.github.com/en/rest/releases/releases#list-releases) · [probe](https://api.github.com/repos/buffedlizard55-lab/MasterSelfLearn/releases?per_page=1) |
| 11 | `github_repo` | GitHub Repos API — one repository | GitHub, Inc. | `verified-live-read` | 24 | 2026-09-22T23:43:29Z | 200 | [docs](https://docs.github.com/en/rest/repos/repos#get-a-repository) · [probe](https://api.github.com/repos/buffedlizard55-lab/MasterSelfLearn) |
| 12 | `github_repos` | GitHub Repos API — owner corpus | GitHub, Inc. | `verified-live-read` | 23 | 2026-09-22T23:43:29Z | 200 | [docs](https://docs.github.com/en/rest/repos/repos) · [probe](https://api.github.com/users/buffedlizard55-lab/repos?per_page=1) |
| 13 | `github_search` | GitHub Search API — repositories | GitHub, Inc. | `verified-live-read` | 102 | 2026-09-22T23:43:29Z | 200 | [docs](https://docs.github.com/en/rest/search/search) · [probe](https://api.github.com/search/repositories?q=created:%3E=2026-09-15&sort=stars&order=desc&per_page=1) |
| 14 | `hn_firebase` | Hacker News official Firebase API | Hacker News / Y Combinator | `verified-live-read` | 11 | 2026-09-22T23:43:29Z | 200 | [docs](https://github.com/HackerNews/API) · [probe](https://hacker-news.firebaseio.com/v0/topstories.json) |
| 15 | `huggingface` | Hugging Face Hub API | Hugging Face, Inc. | `verified-live-read` | 21 | 2026-09-22T23:43:29Z | 200 | [docs](https://huggingface.co/docs/hub/api) · [probe](https://huggingface.co/api/models?sort=trendingScore&limit=1) |
| 16 | `kalshi_public` | Kalshi public market data | KalshiEX LLC | `verified-live-read` | 21 | 2026-09-22T23:43:29Z | 200 | [docs](https://trading-api.readme.io/reference/getmarkets) · [probe](https://api.elections.kalshi.com/trade-api/v2/markets?limit=1) |
| 17 | `master_site_catalog` | MasterSite verified project catalog | buffedlizard55-lab, served by GitHub Contents API | `verified-live-read` | 4 | 2026-09-22T23:43:29Z | 200 | [docs](https://docs.github.com/en/rest/repos/contents#get-repository-content) · [probe](https://api.github.com/repos/buffedlizard55-lab/MasterSite/contents/data/sites.js) |
| 18 | `mlb_statsapi` | MLB StatsAPI — schedule | Major League Baseball Advanced Media | `verified-live-read` | 15 | 2026-09-22T23:43:29Z | 200 | [docs](https://statsapi.mlb.com/) · [probe](https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=2026-09-22) |
| 19 | `nba_cdn` | NBA CDN — today's scoreboard | National Basketball Association | `blocked` | 0 | 2026-09-22T23:43:29Z | 403 | [docs](https://cdn.nba.com/) · [probe](https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json) |
| 20 | `nhl_web` | NHL public web API — scoreboard | National Hockey League | `verified-live-read` | 11 | 2026-09-22T23:43:29Z | 200 | [docs](https://api-web.nhle.com/) · [probe](https://api-web.nhle.com/v1/scoreboard/now) |
| 21 | `nominatim` | OpenStreetMap Nominatim | OpenStreetMap Foundation | `verified-live-read` | 11 | 2026-09-22T23:43:29Z | 200 | [docs](https://nominatim.org/release-docs/latest/api/Search/) · [probe](https://nominatim.openstreetmap.org/search?q=Seoul&format=json&limit=1) |
| 22 | `npm_registry` | npm Registry — package metadata | GitHub, Inc. (npm) | `verified-live-read` | 13 | 2026-09-22T23:43:29Z | 200 | [docs](https://github.com/npm/registry) · [probe](https://registry.npmjs.org/next/latest) |
| 23 | `nws_alerts` | api.weather.gov — active alerts | U.S. National Weather Service (NOAA) | `verified-live-read` | 11 | 2026-09-22T23:43:29Z | 200 | [docs](https://www.weather.gov/documentation/services-web-api) · [probe](https://api.weather.gov/alerts/active?area=CA) |
| 24 | `openalex` | OpenAlex scholarly graph | OurResearch (open catalogue of scholarly works) | `verified-live-read` | 21 | 2026-09-22T23:43:29Z | 200 | [docs](https://docs.openalex.org/) · [probe](https://api.openalex.org/works?sort=publication_date:desc&per-page=1) |
| 25 | `pubmed` | NCBI PubMed E-utilities | U.S. National Library of Medicine | `verified-live-read` | 31 | 2026-09-22T23:43:29Z | 200 | [docs](https://www.ncbi.nlm.nih.gov/books/NBK25501/) · [probe](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=artificial+intelligence&retmax=1&retmode=json) |
| 26 | `pypi_json` | PyPI JSON API | Python Software Foundation | `verified-live-read` | 13 | 2026-09-22T23:43:29Z | 200 | [docs](https://docs.pypi.org/api/json/) · [probe](https://pypi.org/pypi/requests/json) |
| 27 | `sec_edgar` | SEC EDGAR — company submissions | U.S. Securities and Exchange Commission | `blocked` | 0 | 2026-09-22T23:43:29Z | 403 | [docs](https://www.sec.gov/edgar/sec-api-documentation) · [probe](https://data.sec.gov/submissions/CIK0000320193.json) |
| 28 | `stackexchange` | Stack Exchange API 2.3 | Stack Exchange, Inc. | `verified-live-read` | 21 | 2026-09-22T23:43:29Z | 200 | [docs](https://api.stackexchange.com/docs) · [probe](https://api.stackexchange.com/2.3/questions?order=desc&sort=votes&site=stackoverflow&pagesize=1) |
| 29 | `usgs_fdsn` | USGS Earthquake Hazards — FDSN event service | U.S. Geological Survey | `verified-live-read` | 16 | 2026-09-22T23:43:29Z | 200 | [docs](https://earthquake.usgs.gov/fdsnws/event/1/) · [probe](https://earthquake.usgs.gov/fdsnws/event/1/count?format=geojson&starttime=2026-09-15&endtime=2026-09-22&minmagnitude=5.0) |
| 30 | `wikimedia_pageviews` | Wikimedia Pageviews REST API | Wikimedia Foundation | `verified-live-read` | 17 | 2026-09-22T23:43:29Z | 200 | [docs](https://wikimedia.org/api/rest_v1/) · [probe](https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/Artificial_intelligence/daily/20260914/20260920) |
| 31 | `worldbank` | World Bank Open Data API | The World Bank | `verified-live-read` | 21 | 2026-09-22T23:43:29Z | 200 | [docs](https://datahelpdesk.worldbank.org/knowledgebase/articles/889392) · [probe](https://api.worldbank.org/v2/country/USA/indicator/NY.GDP.MKTP.CD?format=json&per_page=1) |

## 3. Most recent evidence rows

Every row is one outbound read, with the hash of what came back.

| Id | Source | HTTP | Captured (UTC) | SHA-256 (16) | Bytes | Capture mode | Integrity | URL |
|---|---|---|---|---|---|---|---|---|
| `E001056` | `federal_register` | 200 | 2026-09-22T23:43:29Z | `eaca7e365b385675` | 10,599 | `pipeline` | `wire` | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=model) |
| `E001057` | `federal_register` | 200 | 2026-09-22T23:43:29Z | `a4d7e27245ca01ea` | 9,710 | `pipeline` | `wire` | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=transformer) |
| `E001058` | `arxiv` | 200 | 2026-09-22T23:43:29Z | `93b2b7de353311ab` | 21,957 | `pipeline` | `wire` | [open](https://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results=8) |
| `E001059` | `openalex` | 200 | 2026-09-22T23:43:29Z | `c14bc3e95a3df548` | 76,265 | `pipeline` | `wire` | [open](https://api.openalex.org/works?sort=publication_date:desc&per-page=5&mailto=buffedlizard55@gmail.com) |
| `E001060` | `crossref` | 200 | 2026-09-22T23:43:29Z | `fd13fcb0a5e5bc2d` | 39,220 | `pipeline` | `wire` | [open](https://api.crossref.org/works?rows=3&sort=created&order=desc&mailto=buffedlizard55@gmail.com) |
| `E001061` | `europepmc` | 200 | 2026-09-22T23:43:29Z | `5b7ccd80b576fd6a` | 2,527 | `pipeline` | `wire` | [open](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=artificial+intelligence&format=json&pageSize=3) |
| `E001062` | `huggingface` | 200 | 2026-09-22T23:43:29Z | `c741e51ad44177b0` | 4,846 | `pipeline` | `wire` | [open](https://huggingface.co/api/models?sort=trendingScore&limit=10) |
| `E001063` | `github_search` | 200 | 2026-09-22T23:43:29Z | `ab4bee06f0be8ef5` | 108,716 | `pipeline` | `wire` | [open](https://api.github.com/search/repositories?q=agent%20created%3A%3E%3D2026-06-24&sort=stars&order=desc&per_page=20) |
| `E001064` | `github_search` | 200 | 2026-09-22T23:43:29Z | `21f8a66d3128ca41` | 111,138 | `pipeline` | `wire` | [open](https://api.github.com/search/repositories?q=framework%20created%3A%3E%3D2026-06-24&sort=stars&order=desc&per_page=20) |
| `E001065` | `github_search` | 200 | 2026-09-22T23:43:29Z | `f192751c971437dc` | 145,847 | `pipeline` | `wire` | [open](https://api.github.com/search/repositories?q=agent%20framework%20created%3A%3E%3D2026-09-15&sort=stars&order=desc&per_page=25) |
| `E001066` | `stackexchange` | 200 | 2026-09-22T23:43:29Z | `2995c1aa1e659453` | 3,795 | `pipeline` | `wire` | [open](https://api.stackexchange.com/2.3/questions?order=desc&sort=votes&site=stackoverflow&pagesize=5&tagged=python) |
| `E001067` | `federal_register` | 200 | 2026-09-22T23:43:29Z | `10be73fd28ead31e` | 10,393 | `pipeline` | `wire` | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=artificial%20intelligence) |
| `E001068` | `federal_register` | 200 | 2026-09-22T23:43:29Z | `4189e96a19401036` | 10,225 | `pipeline` | `wire` | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=health) |
| `E001069` | `federal_register` | 200 | 2026-09-22T23:43:29Z | `0f4c38bd793a8551` | 10,739 | `pipeline` | `wire` | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=energy) |
| `E001070` | `federal_register` | 200 | 2026-09-22T23:43:29Z | `3662c1cd8bf1e6da` | 10,937 | `pipeline` | `wire` | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=security) |
| `E001071` | `worldbank` | 200 | 2026-09-22T23:43:29Z | `f681cb8323b72c96` | 724 | `pipeline` | `wire` | [open](https://api.worldbank.org/v2/country/USA/indicator/NY.GDP.MKTP.CD?format=json&per_page=3) |
| `E001072` | `ecb_sdmx` | 200 | 2026-09-22T23:43:29Z | `b2db4c90250a1605` | 3,352 | `pipeline` | `wire` | [open](https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A?lastNObservations=3&format=jsondata) |
| `E001073` | `frankfurter` | 200 | 2026-09-22T23:43:29Z | `8d7063dd6f8c194b` | 98 | `pipeline` | `wire` | [open](https://api.frankfurter.app/latest?from=USD&to=EUR,KRW,JPY) |
| `E001074` | `usgs_fdsn` | 200 | 2026-09-22T23:43:29Z | `b32363a384488e56` | 31 | `pipeline` | `wire` | [open](https://earthquake.usgs.gov/fdsnws/event/1/count?format=geojson&starttime=2026-09-15&endtime=2026-09-22&minmagnitude=5.0) |
| `E001075` | `nws_alerts` | 200 | 2026-09-22T23:43:29Z | `20455a9b73e03d69` | 223 | `pipeline` | `wire` | [open](https://api.weather.gov/alerts/active?area=CA) |
| `E001076` | `pubmed` | 200 | 2026-09-22T23:43:29Z | `dc17f80f2f8f5bb1` | 798 | `pipeline` | `wire` | [open](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=trial&retmax=1&retmode=json) |
| `E001077` | `federal_register` | 200 | 2026-09-22T23:43:29Z | `126eb4408299a5fa` | 10,519 | `pipeline` | `wire` | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=public%20health) |
| `E001078` | `federal_register` | 200 | 2026-09-22T23:43:29Z | `5cbfd8ac9de93abd` | 11,216 | `pipeline` | `wire` | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=surveillance) |
| `E001079` | `federal_register` | 200 | 2026-09-22T23:43:29Z | `87eb19d32115a5fe` | 9,378 | `pipeline` | `wire` | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=data%20exchange) |
| `E001080` | `pubmed` | 200 | 2026-09-22T23:43:29Z | `b27ac5b524f47ade` | 783 | `pipeline` | `wire` | [open](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=cdc&retmax=1&retmode=json) |
| `E001081` | `kalshi_public` | 200 | 2026-09-22T23:43:29Z | `61030eb7bd71872a` | 22,109 | `pipeline` | `wire` | [open](https://api.elections.kalshi.com/trade-api/v2/markets?limit=5) |
| `E001082` | `mlb_statsapi` | 200 | 2026-09-22T23:43:29Z | `834e826636fa7cd6` | 20,731 | `pipeline` | `wire` | [open](https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=2026-09-22) |
| `E001083` | `nhl_web` | 200 | 2026-09-22T23:43:29Z | `7971bbdd64d6acc3` | 112,703 | `pipeline` | `wire` | [open](https://api-web.nhle.com/v1/scoreboard/now) |
| `E001084` | `github_search` | 200 | 2026-09-22T23:43:29Z | `f6cacf01d798c1f3` | 120,273 | `pipeline` | `wire` | [open](https://api.github.com/search/repositories?q=kalshi%20created%3A%3E%3D2026-06-24&sort=stars&order=desc&per_page=20) |
| `E001085` | `github_search` | 200 | 2026-09-22T23:43:29Z | `e19a8b686d856f4b` | 118,038 | `pipeline` | `wire` | [open](https://api.github.com/search/repositories?q=prediction%20market%20created%3A%3E%3D2026-06-24&sort=stars&order=desc&per_page=20) |
| `E001086` | `github_search` | 200 | 2026-09-22T23:43:29Z | `5e96bd94b1eba8e9` | 145,210 | `pipeline` | `wire` | [open](https://api.github.com/search/repositories?q=kalshi%20prediction%20market%20created%3A%3E%3D2026-09-15&sort=stars&order=desc&per_page=25) |
| `E001087` | `github_repos` | 200 | 2026-09-22T23:43:29Z | `fe6fd796db68e8b2` | 356,501 | `pipeline` | `wire` | [open](https://api.github.com/users/buffedlizard55-lab/repos?per_page=100&sort=updated) |
| `E001088` | `nominatim` | 200 | 2026-09-22T23:43:29Z | `b00a665917081ccf` | 438 | `pipeline` | `wire` | [open](https://nominatim.openstreetmap.org/search?q=Seoul&format=json&limit=1) |
| `E001089` | `wikimedia_pageviews` | 200 | 2026-09-22T23:43:29Z | `8e93bdbf2af1c096` | 1,138 | `pipeline` | `wire` | [open](https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/Artificial_intelligence/daily/20260914/20260920) |
| `E001090` | `github_repo` | 200 | 2026-09-22T23:43:29Z | `bcc0e3b4e6c921d8` | 6,564 | `pipeline` | `wire` | [open](https://api.github.com/repos/browser-use/jev-ultrafast) |
| `E001091` | `github_releases` | 200 | 2026-09-22T23:43:29Z | `4f53cda18c2baa0c` | 2 | `pipeline` | `wire` | [open](https://api.github.com/repos/browser-use/jev-ultrafast/releases?per_page=1) |
| `E001092` | `github_repo` | 200 | 2026-09-22T23:43:29Z | `1c1d8df42bc3d581` | 6,018 | `pipeline` | `wire` | [open](https://api.github.com/repos/zai-org/ZCode) |
| `E001093` | `github_releases` | 200 | 2026-09-22T23:43:29Z | `4f53cda18c2baa0c` | 2 | `pipeline` | `wire` | [open](https://api.github.com/repos/zai-org/ZCode/releases?per_page=1) |
| `E001094` | `github_repo` | 200 | 2026-09-22T23:43:29Z | `93b20032aea1ee16` | 5,500 | `pipeline` | `wire` | [open](https://api.github.com/repos/brayonpi/hexstellar) |
| `E001095` | `github_releases` | 200 | 2026-09-22T23:43:29Z | `2ab1e823c7832009` | 2,781 | `pipeline` | `wire` | [open](https://api.github.com/repos/brayonpi/hexstellar/releases?per_page=1) |
| `E001096` | `github_search` | 200 | 2026-09-22T23:43:29Z | `c8a4e6e3edf9bd29` | 5,559 | `pipeline` | `wire` | [open](https://api.github.com/search/repositories?q=created:%3E=2026-09-15&sort=stars&order=desc&per_page=1) |
| `E001097` | `github_repos` | 200 | 2026-09-22T23:43:29Z | `6ef46cea7e73bff1` | 5,494 | `pipeline` | `wire` | [open](https://api.github.com/users/buffedlizard55-lab/repos?per_page=1) |
| `E001098` | `github_repo` | 200 | 2026-09-22T23:43:29Z | `43e6de7f6d4813b1` | 5,824 | `pipeline` | `wire` | [open](https://api.github.com/repos/buffedlizard55-lab/MasterSelfLearn) |
| `E001099` | `github_releases` | 200 | 2026-09-22T23:43:29Z | `4f53cda18c2baa0c` | 2 | `pipeline` | `wire` | [open](https://api.github.com/repos/buffedlizard55-lab/MasterSelfLearn/releases?per_page=1) |
| `E001100` | `master_site_catalog` | 200 | 2026-09-22T23:43:29Z | `10ece627e9bebb5c` | 346,810 | `pipeline` | `wire` | [open](https://api.github.com/repos/buffedlizard55-lab/MasterSite/contents/data/sites.js) |
| `E001101` | `pypi_json` | 200 | 2026-09-22T23:43:29Z | `bcfc6a202592e4e9` | 192,973 | `pipeline` | `wire` | [open](https://pypi.org/pypi/requests/json) |
| `E001102` | `npm_registry` | 200 | 2026-09-22T23:43:29Z | `80fde3eccb93e473` | 3,069 | `pipeline` | `wire` | [open](https://registry.npmjs.org/next/latest) |
| `E001103` | `federal_register` | 200 | 2026-09-22T23:43:29Z | `d2b1771420a54c0b` | 31,543 | `pipeline` | `wire` | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=1&order=newest) |
| `E001104` | `hn_firebase` | 200 | 2026-09-22T23:43:29Z | `6212f2636c9cea5d` | 4,501 | `pipeline` | `wire` | [open](https://hacker-news.firebaseio.com/v0/topstories.json) |
| `E001105` | `arxiv` | 200 | 2026-09-22T23:43:29Z | `d177cfcafed1e2a9` | 4,225 | `pipeline` | `wire` | [open](https://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results=1) |
| `E001106` | `pubmed` | 200 | 2026-09-22T23:43:29Z | `8c20e0d5f913c730` | 509 | `pipeline` | `wire` | [open](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=artificial+intelligence&retmax=1&retmode=json) |
| `E001107` | `openalex` | 200 | 2026-09-22T23:43:29Z | `4f0f5de83a1a6ca6` | 15,259 | `pipeline` | `wire` | [open](https://api.openalex.org/works?sort=publication_date:desc&per-page=1) |
| `E001108` | `crossref` | 200 | 2026-09-22T23:43:29Z | `95989a7328e83a16` | 29,601 | `pipeline` | `wire` | [open](https://api.crossref.org/works?rows=1&sort=created&order=desc) |
| `E001109` | `stackexchange` | 200 | 2026-09-22T23:43:29Z | `eb411690718c5e6d` | 890 | `pipeline` | `wire` | [open](https://api.stackexchange.com/2.3/questions?order=desc&sort=votes&site=stackoverflow&pagesize=1) |
| `E001110` | `huggingface` | 200 | 2026-09-22T23:43:29Z | `5fb4128a8336d2fb` | 542 | `pipeline` | `wire` | [open](https://huggingface.co/api/models?sort=trendingScore&limit=1) |
| `E001111` | `worldbank` | 200 | 2026-09-22T23:43:29Z | `0302192ef40cbef6` | 302 | `pipeline` | `wire` | [open](https://api.worldbank.org/v2/country/USA/indicator/NY.GDP.MKTP.CD?format=json&per_page=1) |
| `E001112` | `ecb_sdmx` | 200 | 2026-09-22T23:43:29Z | `e1c0d0764bd0d87e` | 3,064 | `pipeline` | `wire` | [open](https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A?lastNObservations=1&format=jsondata) |
| `E001113` | `frankfurter` | 200 | 2026-09-22T23:43:29Z | `834d24f8f98686b0` | 85 | `pipeline` | `wire` | [open](https://api.frankfurter.app/latest?from=USD&to=EUR,KRW) |
| `E001114` | `europepmc` | 200 | 2026-09-22T23:43:29Z | `fa4457e0559588c5` | 1,037 | `pipeline` | `wire` | [open](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=artificial+intelligence&format=json&pageSize=1) |
| `E001115` | `kalshi_public` | 200 | 2026-09-22T23:43:29Z | `488811b1ba0e21e1` | 11,551 | `pipeline` | `wire` | [open](https://api.elections.kalshi.com/trade-api/v2/markets?limit=1) |

`wire` means SHA-256 covers the exact complete bytes handed to the adapter;
`projection` means only a canonical parsed projection was retained. Projection
rows remain usable legacy evidence but are never relabelled as wire-verifiable.

## 4. Library accounting

| | |
|---|---|
| Topics tracked | 157 |
| Topics with ≥1 claim row naming them (row-provable) | 133 |
| Topics with only pre-schema-v2 credit (not row-provable) | 19 |
| Topics with neither | 5 |
| Candidate / active / retired / blocked | 9 / 148 / 0 / 0 |
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
