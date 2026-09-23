# VERIFICATION — line-by-line audit ledger

Generated `2026-09-23T07:19:33Z` at cycle 26. Read-only verifiers:
`python3 -m msl.cli verify-claims` and `python3 tools/probe_sources.py`.

## 1. Claim ledger composition

| Kind | Count | What it means |
|---|---|---|
| `captured` | 15,309 | A value lifted from a payload this project read |
| `documented` | 0 | A value from the operator's own published record |
| `negative` | 26 | Proof that something does **not** exist |
| `derived` | 7,885 | Arithmetic over claims above, formula recorded |
| **Total accepted** | **23,220** | |
| Rejected by the gate | 0 | Published, not swallowed |

## 2. Source registry

31 sources. `status` comes only from conclusive cycle/probe reads
recorded in the shared health ledger, never from a hand-written registry value.

| # | Id | Name | Operator | Status | Live reads | Last read (UTC) | HTTP | Links |
|---|---|---|---|---|---|---|---|---|
| 1 | `arxiv` | arXiv API | arXiv (Cornell University) | `verified-live-read` | 25 | 2026-09-23T07:19:33Z | 200 | [docs](https://info.arxiv.org/help/api/index.html) · [probe](https://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results=1) |
| 2 | `bls` | U.S. Bureau of Labor Statistics Public Data API v2 | U.S. Bureau of Labor Statistics | `verified-live-read` | 7 | 2026-09-22T17:31:33Z | 200 | [docs](https://www.bls.gov/developers/home.htm) · [probe](https://api.bls.gov/publicAPI/v2/timeseries/data/CUUR0000SA0) |
| 3 | `census_acs` | U.S. Census Bureau API (ACS 5-year) | U.S. Census Bureau | `verified-live-read` | 7 | 2026-09-23T07:19:33Z | 200 | [docs](https://www.census.gov/data/developers/data-sets.html) · [probe](https://api.census.gov/data/2022/acs/acs5?get=NAME,B01001_001E&for=state:06) |
| 4 | `clinicaltrials` | ClinicalTrials.gov API v2 | U.S. National Library of Medicine | `blocked` | 0 | 2026-09-23T07:19:33Z | 403 | [docs](https://clinicaltrials.gov/data-api/api) · [probe](https://clinicaltrials.gov/api/v2/studies?pageSize=1&countTotal=true&query.term=artificial%20intelligence) |
| 5 | `crossref` | Crossref REST API | Crossref | `verified-live-read` | 25 | 2026-09-23T07:19:33Z | 200 | [docs](https://www.crossref.org/documentation/retrieve-metadata/rest-api/) · [probe](https://api.crossref.org/works?rows=1&sort=created&order=desc) |
| 6 | `ecb_sdmx` | ECB Data Portal — SDMX REST (EXR daily) | European Central Bank | `verified-live-read` | 25 | 2026-09-23T07:19:33Z | 200 | [docs](https://data-explorer.ecb.europa.eu/) · [probe](https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A?lastNObservations=1&format=jsondata) |
| 7 | `europepmc` | Europe PMC REST | European Molecular Biology Laboratory | `verified-live-read` | 25 | 2026-09-23T07:19:33Z | 200 | [docs](https://europepmc.org/RestfulWebService) · [probe](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=artificial+intelligence&format=json&pageSize=1) |
| 8 | `federal_register` | Federal Register API v1 | U.S. National Archives / Office of the Federal Register | `verified-live-read` | 145 | 2026-09-23T07:19:33Z | 200 | [docs](https://www.federalregister.gov/developers/documentation/api/v1) · [probe](https://www.federalregister.gov/api/v1/documents.json?per_page=1&order=newest) |
| 9 | `frankfurter` | Frankfurter FX (ECB reference rates mirror) | Community service publishing ECB reference rates | `verified-live-read` | 25 | 2026-09-23T07:19:33Z | 200 | [docs](https://www.frankfurter.app/) · [probe](https://api.frankfurter.app/latest?from=USD&to=EUR,KRW) |
| 10 | `github_releases` | GitHub Releases API — newest release | GitHub, Inc. | `verified-live-read` | 32 | 2026-09-23T07:19:33Z | 200 | [docs](https://docs.github.com/en/rest/releases/releases#list-releases) · [probe](https://api.github.com/repos/buffedlizard55-lab/MasterSelfLearn/releases?per_page=1) |
| 11 | `github_repo` | GitHub Repos API — one repository | GitHub, Inc. | `verified-live-read` | 32 | 2026-09-23T07:19:33Z | 200 | [docs](https://docs.github.com/en/rest/repos/repos#get-a-repository) · [probe](https://api.github.com/repos/buffedlizard55-lab/MasterSelfLearn) |
| 12 | `github_repos` | GitHub Repos API — owner corpus | GitHub, Inc. | `verified-live-read` | 27 | 2026-09-23T07:19:33Z | 200 | [docs](https://docs.github.com/en/rest/repos/repos) · [probe](https://api.github.com/users/buffedlizard55-lab/repos?per_page=1) |
| 13 | `github_search` | GitHub Search API — repositories | GitHub, Inc. | `verified-live-read` | 116 | 2026-09-23T07:19:33Z | 200 | [docs](https://docs.github.com/en/rest/search/search) · [probe](https://api.github.com/search/repositories?q=created:%3E=2026-09-16&sort=stars&order=desc&per_page=1) |
| 14 | `hn_firebase` | Hacker News official Firebase API | Hacker News / Y Combinator | `verified-live-read` | 13 | 2026-09-23T07:19:33Z | 200 | [docs](https://github.com/HackerNews/API) · [probe](https://hacker-news.firebaseio.com/v0/topstories.json) |
| 15 | `huggingface` | Hugging Face Hub API | Hugging Face, Inc. | `verified-live-read` | 25 | 2026-09-23T07:19:33Z | 200 | [docs](https://huggingface.co/docs/hub/api) · [probe](https://huggingface.co/api/models?sort=trendingScore&limit=1) |
| 16 | `kalshi_public` | Kalshi public market data | KalshiEX LLC | `verified-live-read` | 25 | 2026-09-23T07:19:33Z | 200 | [docs](https://trading-api.readme.io/reference/getmarkets) · [probe](https://api.elections.kalshi.com/trade-api/v2/markets?limit=1) |
| 17 | `master_site_catalog` | MasterSite verified project catalog | buffedlizard55-lab, served by GitHub Contents API | `verified-live-read` | 6 | 2026-09-23T07:19:33Z | 200 | [docs](https://docs.github.com/en/rest/repos/contents#get-repository-content) · [probe](https://api.github.com/repos/buffedlizard55-lab/MasterSite/contents/data/sites.js) |
| 18 | `mlb_statsapi` | MLB StatsAPI — schedule | Major League Baseball Advanced Media | `verified-live-read` | 17 | 2026-09-23T07:19:33Z | 200 | [docs](https://statsapi.mlb.com/) · [probe](https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=2026-09-23) |
| 19 | `nba_cdn` | NBA CDN — today's scoreboard | National Basketball Association | `blocked` | 0 | 2026-09-23T07:19:33Z | 403 | [docs](https://cdn.nba.com/) · [probe](https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json) |
| 20 | `nhl_web` | NHL public web API — scoreboard | National Hockey League | `verified-live-read` | 13 | 2026-09-23T07:19:33Z | 200 | [docs](https://api-web.nhle.com/) · [probe](https://api-web.nhle.com/v1/scoreboard/now) |
| 21 | `nominatim` | OpenStreetMap Nominatim | OpenStreetMap Foundation | `verified-live-read` | 13 | 2026-09-23T07:19:33Z | 200 | [docs](https://nominatim.org/release-docs/latest/api/Search/) · [probe](https://nominatim.openstreetmap.org/search?q=Seoul&format=json&limit=1) |
| 22 | `npm_registry` | npm Registry — package metadata | GitHub, Inc. (npm) | `verified-live-read` | 15 | 2026-09-23T07:19:33Z | 200 | [docs](https://github.com/npm/registry) · [probe](https://registry.npmjs.org/next/latest) |
| 23 | `nws_alerts` | api.weather.gov — active alerts | U.S. National Weather Service (NOAA) | `verified-live-read` | 13 | 2026-09-23T07:19:33Z | 200 | [docs](https://www.weather.gov/documentation/services-web-api) · [probe](https://api.weather.gov/alerts/active?area=CA) |
| 24 | `openalex` | OpenAlex scholarly graph | OurResearch (open catalogue of scholarly works) | `verified-live-read` | 25 | 2026-09-23T07:19:33Z | 200 | [docs](https://docs.openalex.org/) · [probe](https://api.openalex.org/works?sort=publication_date:desc&per-page=1) |
| 25 | `pubmed` | NCBI PubMed E-utilities | U.S. National Library of Medicine | `verified-live-read` | 37 | 2026-09-23T07:19:33Z | 200 | [docs](https://www.ncbi.nlm.nih.gov/books/NBK25501/) · [probe](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=artificial+intelligence&retmax=1&retmode=json) |
| 26 | `pypi_json` | PyPI JSON API | Python Software Foundation | `verified-live-read` | 15 | 2026-09-23T07:19:33Z | 200 | [docs](https://docs.pypi.org/api/json/) · [probe](https://pypi.org/pypi/requests/json) |
| 27 | `sec_edgar` | SEC EDGAR — company submissions | U.S. Securities and Exchange Commission | `blocked` | 0 | 2026-09-23T07:19:33Z | 403 | [docs](https://www.sec.gov/edgar/sec-api-documentation) · [probe](https://data.sec.gov/submissions/CIK0000320193.json) |
| 28 | `stackexchange` | Stack Exchange API 2.3 | Stack Exchange, Inc. | `verified-live-read` | 25 | 2026-09-23T07:19:33Z | 200 | [docs](https://api.stackexchange.com/docs) · [probe](https://api.stackexchange.com/2.3/questions?order=desc&sort=votes&site=stackoverflow&pagesize=1) |
| 29 | `usgs_fdsn` | USGS Earthquake Hazards — FDSN event service | U.S. Geological Survey | `verified-live-read` | 18 | 2026-09-23T07:19:33Z | 200 | [docs](https://earthquake.usgs.gov/fdsnws/event/1/) · [probe](https://earthquake.usgs.gov/fdsnws/event/1/count?format=geojson&starttime=2026-09-16&endtime=2026-09-23&minmagnitude=5.0) |
| 30 | `wikimedia_pageviews` | Wikimedia Pageviews REST API | Wikimedia Foundation | `verified-live-read` | 21 | 2026-09-23T07:19:33Z | 200 | [docs](https://wikimedia.org/api/rest_v1/) · [probe](https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/Artificial_intelligence/daily/20260914/20260920) |
| 31 | `worldbank` | World Bank Open Data API | The World Bank | `verified-live-read` | 25 | 2026-09-23T07:19:33Z | 200 | [docs](https://datahelpdesk.worldbank.org/knowledgebase/articles/889392) · [probe](https://api.worldbank.org/v2/country/USA/indicator/NY.GDP.MKTP.CD?format=json&per_page=1) |

## 3. Most recent evidence rows

Every row is one outbound read, with the hash of what came back.

| Id | Source | HTTP | Captured (UTC) | SHA-256 (16) | Bytes | Capture mode | Integrity | URL |
|---|---|---|---|---|---|---|---|---|
| `E001182` | `federal_register` | 200 | 2026-09-23T07:19:33Z | `a4d7e27245ca01ea` | 9,710 | `pipeline` | `wire` | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=transformer) |
| `E001183` | `arxiv` | 200 | 2026-09-23T07:19:33Z | `e2931d5c6e99d046` | 22,364 | `pipeline` | `wire` | [open](https://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results=8) |
| `E001184` | `openalex` | 200 | 2026-09-23T07:19:33Z | `10e99895e9e3bebe` | 76,265 | `pipeline` | `wire` | [open](https://api.openalex.org/works?sort=publication_date:desc&per-page=5&mailto=buffedlizard55@gmail.com) |
| `E001185` | `crossref` | 200 | 2026-09-23T07:19:33Z | `303f10b5e33a1c15` | 36,095 | `pipeline` | `wire` | [open](https://api.crossref.org/works?rows=3&sort=created&order=desc&mailto=buffedlizard55@gmail.com) |
| `E001186` | `europepmc` | 200 | 2026-09-23T07:19:33Z | `5f7cfc8f99f6fd6e` | 2,545 | `pipeline` | `wire` | [open](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=artificial+intelligence&format=json&pageSize=3) |
| `E001187` | `huggingface` | 200 | 2026-09-23T07:19:33Z | `2278eea7251c3990` | 4,847 | `pipeline` | `wire` | [open](https://huggingface.co/api/models?sort=trendingScore&limit=10) |
| `E001188` | `github_search` | 200 | 2026-09-23T07:19:33Z | `881ba0571246ec8c` | 108,714 | `pipeline` | `wire` | [open](https://api.github.com/search/repositories?q=agent%20created%3A%3E%3D2026-06-25&sort=stars&order=desc&per_page=20) |
| `E001189` | `github_search` | 200 | 2026-09-23T07:19:33Z | `5a44852017e876b8` | 110,655 | `pipeline` | `wire` | [open](https://api.github.com/search/repositories?q=framework%20created%3A%3E%3D2026-06-25&sort=stars&order=desc&per_page=20) |
| `E001190` | `github_search` | 200 | 2026-09-23T07:19:33Z | `e8ebe1f8ea54c216` | 145,728 | `pipeline` | `wire` | [open](https://api.github.com/search/repositories?q=agent%20framework%20created%3A%3E%3D2026-09-16&sort=stars&order=desc&per_page=25) |
| `E001191` | `stackexchange` | 200 | 2026-09-23T07:19:33Z | `a5616ed67d664c61` | 3,795 | `pipeline` | `wire` | [open](https://api.stackexchange.com/2.3/questions?order=desc&sort=votes&site=stackoverflow&pagesize=5&tagged=python) |
| `E001192` | `federal_register` | 200 | 2026-09-23T07:19:33Z | `10be73fd28ead31e` | 10,393 | `pipeline` | `wire` | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=artificial%20intelligence) |
| `E001193` | `federal_register` | 200 | 2026-09-23T07:19:33Z | `4189e96a19401036` | 10,225 | `pipeline` | `wire` | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=health) |
| `E001194` | `federal_register` | 200 | 2026-09-23T07:19:33Z | `0f4c38bd793a8551` | 10,739 | `pipeline` | `wire` | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=energy) |
| `E001195` | `federal_register` | 200 | 2026-09-23T07:19:33Z | `3662c1cd8bf1e6da` | 10,937 | `pipeline` | `wire` | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=security) |
| `E001196` | `worldbank` | 200 | 2026-09-23T07:19:33Z | `f681cb8323b72c96` | 724 | `pipeline` | `wire` | [open](https://api.worldbank.org/v2/country/USA/indicator/NY.GDP.MKTP.CD?format=json&per_page=3) |
| `E001197` | `ecb_sdmx` | 200 | 2026-09-23T07:19:33Z | `b61c872bf4bcc8f9` | 3,352 | `pipeline` | `wire` | [open](https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A?lastNObservations=3&format=jsondata) |
| `E001198` | `frankfurter` | 200 | 2026-09-23T07:19:33Z | `8d7063dd6f8c194b` | 98 | `pipeline` | `wire` | [open](https://api.frankfurter.app/latest?from=USD&to=EUR,KRW,JPY) |
| `E001199` | `usgs_fdsn` | 200 | 2026-09-23T07:19:33Z | `1ce6807aff2bce3d` | 31 | `pipeline` | `wire` | [open](https://earthquake.usgs.gov/fdsnws/event/1/count?format=geojson&starttime=2026-09-16&endtime=2026-09-23&minmagnitude=5.0) |
| `E001200` | `nws_alerts` | 200 | 2026-09-23T07:19:33Z | `c1fceda807a65b5b` | 223 | `pipeline` | `wire` | [open](https://api.weather.gov/alerts/active?area=CA) |
| `E001201` | `pubmed` | 200 | 2026-09-23T07:19:33Z | `2a8868d603b8627f` | 798 | `pipeline` | `wire` | [open](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=trial&retmax=1&retmode=json) |
| `E001202` | `federal_register` | 200 | 2026-09-23T07:19:33Z | `126eb4408299a5fa` | 10,519 | `pipeline` | `wire` | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=public%20health) |
| `E001203` | `federal_register` | 200 | 2026-09-23T07:19:33Z | `5cbfd8ac9de93abd` | 11,216 | `pipeline` | `wire` | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=surveillance) |
| `E001204` | `federal_register` | 200 | 2026-09-23T07:19:33Z | `87eb19d32115a5fe` | 9,378 | `pipeline` | `wire` | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=data%20exchange) |
| `E001205` | `pubmed` | 200 | 2026-09-23T07:19:33Z | `c809505ac53ea959` | 783 | `pipeline` | `wire` | [open](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=cdc&retmax=1&retmode=json) |
| `E001206` | `kalshi_public` | 200 | 2026-09-23T07:19:33Z | `fedd4f1dd2fd4faa` | 18,209 | `pipeline` | `wire` | [open](https://api.elections.kalshi.com/trade-api/v2/markets?limit=5) |
| `E001207` | `mlb_statsapi` | 200 | 2026-09-23T07:19:33Z | `8121c030bec01316` | 20,323 | `pipeline` | `wire` | [open](https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=2026-09-23) |
| `E001208` | `nhl_web` | 200 | 2026-09-23T07:19:33Z | `d88c0b5e4f955e90` | 111,534 | `pipeline` | `wire` | [open](https://api-web.nhle.com/v1/scoreboard/now) |
| `E001209` | `github_search` | 200 | 2026-09-23T07:19:33Z | `0d39c2a4af14011a` | 120,273 | `pipeline` | `wire` | [open](https://api.github.com/search/repositories?q=kalshi%20created%3A%3E%3D2026-06-25&sort=stars&order=desc&per_page=20) |
| `E001210` | `github_search` | 200 | 2026-09-23T07:19:33Z | `c55d49c37a02f10f` | 118,038 | `pipeline` | `wire` | [open](https://api.github.com/search/repositories?q=prediction%20market%20created%3A%3E%3D2026-06-25&sort=stars&order=desc&per_page=20) |
| `E001211` | `github_search` | 200 | 2026-09-23T07:19:33Z | `d50c27e3ec8f00c3` | 145,523 | `pipeline` | `wire` | [open](https://api.github.com/search/repositories?q=kalshi%20prediction%20market%20created%3A%3E%3D2026-09-16&sort=stars&order=desc&per_page=25) |
| `E001212` | `github_repos` | 200 | 2026-09-23T07:19:33Z | `3e2d9d21dde8b51a` | 362,446 | `pipeline` | `wire` | [open](https://api.github.com/users/buffedlizard55-lab/repos?per_page=100&sort=updated) |
| `E001213` | `nominatim` | 200 | 2026-09-23T07:19:33Z | `4ca9a5a8bd95ddcb` | 438 | `pipeline` | `wire` | [open](https://nominatim.openstreetmap.org/search?q=Seoul&format=json&limit=1) |
| `E001214` | `wikimedia_pageviews` | 200 | 2026-09-23T07:19:33Z | `99e147390f895ad2` | 1,138 | `pipeline` | `wire` | [open](https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/Artificial_intelligence/daily/20260915/20260921) |
| `E001215` | `github_repo` | 200 | 2026-09-23T07:19:33Z | `4f6d086cee934185` | 6,564 | `pipeline` | `wire` | [open](https://api.github.com/repos/browser-use/jev-ultrafast) |
| `E001216` | `github_releases` | 200 | 2026-09-23T07:19:33Z | `4f53cda18c2baa0c` | 2 | `pipeline` | `wire` | [open](https://api.github.com/repos/browser-use/jev-ultrafast/releases?per_page=1) |
| `E001217` | `github_repo` | 200 | 2026-09-23T07:19:33Z | `42767288f5cf457c` | 6,018 | `pipeline` | `wire` | [open](https://api.github.com/repos/zai-org/ZCode) |
| `E001218` | `github_releases` | 200 | 2026-09-23T07:19:33Z | `4f53cda18c2baa0c` | 2 | `pipeline` | `wire` | [open](https://api.github.com/repos/zai-org/ZCode/releases?per_page=1) |
| `E001219` | `github_repo` | 200 | 2026-09-23T07:19:33Z | `93b20032aea1ee16` | 5,500 | `pipeline` | `wire` | [open](https://api.github.com/repos/brayonpi/hexstellar) |
| `E001220` | `github_releases` | 200 | 2026-09-23T07:19:33Z | `2ab1e823c7832009` | 2,781 | `pipeline` | `wire` | [open](https://api.github.com/repos/brayonpi/hexstellar/releases?per_page=1) |
| `E001221` | `github_search` | 200 | 2026-09-23T07:19:33Z | `a82919d9c9255174` | 5,559 | `pipeline` | `wire` | [open](https://api.github.com/search/repositories?q=created:%3E=2026-09-16&sort=stars&order=desc&per_page=1) |
| `E001222` | `github_repos` | 200 | 2026-09-23T07:19:33Z | `6ef46cea7e73bff1` | 5,494 | `pipeline` | `wire` | [open](https://api.github.com/users/buffedlizard55-lab/repos?per_page=1) |
| `E001223` | `github_repo` | 200 | 2026-09-23T07:19:33Z | `ce146d9dde020fac` | 5,825 | `pipeline` | `wire` | [open](https://api.github.com/repos/buffedlizard55-lab/MasterSelfLearn) |
| `E001224` | `github_releases` | 200 | 2026-09-23T07:19:33Z | `4f53cda18c2baa0c` | 2 | `pipeline` | `wire` | [open](https://api.github.com/repos/buffedlizard55-lab/MasterSelfLearn/releases?per_page=1) |
| `E001225` | `master_site_catalog` | 200 | 2026-09-23T07:19:33Z | `312a6d754eea7a4a` | 553,056 | `pipeline` | `wire` | [open](https://api.github.com/repos/buffedlizard55-lab/MasterSite/contents/data/sites.js) |
| `E001226` | `pypi_json` | 200 | 2026-09-23T07:19:33Z | `bcfc6a202592e4e9` | 192,973 | `pipeline` | `wire` | [open](https://pypi.org/pypi/requests/json) |
| `E001227` | `npm_registry` | 200 | 2026-09-23T07:19:33Z | `80fde3eccb93e473` | 3,069 | `pipeline` | `wire` | [open](https://registry.npmjs.org/next/latest) |
| `E001228` | `wikimedia_pageviews` | 200 | 2026-09-23T07:19:33Z | `8e93bdbf2af1c096` | 1,138 | `pipeline` | `wire` | [open](https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/Artificial_intelligence/daily/20260914/20260920) |
| `E001229` | `federal_register` | 200 | 2026-09-23T07:19:33Z | `d2b1771420a54c0b` | 31,543 | `pipeline` | `wire` | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=1&order=newest) |
| `E001230` | `hn_firebase` | 200 | 2026-09-23T07:19:33Z | `aea31fc19a336ade` | 4,501 | `pipeline` | `wire` | [open](https://hacker-news.firebaseio.com/v0/topstories.json) |
| `E001231` | `arxiv` | 200 | 2026-09-23T07:19:33Z | `fbf717bddc32cf26` | 3,800 | `pipeline` | `wire` | [open](https://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results=1) |
| `E001232` | `pubmed` | 200 | 2026-09-23T07:19:33Z | `273483dbbc013756` | 509 | `pipeline` | `wire` | [open](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=artificial+intelligence&retmax=1&retmode=json) |
| `E001233` | `openalex` | 200 | 2026-09-23T07:19:33Z | `6f503f740a7f553b` | 15,259 | `pipeline` | `wire` | [open](https://api.openalex.org/works?sort=publication_date:desc&per-page=1) |
| `E001234` | `crossref` | 200 | 2026-09-23T07:19:33Z | `3131833a914a3aa9` | 1,341 | `pipeline` | `wire` | [open](https://api.crossref.org/works?rows=1&sort=created&order=desc) |
| `E001235` | `stackexchange` | 200 | 2026-09-23T07:19:33Z | `64b9e2ee3d2a643d` | 890 | `pipeline` | `wire` | [open](https://api.stackexchange.com/2.3/questions?order=desc&sort=votes&site=stackoverflow&pagesize=1) |
| `E001236` | `huggingface` | 200 | 2026-09-23T07:19:33Z | `3b10c6583f766676` | 542 | `pipeline` | `wire` | [open](https://huggingface.co/api/models?sort=trendingScore&limit=1) |
| `E001237` | `worldbank` | 200 | 2026-09-23T07:19:33Z | `0302192ef40cbef6` | 302 | `pipeline` | `wire` | [open](https://api.worldbank.org/v2/country/USA/indicator/NY.GDP.MKTP.CD?format=json&per_page=1) |
| `E001238` | `ecb_sdmx` | 200 | 2026-09-23T07:19:33Z | `e1c0d0764bd0d87e` | 3,064 | `pipeline` | `wire` | [open](https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A?lastNObservations=1&format=jsondata) |
| `E001239` | `frankfurter` | 200 | 2026-09-23T07:19:33Z | `834d24f8f98686b0` | 85 | `pipeline` | `wire` | [open](https://api.frankfurter.app/latest?from=USD&to=EUR,KRW) |
| `E001240` | `europepmc` | 200 | 2026-09-23T07:19:33Z | `6b064be11c97be34` | 1,100 | `pipeline` | `wire` | [open](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=artificial+intelligence&format=json&pageSize=1) |
| `E001241` | `kalshi_public` | 200 | 2026-09-23T07:19:33Z | `2f259e5d6151a588` | 22,070 | `pipeline` | `wire` | [open](https://api.elections.kalshi.com/trade-api/v2/markets?limit=1) |

`wire` means SHA-256 covers the exact complete bytes handed to the adapter;
`projection` means only a canonical parsed projection was retained. Projection
rows remain usable legacy evidence but are never relabelled as wire-verifiable.

## 4. Library accounting

| | |
|---|---|
| Topics tracked | 169 |
| Topics with ≥1 claim row naming them (row-provable) | 145 |
| Topics with only pre-schema-v2 credit (not row-provable) | 19 |
| Topics with neither | 5 |
| Candidate / active / retired / blocked | 12 / 157 / 0 / 0 |
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
