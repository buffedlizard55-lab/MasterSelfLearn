# VERIFICATION — line-by-line audit ledger

Generated `2026-09-22T19:23:59Z` at cycle 20. Read-only verifiers:
`python3 -m msl.cli verify-claims` and `python3 tools/probe_sources.py`.

## 1. Claim ledger composition

| Kind | Count | What it means |
|---|---|---|
| `captured` | 10,952 | A value lifted from a payload this project read |
| `documented` | 0 | A value from the operator's own published record |
| `negative` | 8 | Proof that something does **not** exist |
| `derived` | 5,572 | Arithmetic over claims above, formula recorded |
| **Total accepted** | **16,532** | |
| Rejected by the gate | 0 | Published, not swallowed |

## 2. Source registry

31 sources. `status` comes only from conclusive cycle/probe reads
recorded in the shared health ledger, never from a hand-written registry value.

| # | Id | Name | Operator | Status | Live reads | Last read (UTC) | HTTP | Links |
|---|---|---|---|---|---|---|---|---|
| 1 | `arxiv` | arXiv API | arXiv (Cornell University) | `verified-live-read` | 13 | 2026-09-22T17:31:33Z | 200 | [docs](https://info.arxiv.org/help/api/index.html) · [probe](https://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results=1) |
| 2 | `bls` | U.S. Bureau of Labor Statistics Public Data API v2 | U.S. Bureau of Labor Statistics | `verified-live-read` | 7 | 2026-09-22T17:31:33Z | 200 | [docs](https://www.bls.gov/developers/home.htm) · [probe](https://api.bls.gov/publicAPI/v2/timeseries/data/CUUR0000SA0) |
| 3 | `census_acs` | U.S. Census Bureau API (ACS 5-year) | U.S. Census Bureau | `verified-live-read` | 1 | 2026-09-22T17:31:33Z | 200 | [docs](https://www.census.gov/data/developers/data-sets.html) · [probe](https://api.census.gov/data/2022/acs/acs5?get=NAME,B01001_001E&for=state:06) |
| 4 | `clinicaltrials` | ClinicalTrials.gov API v2 | U.S. National Library of Medicine | `blocked` | 0 | 2026-09-22T17:31:33Z | 403 | [docs](https://clinicaltrials.gov/data-api/api) · [probe](https://clinicaltrials.gov/api/v2/studies?pageSize=1&countTotal=true&query.term=artificial%20intelligence) |
| 5 | `crossref` | Crossref REST API | Crossref | `verified-live-read` | 13 | 2026-09-22T17:31:33Z | 200 | [docs](https://www.crossref.org/documentation/retrieve-metadata/rest-api/) · [probe](https://api.crossref.org/works?rows=1&sort=created&order=desc) |
| 6 | `ecb_sdmx` | ECB Data Portal — SDMX REST (EXR daily) | European Central Bank | `verified-live-read` | 13 | 2026-09-22T17:31:33Z | 200 | [docs](https://data-explorer.ecb.europa.eu/) · [probe](https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A?lastNObservations=1&format=jsondata) |
| 7 | `europepmc` | Europe PMC REST | European Molecular Biology Laboratory | `verified-live-read` | 13 | 2026-09-22T17:31:33Z | 200 | [docs](https://europepmc.org/RestfulWebService) · [probe](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=artificial+intelligence&format=json&pageSize=1) |
| 8 | `federal_register` | Federal Register API v1 | U.S. National Archives / Office of the Federal Register | `verified-live-read` | 73 | 2026-09-22T17:31:33Z | 200 | [docs](https://www.federalregister.gov/developers/documentation/api/v1) · [probe](https://www.federalregister.gov/api/v1/documents.json?per_page=1&order=newest) |
| 9 | `frankfurter` | Frankfurter FX (ECB reference rates mirror) | Community service publishing ECB reference rates | `verified-live-read` | 13 | 2026-09-22T17:31:33Z | 200 | [docs](https://www.frankfurter.app/) · [probe](https://api.frankfurter.app/latest?from=USD&to=EUR,KRW) |
| 10 | `github_releases` | GitHub Releases API — newest release | GitHub, Inc. | `verified-live-read` | 8 | 2026-09-22T17:31:33Z | 200 | [docs](https://docs.github.com/en/rest/releases/releases#list-releases) · [probe](https://api.github.com/repos/buffedlizard55-lab/MasterSelfLearn/releases?per_page=1) |
| 11 | `github_repo` | GitHub Repos API — one repository | GitHub, Inc. | `verified-live-read` | 8 | 2026-09-22T17:31:33Z | 200 | [docs](https://docs.github.com/en/rest/repos/repos#get-a-repository) · [probe](https://api.github.com/repos/buffedlizard55-lab/MasterSelfLearn) |
| 12 | `github_repos` | GitHub Repos API — owner corpus | GitHub, Inc. | `verified-live-read` | 15 | 2026-09-22T17:31:33Z | 200 | [docs](https://docs.github.com/en/rest/repos/repos) · [probe](https://api.github.com/users/buffedlizard55-lab/repos?per_page=1) |
| 13 | `github_search` | GitHub Search API — repositories | GitHub, Inc. | `verified-live-read` | 74 | 2026-09-22T17:31:33Z | 200 | [docs](https://docs.github.com/en/rest/search/search) · [probe](https://api.github.com/search/repositories?q=created:%3E=2026-09-14&sort=stars&order=desc&per_page=1) |
| 14 | `hn_firebase` | Hacker News official Firebase API | Hacker News / Y Combinator | `verified-live-read` | 7 | 2026-09-22T17:31:33Z | 200 | [docs](https://github.com/HackerNews/API) · [probe](https://hacker-news.firebaseio.com/v0/topstories.json) |
| 15 | `huggingface` | Hugging Face Hub API | Hugging Face, Inc. | `verified-live-read` | 13 | 2026-09-22T17:31:33Z | 200 | [docs](https://huggingface.co/docs/hub/api) · [probe](https://huggingface.co/api/models?sort=trendingScore&limit=1) |
| 16 | `kalshi_public` | Kalshi public market data | KalshiEX LLC | `verified-live-read` | 13 | 2026-09-22T17:31:33Z | 200 | [docs](https://trading-api.readme.io/reference/getmarkets) · [probe](https://api.elections.kalshi.com/trade-api/v2/markets?limit=1) |
| 17 | `master_site_catalog` | MasterSite verified project catalog | buffedlizard55-lab, served by GitHub Contents API | `registered` | 0 | — | — | [docs](https://docs.github.com/en/rest/repos/contents#get-repository-content) · [probe](https://api.github.com/repos/buffedlizard55-lab/MasterSite/contents/data/sites.js) |
| 18 | `mlb_statsapi` | MLB StatsAPI — schedule | Major League Baseball Advanced Media | `verified-live-read` | 8 | 2026-09-22T17:31:33Z | 200 | [docs](https://statsapi.mlb.com/) · [probe](https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=2026-09-20) |
| 19 | `nba_cdn` | NBA CDN — today's scoreboard | National Basketball Association | `blocked` | 0 | 2026-09-22T17:31:33Z | 403 | [docs](https://cdn.nba.com/) · [probe](https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json) |
| 20 | `nhl_web` | NHL public web API — scoreboard | National Hockey League | `verified-live-read` | 7 | 2026-09-22T17:31:33Z | 200 | [docs](https://api-web.nhle.com/) · [probe](https://api-web.nhle.com/v1/scoreboard/now) |
| 21 | `nominatim` | OpenStreetMap Nominatim | OpenStreetMap Foundation | `verified-live-read` | 7 | 2026-09-22T17:31:33Z | 200 | [docs](https://nominatim.org/release-docs/latest/api/Search/) · [probe](https://nominatim.openstreetmap.org/search?q=Seoul&format=json&limit=1) |
| 22 | `npm_registry` | npm Registry — package metadata | GitHub, Inc. (npm) | `verified-live-read` | 9 | 2026-09-22T17:31:33Z | 200 | [docs](https://github.com/npm/registry) · [probe](https://registry.npmjs.org/next/latest) |
| 23 | `nws_alerts` | api.weather.gov — active alerts | U.S. National Weather Service (NOAA) | `verified-live-read` | 7 | 2026-09-22T17:31:33Z | 200 | [docs](https://www.weather.gov/documentation/services-web-api) · [probe](https://api.weather.gov/alerts/active?area=CA) |
| 24 | `openalex` | OpenAlex scholarly graph | OurResearch (open catalogue of scholarly works) | `verified-live-read` | 13 | 2026-09-22T17:31:33Z | 200 | [docs](https://docs.openalex.org/) · [probe](https://api.openalex.org/works?sort=publication_date:desc&per-page=1) |
| 25 | `pubmed` | NCBI PubMed E-utilities | U.S. National Library of Medicine | `verified-live-read` | 19 | 2026-09-22T17:31:33Z | 200 | [docs](https://www.ncbi.nlm.nih.gov/books/NBK25501/) · [probe](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=artificial+intelligence&retmax=1&retmode=json) |
| 26 | `pypi_json` | PyPI JSON API | Python Software Foundation | `verified-live-read` | 9 | 2026-09-22T17:31:33Z | 200 | [docs](https://docs.pypi.org/api/json/) · [probe](https://pypi.org/pypi/requests/json) |
| 27 | `sec_edgar` | SEC EDGAR — company submissions | U.S. Securities and Exchange Commission | `blocked` | 0 | 2026-09-22T17:31:33Z | 403 | [docs](https://www.sec.gov/edgar/sec-api-documentation) · [probe](https://data.sec.gov/submissions/CIK0000320193.json) |
| 28 | `stackexchange` | Stack Exchange API 2.3 | Stack Exchange, Inc. | `verified-live-read` | 13 | 2026-09-22T17:31:33Z | 200 | [docs](https://api.stackexchange.com/docs) · [probe](https://api.stackexchange.com/2.3/questions?order=desc&sort=votes&site=stackoverflow&pagesize=1) |
| 29 | `usgs_fdsn` | USGS Earthquake Hazards — FDSN event service | U.S. Geological Survey | `verified-live-read` | 9 | 2026-09-22T17:31:33Z | 200 | [docs](https://earthquake.usgs.gov/fdsnws/event/1/) · [probe](https://earthquake.usgs.gov/fdsnws/event/1/count?format=geojson&starttime=2026-09-14&minmagnitude=5.0) |
| 30 | `wikimedia_pageviews` | Wikimedia Pageviews REST API | Wikimedia Foundation | `verified-live-read` | 13 | 2026-09-22T17:31:33Z | 200 | [docs](https://wikimedia.org/api/rest_v1/) · [probe](https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/Artificial_intelligence/daily/20260914/20260920) |
| 31 | `worldbank` | World Bank Open Data API | The World Bank | `verified-live-read` | 13 | 2026-09-22T17:31:33Z | 200 | [docs](https://datahelpdesk.worldbank.org/knowledgebase/articles/889392) · [probe](https://api.worldbank.org/v2/country/USA/indicator/NY.GDP.MKTP.CD?format=json&per_page=1) |

## 3. Most recent evidence rows

Every row is one outbound read, with the hash of what came back.

| Id | Source | HTTP | Captured (UTC) | SHA-256 (16) | Bytes | Capture mode | Integrity | URL |
|---|---|---|---|---|---|---|---|---|
| `E000802` | `federal_register` | 200 | 2026-09-22T17:31:33Z | `f86462d8803caf8a` | 0 | `pipeline` | `projection` | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=surveillance) |
| `E000803` | `federal_register` | 200 | 2026-09-22T17:31:33Z | `b510a7e519653cde` | 0 | `pipeline` | `projection` | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=data%20exchange) |
| `E000804` | `pubmed` | 200 | 2026-09-22T17:31:33Z | `2817f2beb6de6333` | 0 | `pipeline` | `projection` | [open](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=cdc&retmax=1&retmode=json) |
| `E000805` | `kalshi_public` | 200 | 2026-09-22T17:31:33Z | `3a9700ab05e95101` | 0 | `pipeline` | `projection` | [open](https://api.elections.kalshi.com/trade-api/v2/markets?limit=5) |
| `E000806` | `mlb_statsapi` | 200 | 2026-09-22T17:31:33Z | `c8174762b99d1fb2` | 0 | `pipeline` | `projection` | [open](https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=2026-09-15) |
| `E000807` | `github_search` | 200 | 2026-09-22T17:31:33Z | `47cb0eac8c1e7c6b` | 0 | `pipeline` | `projection` | [open](https://api.github.com/search/repositories?q=kalshi%20created%3A%3E%3D2026-06-24&sort=stars&order=desc&per_page=20) |
| `E000808` | `github_search` | 200 | 2026-09-22T17:31:33Z | `a748df0135cecd2b` | 0 | `pipeline` | `projection` | [open](https://api.github.com/search/repositories?q=prediction%20market%20created%3A%3E%3D2026-06-24&sort=stars&order=desc&per_page=20) |
| `E000809` | `github_search` | 200 | 2026-09-22T17:31:33Z | `b388f411ff06cf14` | 0 | `pipeline` | `projection` | [open](https://api.github.com/search/repositories?q=kalshi%20prediction%20market%20created%3A%3E%3D2026-09-15&sort=stars&order=desc&per_page=25) |
| `E000810` | `github_repos` | 200 | 2026-09-22T17:31:33Z | `aea8bc99fca23076` | 0 | `pipeline` | `projection` | [open](https://api.github.com/users/buffedlizard55-lab/repos?per_page=100&sort=updated) |
| `E000811` | `wikimedia_pageviews` | 200 | 2026-09-22T17:31:33Z | `2cb3b522b0a3827a` | 0 | `pipeline` | `projection` | [open](https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/Artificial_intelligence/daily/20260909/20260915) |
| `E000812` | `github_repo` | 200 | 2026-09-22T17:31:33Z | `ae0a546031927075` | 0 | `pipeline` | `projection` | [open](https://api.github.com/repos/browser-use/jev-ultrafast) |
| `E000813` | `github_releases` | 200 | 2026-09-22T17:31:33Z | `4f53cda18c2baa0c` | 0 | `pipeline` | `projection` | [open](https://api.github.com/repos/browser-use/jev-ultrafast/releases?per_page=1) |
| `E000814` | `github_repo` | 200 | 2026-09-22T17:31:33Z | `a5a862c39d3ad05c` | 0 | `pipeline` | `projection` | [open](https://api.github.com/repos/zai-org/ZCode) |
| `E000815` | `github_releases` | 200 | 2026-09-22T17:31:33Z | `4f53cda18c2baa0c` | 0 | `pipeline` | `projection` | [open](https://api.github.com/repos/zai-org/ZCode/releases?per_page=1) |
| `E000816` | `github_repo` | 200 | 2026-09-22T17:31:33Z | `10b6e01f64b6c2bc` | 0 | `pipeline` | `projection` | [open](https://api.github.com/repos/brayonpi/hexstellar) |
| `E000817` | `github_releases` | 200 | 2026-09-22T17:31:33Z | `e37e72a0a81dbbf4` | 0 | `pipeline` | `projection` | [open](https://api.github.com/repos/brayonpi/hexstellar/releases?per_page=1) |
| `E000818` | `federal_register` | 200 | 2026-09-21T22:58:00Z | `cb359277f96f3637` | 0 | `offline-fixture` | `projection` | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=2&order=newest&conditions%5Bterm%5D=artificial+intelligence) |
| `E000819` | `github_search` | 200 | 2026-09-21T23:23:48Z | `cf78e54ce087f393` | 0 | `offline-fixture` | `projection` | [open](https://api.github.com/search/repositories?q=AI%20agents%20created%3A%3E%3D2026-08-22&sort=stars&order=desc&per_page=25) |
| `E000820` | `github_search` | 200 | 2026-09-21T23:23:49Z | `c5b6e617a9180500` | 0 | `offline-fixture` | `projection` | [open](https://api.github.com/search/repositories?q=LLM%20reasoning%20created%3A%3E%3D2026-08-22&sort=stars&order=desc&per_page=25) |
| `E000821` | `github_search` | 200 | 2026-09-21T23:23:47Z | `405a20e09a41624d` | 0 | `offline-fixture` | `projection` | [open](https://api.github.com/search/repositories?q=created%3A%3E%3D2026-09-14&sort=stars&order=desc&per_page=25) |
| `E000822` | `github_search` | 200 | 2026-09-21T23:23:50Z | `ec002e3054a260a6` | 0 | `offline-fixture` | `projection` | [open](https://api.github.com/search/repositories?q=prediction%20markets%20created%3A%3E%3D2026-06-23&sort=stars&order=desc&per_page=25) |
| `E000823` | `github_releases` | 200 | 2026-09-22T07:03:02Z | `4f53cda18c2baa0c` | 0 | `offline-fixture` | `projection` | [open](https://api.github.com/repos/browser-use/jev-ultrafast/releases?per_page=1) |
| `E000824` | `github_releases` | 200 | 2026-09-22T07:03:03Z | `c7cc0fec80bec0f5` | 0 | `offline-fixture` | `projection` | [open](https://api.github.com/repos/ollama/ollama/releases?per_page=1) |
| `E000825` | `github_repo` | 200 | 2026-09-22T07:03:02Z | `4182923f9d460ca4` | 0 | `offline-fixture` | `projection` | [open](https://api.github.com/repos/browser-use/jev-ultrafast) |
| `E000826` | `github_search` | 200 | 2026-09-21T23:23:51Z | `ed417b263f53ee07` | 0 | `offline-fixture` | `projection` | [open](https://api.github.com/search/repositories?q=sports%20analytics%20created%3A%3E%3D2026-06-23&sort=stars&order=desc&per_page=25) |
| `E000827` | `hn_firebase` | 200 | 2026-09-21T22:48:00Z | `b7c96de2d1d7bcc3` | 0 | `offline-fixture` | `projection` | [open](https://hacker-news.firebaseio.com/v0/topstories.json) |
| `E000828` | `master_site_catalog` | 200 | 2026-09-22T18:09:33Z | `9982e54c46bec945` | 0 | `offline-fixture` | `projection` | [open](https://api.github.com/repos/buffedlizard55-lab/MasterSite/contents/data/sites.js) |
| `E000829` | `npm_registry` | 200 | 2026-09-21T23:18:26Z | `8738636d87e465a7` | 0 | `offline-fixture` | `projection` | [open](https://registry.npmjs.org/next/latest) |
| `E000830` | `npm_registry` | 200 | 2026-09-21T23:18:27Z | `07ba1af01a3d2247` | 0 | `offline-fixture` | `projection` | [open](https://registry.npmjs.org/react/latest) |
| `E000831` | `npm_registry` | 200 | 2026-09-21T23:18:27Z | `5822ee8e5f2d4ba7` | 0 | `offline-fixture` | `projection` | [open](https://registry.npmjs.org/typescript/latest) |
| `E000832` | `npm_registry` | 200 | 2026-09-21T23:18:27Z | `67311bc5afa0719a` | 0 | `offline-fixture` | `projection` | [open](https://registry.npmjs.org/vite/latest) |
| `E000833` | `github_repos` | 200 | 2026-09-21T23:18:26Z | `87f19cebf5ea8c2d` | 0 | `offline-fixture` | `projection` | [open](https://api.github.com/users/buffedlizard55-lab/repos?per_page=100&sort=updated) |
| `E000834` | `pypi_json` | 200 | 2026-09-21T23:19:23Z | `bdac160cc4c04547` | 0 | `offline-fixture` | `projection` | [open](https://pypi.org/pypi/numpy/json) |
| `E000835` | `pypi_json` | 200 | 2026-09-21T23:19:23Z | `e1f7dec9d4364237` | 0 | `offline-fixture` | `projection` | [open](https://pypi.org/pypi/pandas/json) |
| `E000836` | `pypi_json` | 200 | 2026-09-21T23:18:26Z | `14d9c92317db9922` | 0 | `offline-fixture` | `projection` | [open](https://pypi.org/pypi/requests/json) |
| `E000837` | `pypi_json` | 200 | 2026-09-21T23:19:23Z | `82d60b17ede99d4f` | 0 | `offline-fixture` | `projection` | [open](https://pypi.org/pypi/scikit-learn/json) |
| `E000838` | `usgs_fdsn` | 200 | 2026-09-21T22:56:00Z | `34a313d9faf37155` | 0 | `offline-fixture` | `projection` | [open](https://earthquake.usgs.gov/fdsnws/event/1/count?format=geojson&starttime=2026-09-14&minmagnitude=5.0) |
| `E000839` | `wikimedia_pageviews` | 200 | 2026-09-21T22:58:00Z | `0a5b8138baa6a361` | 0 | `offline-fixture` | `projection` | [open](https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/Artificial_intelligence/daily/20260914/20260920) |
| `E000840` | `federal_register` | 200 | 2026-09-21T22:58:00Z | `cb359277f96f3637` | 0 | `offline-fixture` | `projection` | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=2&order=newest&conditions%5Bterm%5D=artificial+intelligence) |
| `E000841` | `github_search` | 200 | 2026-09-21T23:23:48Z | `cf78e54ce087f393` | 0 | `offline-fixture` | `projection` | [open](https://api.github.com/search/repositories?q=AI%20agents%20created%3A%3E%3D2026-08-22&sort=stars&order=desc&per_page=25) |
| `E000842` | `github_search` | 200 | 2026-09-21T23:23:49Z | `c5b6e617a9180500` | 0 | `offline-fixture` | `projection` | [open](https://api.github.com/search/repositories?q=LLM%20reasoning%20created%3A%3E%3D2026-08-22&sort=stars&order=desc&per_page=25) |
| `E000843` | `github_search` | 200 | 2026-09-21T23:23:47Z | `405a20e09a41624d` | 0 | `offline-fixture` | `projection` | [open](https://api.github.com/search/repositories?q=created%3A%3E%3D2026-09-14&sort=stars&order=desc&per_page=25) |
| `E000844` | `github_search` | 200 | 2026-09-21T23:23:50Z | `ec002e3054a260a6` | 0 | `offline-fixture` | `projection` | [open](https://api.github.com/search/repositories?q=prediction%20markets%20created%3A%3E%3D2026-06-23&sort=stars&order=desc&per_page=25) |
| `E000845` | `github_releases` | 200 | 2026-09-22T07:03:02Z | `4f53cda18c2baa0c` | 0 | `offline-fixture` | `projection` | [open](https://api.github.com/repos/browser-use/jev-ultrafast/releases?per_page=1) |
| `E000846` | `github_releases` | 200 | 2026-09-22T07:03:03Z | `c7cc0fec80bec0f5` | 0 | `offline-fixture` | `projection` | [open](https://api.github.com/repos/ollama/ollama/releases?per_page=1) |
| `E000847` | `github_repo` | 200 | 2026-09-22T07:03:02Z | `4182923f9d460ca4` | 0 | `offline-fixture` | `projection` | [open](https://api.github.com/repos/browser-use/jev-ultrafast) |
| `E000848` | `github_search` | 200 | 2026-09-21T23:23:51Z | `ed417b263f53ee07` | 0 | `offline-fixture` | `projection` | [open](https://api.github.com/search/repositories?q=sports%20analytics%20created%3A%3E%3D2026-06-23&sort=stars&order=desc&per_page=25) |
| `E000849` | `hn_firebase` | 200 | 2026-09-21T22:48:00Z | `b7c96de2d1d7bcc3` | 0 | `offline-fixture` | `projection` | [open](https://hacker-news.firebaseio.com/v0/topstories.json) |
| `E000850` | `master_site_catalog` | 200 | 2026-09-22T18:09:33Z | `9982e54c46bec945` | 0 | `offline-fixture` | `projection` | [open](https://api.github.com/repos/buffedlizard55-lab/MasterSite/contents/data/sites.js) |
| `E000851` | `npm_registry` | 200 | 2026-09-21T23:18:26Z | `8738636d87e465a7` | 0 | `offline-fixture` | `projection` | [open](https://registry.npmjs.org/next/latest) |
| `E000852` | `npm_registry` | 200 | 2026-09-21T23:18:27Z | `07ba1af01a3d2247` | 0 | `offline-fixture` | `projection` | [open](https://registry.npmjs.org/react/latest) |
| `E000853` | `npm_registry` | 200 | 2026-09-21T23:18:27Z | `5822ee8e5f2d4ba7` | 0 | `offline-fixture` | `projection` | [open](https://registry.npmjs.org/typescript/latest) |
| `E000854` | `npm_registry` | 200 | 2026-09-21T23:18:27Z | `67311bc5afa0719a` | 0 | `offline-fixture` | `projection` | [open](https://registry.npmjs.org/vite/latest) |
| `E000855` | `github_repos` | 200 | 2026-09-21T23:18:26Z | `87f19cebf5ea8c2d` | 0 | `offline-fixture` | `projection` | [open](https://api.github.com/users/buffedlizard55-lab/repos?per_page=100&sort=updated) |
| `E000856` | `pypi_json` | 200 | 2026-09-21T23:19:23Z | `bdac160cc4c04547` | 0 | `offline-fixture` | `projection` | [open](https://pypi.org/pypi/numpy/json) |
| `E000857` | `pypi_json` | 200 | 2026-09-21T23:19:23Z | `e1f7dec9d4364237` | 0 | `offline-fixture` | `projection` | [open](https://pypi.org/pypi/pandas/json) |
| `E000858` | `pypi_json` | 200 | 2026-09-21T23:18:26Z | `14d9c92317db9922` | 0 | `offline-fixture` | `projection` | [open](https://pypi.org/pypi/requests/json) |
| `E000859` | `pypi_json` | 200 | 2026-09-21T23:19:23Z | `82d60b17ede99d4f` | 0 | `offline-fixture` | `projection` | [open](https://pypi.org/pypi/scikit-learn/json) |
| `E000860` | `usgs_fdsn` | 200 | 2026-09-21T22:56:00Z | `34a313d9faf37155` | 0 | `offline-fixture` | `projection` | [open](https://earthquake.usgs.gov/fdsnws/event/1/count?format=geojson&starttime=2026-09-14&minmagnitude=5.0) |
| `E000861` | `wikimedia_pageviews` | 200 | 2026-09-21T22:58:00Z | `0a5b8138baa6a361` | 0 | `offline-fixture` | `projection` | [open](https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/Artificial_intelligence/daily/20260914/20260920) |

`wire` means SHA-256 covers the exact complete bytes handed to the adapter;
`projection` means only a canonical parsed projection was retained. Projection
rows remain usable legacy evidence but are never relabelled as wire-verifiable.

## 4. Library accounting

| | |
|---|---|
| Topics tracked | 133 |
| Topics with ≥1 accepted claim credit | 116 |
| Topics with 0 accepted claim credits | 17 |
| Candidate / active / retired / blocked | 9 / 123 / 0 / 1 |
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
