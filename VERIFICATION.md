# VERIFICATION — line-by-line audit ledger

Generated `2026-09-27T00:13:12Z` at cycle 29. Read-only verifiers:
`python3 -m msl.cli verify-claims` and `python3 tools/probe_sources.py`.

## 1. Claim ledger composition

| Kind | Count | What it means |
|---|---|---|
| `captured` | 17,297 | A value lifted from a payload this project read |
| `documented` | 0 | A value from the operator's own published record |
| `negative` | 32 | Proof that something does **not** exist |
| `derived` | 9,180 | Arithmetic over claims above, formula recorded |
| **Total accepted** | **26,509** | |
| Rejected by the gate | 0 | Published, not swallowed |

## 2. Source registry

31 sources. `status` comes only from conclusive cycle/probe reads
recorded in the shared health ledger, never from a hand-written registry value.

| # | Id | Name | Operator | Status | Live reads | Last read (UTC) | HTTP | Links |
|---|---|---|---|---|---|---|---|---|
| 1 | `arxiv` | arXiv API | arXiv (Cornell University) | `verified-live-read` | 33 | 2026-09-27T00:13:12Z | 200 | [docs](https://info.arxiv.org/help/api/index.html) · [probe](https://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results=1) |
| 2 | `bls` | U.S. Bureau of Labor Statistics Public Data API v2 | U.S. Bureau of Labor Statistics | `verified-live-read` | 12 | 2026-09-27T00:13:12Z | 200 | [docs](https://www.bls.gov/developers/home.htm) · [probe](https://api.bls.gov/publicAPI/v2/timeseries/data/CUUR0000SA0) |
| 3 | `census_acs` | U.S. Census Bureau API (ACS 5-year) | U.S. Census Bureau | `verified-live-read` | 13 | 2026-09-27T00:13:12Z | 200 | [docs](https://www.census.gov/data/developers/data-sets.html) · [probe](https://api.census.gov/data/2022/acs/acs5?get=NAME,B01001_001E&for=state:06) |
| 4 | `clinicaltrials` | ClinicalTrials.gov API v2 | U.S. National Library of Medicine | `blocked` | 0 | 2026-09-27T00:13:12Z | 403 | [docs](https://clinicaltrials.gov/data-api/api) · [probe](https://clinicaltrials.gov/api/v2/studies?pageSize=1&countTotal=true&query.term=artificial%20intelligence) |
| 5 | `crossref` | Crossref REST API | Crossref | `verified-live-read` | 33 | 2026-09-27T00:13:12Z | 200 | [docs](https://www.crossref.org/documentation/retrieve-metadata/rest-api/) · [probe](https://api.crossref.org/works?rows=1&sort=created&order=desc) |
| 6 | `ecb_sdmx` | ECB Data Portal — SDMX REST (EXR daily) | European Central Bank | `verified-live-read` | 33 | 2026-09-27T00:13:12Z | 200 | [docs](https://data-explorer.ecb.europa.eu/) · [probe](https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A?lastNObservations=1&format=jsondata) |
| 7 | `europepmc` | Europe PMC REST | European Molecular Biology Laboratory | `verified-live-read` | 33 | 2026-09-27T00:13:12Z | 200 | [docs](https://europepmc.org/RestfulWebService) · [probe](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=artificial+intelligence&format=json&pageSize=1) |
| 8 | `federal_register` | Federal Register API v1 | U.S. National Archives / Office of the Federal Register | `verified-live-read` | 173 | 2026-09-27T00:13:12Z | 200 | [docs](https://www.federalregister.gov/developers/documentation/api/v1) · [probe](https://www.federalregister.gov/api/v1/documents.json?per_page=1&order=newest) |
| 9 | `frankfurter` | Frankfurter FX (ECB reference rates mirror) | Community service publishing ECB reference rates | `verified-live-read` | 33 | 2026-09-27T00:13:12Z | 200 | [docs](https://www.frankfurter.app/) · [probe](https://api.frankfurter.app/latest?from=USD&to=EUR,KRW) |
| 10 | `github_releases` | GitHub Releases API — newest release | GitHub, Inc. | `verified-live-read` | 44 | 2026-09-27T00:13:12Z | 200 | [docs](https://docs.github.com/en/rest/releases/releases#list-releases) · [probe](https://api.github.com/repos/buffedlizard55-lab/MasterSelfLearn/releases?per_page=1) |
| 11 | `github_repo` | GitHub Repos API — one repository | GitHub, Inc. | `verified-live-read` | 44 | 2026-09-27T00:13:12Z | 200 | [docs](https://docs.github.com/en/rest/repos/repos#get-a-repository) · [probe](https://api.github.com/repos/buffedlizard55-lab/MasterSelfLearn) |
| 12 | `github_repos` | GitHub Repos API — owner corpus | GitHub, Inc. | `verified-live-read` | 35 | 2026-09-27T00:13:12Z | 200 | [docs](https://docs.github.com/en/rest/repos/repos) · [probe](https://api.github.com/users/buffedlizard55-lab/repos?per_page=1) |
| 13 | `github_search` | GitHub Search API — repositories | GitHub, Inc. | `verified-live-read` | 134 | 2026-09-27T00:13:12Z | 200 | [docs](https://docs.github.com/en/rest/search/search) · [probe](https://api.github.com/search/repositories?q=created:%3E=2026-09-20&sort=stars&order=desc&per_page=1) |
| 14 | `hn_firebase` | Hacker News official Firebase API | Hacker News / Y Combinator | `verified-live-read` | 19 | 2026-09-27T00:13:12Z | 200 | [docs](https://github.com/HackerNews/API) · [probe](https://hacker-news.firebaseio.com/v0/topstories.json) |
| 15 | `huggingface` | Hugging Face Hub API | Hugging Face, Inc. | `verified-live-read` | 33 | 2026-09-27T00:13:12Z | 200 | [docs](https://huggingface.co/docs/hub/api) · [probe](https://huggingface.co/api/models?sort=trendingScore&limit=1) |
| 16 | `kalshi_public` | Kalshi public market data | KalshiEX LLC | `verified-live-read` | 33 | 2026-09-27T00:13:12Z | 200 | [docs](https://trading-api.readme.io/reference/getmarkets) · [probe](https://api.elections.kalshi.com/trade-api/v2/markets?limit=1) |
| 17 | `master_site_catalog` | MasterSite verified project catalog | buffedlizard55-lab, served by GitHub Contents API | `verified-live-read` | 12 | 2026-09-27T00:13:12Z | 200 | [docs](https://docs.github.com/en/rest/repos/contents#get-repository-content) · [probe](https://api.github.com/repos/buffedlizard55-lab/MasterSite/contents/data/sites.js) |
| 18 | `mlb_statsapi` | MLB StatsAPI — schedule | Major League Baseball Advanced Media | `verified-live-read` | 23 | 2026-09-27T00:13:12Z | 200 | [docs](https://statsapi.mlb.com/) · [probe](https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=2026-09-26) |
| 19 | `nba_cdn` | NBA CDN — today's scoreboard | National Basketball Association | `blocked` | 0 | 2026-09-27T00:13:12Z | 403 | [docs](https://cdn.nba.com/) · [probe](https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json) |
| 20 | `nhl_web` | NHL public web API — scoreboard | National Hockey League | `verified-live-read` | 19 | 2026-09-27T00:13:12Z | 200 | [docs](https://api-web.nhle.com/) · [probe](https://api-web.nhle.com/v1/scoreboard/now) |
| 21 | `nominatim` | OpenStreetMap Nominatim | OpenStreetMap Foundation | `verified-live-read` | 19 | 2026-09-27T00:13:12Z | 200 | [docs](https://nominatim.org/release-docs/latest/api/Search/) · [probe](https://nominatim.openstreetmap.org/search?q=Seoul&format=json&limit=1) |
| 22 | `npm_registry` | npm Registry — package metadata | GitHub, Inc. (npm) | `verified-live-read` | 21 | 2026-09-27T00:13:12Z | 200 | [docs](https://github.com/npm/registry) · [probe](https://registry.npmjs.org/next/latest) |
| 23 | `nws_alerts` | api.weather.gov — active alerts | U.S. National Weather Service (NOAA) | `verified-live-read` | 19 | 2026-09-27T00:13:12Z | 200 | [docs](https://www.weather.gov/documentation/services-web-api) · [probe](https://api.weather.gov/alerts/active?area=CA) |
| 24 | `openalex` | OpenAlex scholarly graph | OurResearch (open catalogue of scholarly works) | `verified-live-read` | 33 | 2026-09-27T00:13:12Z | 200 | [docs](https://docs.openalex.org/) · [probe](https://api.openalex.org/works?sort=publication_date:desc&per-page=1) |
| 25 | `pubmed` | NCBI PubMed E-utilities | U.S. National Library of Medicine | `verified-live-read` | 47 | 2026-09-27T00:13:12Z | 200 | [docs](https://www.ncbi.nlm.nih.gov/books/NBK25501/) · [probe](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=artificial+intelligence&retmax=1&retmode=json) |
| 26 | `pypi_json` | PyPI JSON API | Python Software Foundation | `verified-live-read` | 21 | 2026-09-27T00:13:12Z | 200 | [docs](https://docs.pypi.org/api/json/) · [probe](https://pypi.org/pypi/requests/json) |
| 27 | `sec_edgar` | SEC EDGAR — company submissions | U.S. Securities and Exchange Commission | `blocked` | 0 | 2026-09-27T00:13:12Z | 403 | [docs](https://www.sec.gov/edgar/sec-api-documentation) · [probe](https://data.sec.gov/submissions/CIK0000320193.json) |
| 28 | `stackexchange` | Stack Exchange API 2.3 | Stack Exchange, Inc. | `verified-live-read` | 33 | 2026-09-27T00:13:12Z | 200 | [docs](https://api.stackexchange.com/docs) · [probe](https://api.stackexchange.com/2.3/questions?order=desc&sort=votes&site=stackoverflow&pagesize=1) |
| 29 | `usgs_fdsn` | USGS Earthquake Hazards — FDSN event service | U.S. Geological Survey | `verified-live-read` | 24 | 2026-09-27T00:13:12Z | 200 | [docs](https://earthquake.usgs.gov/fdsnws/event/1/) · [probe](https://earthquake.usgs.gov/fdsnws/event/1/count?format=geojson&starttime=2026-09-20&endtime=2026-09-27&minmagnitude=5.0) |
| 30 | `wikimedia_pageviews` | Wikimedia Pageviews REST API | Wikimedia Foundation | `verified-live-read` | 29 | 2026-09-27T00:13:12Z | 200 | [docs](https://wikimedia.org/api/rest_v1/) · [probe](https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/Artificial_intelligence/daily/20260914/20260920) |
| 31 | `worldbank` | World Bank Open Data API | The World Bank | `verified-live-read` | 33 | 2026-09-27T00:13:12Z | 200 | [docs](https://datahelpdesk.worldbank.org/knowledgebase/articles/889392) · [probe](https://api.worldbank.org/v2/country/USA/indicator/NY.GDP.MKTP.CD?format=json&per_page=1) |

## 3. Most recent evidence rows

Every row is one outbound read, with the hash of what came back.

| Id | Source | HTTP | Captured (UTC) | SHA-256 (16) | Bytes | Capture mode | Integrity | URL |
|---|---|---|---|---|---|---|---|---|
| `E001331` | `arxiv` | 200 | 2026-09-27T00:13:12Z | `b2751ca9f2082f2a` | 21,208 | `pipeline` | `wire` | [open](https://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results=8) |
| `E001332` | `openalex` | 200 | 2026-09-27T00:13:12Z | `d40f0d25c5720c13` | 76,401 | `pipeline` | `wire` | [open](https://api.openalex.org/works?sort=publication_date:desc&per-page=5&mailto=buffedlizard55@gmail.com) |
| `E001333` | `crossref` | 200 | 2026-09-27T00:13:12Z | `2a189b86478f2f7e` | 19,357 | `pipeline` | `wire` | [open](https://api.crossref.org/works?rows=3&sort=created&order=desc&mailto=buffedlizard55@gmail.com) |
| `E001334` | `europepmc` | 200 | 2026-09-27T00:13:12Z | `18947e95078e9b3a` | 2,637 | `pipeline` | `wire` | [open](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=artificial+intelligence&format=json&pageSize=3) |
| `E001335` | `huggingface` | 200 | 2026-09-27T00:13:12Z | `a95b2adbeebfe2ef` | 5,020 | `pipeline` | `wire` | [open](https://huggingface.co/api/models?sort=trendingScore&limit=10) |
| `E001336` | `github_search` | 200 | 2026-09-27T00:13:12Z | `9b50fd1ea50bc5e2` | 108,812 | `pipeline` | `wire` | [open](https://api.github.com/search/repositories?q=agent%20created%3A%3E%3D2026-06-29&sort=stars&order=desc&per_page=20) |
| `E001337` | `github_search` | 200 | 2026-09-27T00:13:12Z | `d870f2625a6e362b` | 110,792 | `pipeline` | `wire` | [open](https://api.github.com/search/repositories?q=framework%20created%3A%3E%3D2026-06-29&sort=stars&order=desc&per_page=20) |
| `E001338` | `github_search` | 200 | 2026-09-27T00:13:12Z | `11a83f13f926f59f` | 147,843 | `pipeline` | `wire` | [open](https://api.github.com/search/repositories?q=agent%20framework%20created%3A%3E%3D2026-09-20&sort=stars&order=desc&per_page=25) |
| `E001339` | `stackexchange` | 200 | 2026-09-27T00:13:12Z | `36da4488f2c19d81` | 3,795 | `pipeline` | `wire` | [open](https://api.stackexchange.com/2.3/questions?order=desc&sort=votes&site=stackoverflow&pagesize=5&tagged=python) |
| `E001340` | `federal_register` | 200 | 2026-09-27T00:13:12Z | `8c03f139b1716aa8` | 10,753 | `pipeline` | `wire` | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=artificial%20intelligence) |
| `E001341` | `federal_register` | 200 | 2026-09-27T00:13:12Z | `65df9d2dd54a12b3` | 10,498 | `pipeline` | `wire` | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=health) |
| `E001342` | `federal_register` | 200 | 2026-09-27T00:13:12Z | `928c2fa0b85c0f0c` | 12,544 | `pipeline` | `wire` | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=energy) |
| `E001343` | `federal_register` | 200 | 2026-09-27T00:13:12Z | `48269e873f74b62a` | 12,295 | `pipeline` | `wire` | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=security) |
| `E001344` | `worldbank` | 200 | 2026-09-27T00:13:12Z | `f681cb8323b72c96` | 724 | `pipeline` | `wire` | [open](https://api.worldbank.org/v2/country/USA/indicator/NY.GDP.MKTP.CD?format=json&per_page=3) |
| `E001345` | `ecb_sdmx` | 200 | 2026-09-27T00:13:12Z | `d5f9f8b947c5a239` | 3,354 | `pipeline` | `wire` | [open](https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A?lastNObservations=3&format=jsondata) |
| `E001346` | `frankfurter` | 200 | 2026-09-27T00:13:12Z | `a46364e3160233ed` | 98 | `pipeline` | `wire` | [open](https://api.frankfurter.app/latest?from=USD&to=EUR,KRW,JPY) |
| `E001347` | `bls` | 200 | 2026-09-27T00:13:12Z | `43a042423a390fd7` | 3,024 | `pipeline` | `wire` | [open](https://api.bls.gov/publicAPI/v2/timeseries/data/CUUR0000SA0) |
| `E001348` | `usgs_fdsn` | 200 | 2026-09-27T00:13:12Z | `252beeb5645efd69` | 31 | `pipeline` | `wire` | [open](https://earthquake.usgs.gov/fdsnws/event/1/count?format=geojson&starttime=2026-09-20&endtime=2026-09-27&minmagnitude=5.0) |
| `E001349` | `nws_alerts` | 200 | 2026-09-27T00:13:12Z | `a1228c668189f0ea` | 40,946 | `pipeline` | `wire` | [open](https://api.weather.gov/alerts/active?area=CA) |
| `E001350` | `pubmed` | 200 | 2026-09-27T00:13:12Z | `ebd83ed924988f6e` | 798 | `pipeline` | `wire` | [open](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=trial&retmax=1&retmode=json) |
| `E001351` | `federal_register` | 200 | 2026-09-27T00:13:12Z | `69f2dcd042e7dbfc` | 10,653 | `pipeline` | `wire` | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=public%20health) |
| `E001352` | `federal_register` | 200 | 2026-09-27T00:13:12Z | `c02af7b1ed48fe97` | 11,846 | `pipeline` | `wire` | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=surveillance) |
| `E001353` | `federal_register` | 200 | 2026-09-27T00:13:12Z | `90cec07988c09e9d` | 8,546 | `pipeline` | `wire` | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=data%20exchange) |
| `E001354` | `pubmed` | 200 | 2026-09-27T00:13:12Z | `1ff80705b7410dd1` | 783 | `pipeline` | `wire` | [open](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=cdc&retmax=1&retmode=json) |
| `E001355` | `kalshi_public` | 200 | 2026-09-27T00:13:12Z | `40d48a550089081c` | 13,111 | `pipeline` | `wire` | [open](https://api.elections.kalshi.com/trade-api/v2/markets?limit=5) |
| `E001356` | `mlb_statsapi` | 200 | 2026-09-27T00:13:12Z | `fd73369a96ecbb9e` | 16,931 | `pipeline` | `wire` | [open](https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=2026-09-26) |
| `E001357` | `nhl_web` | 200 | 2026-09-27T00:13:12Z | `ff76609116c22896` | 118,019 | `pipeline` | `wire` | [open](https://api-web.nhle.com/v1/scoreboard/now) |
| `E001358` | `github_search` | 200 | 2026-09-27T00:13:12Z | `1f1633170bdaa0c5` | 118,628 | `pipeline` | `wire` | [open](https://api.github.com/search/repositories?q=kalshi%20created%3A%3E%3D2026-06-29&sort=stars&order=desc&per_page=20) |
| `E001359` | `github_search` | 200 | 2026-09-27T00:13:12Z | `e8000648a7adceb7` | 117,367 | `pipeline` | `wire` | [open](https://api.github.com/search/repositories?q=prediction%20market%20created%3A%3E%3D2026-06-29&sort=stars&order=desc&per_page=20) |
| `E001360` | `github_search` | 200 | 2026-09-27T00:13:12Z | `d293a42e9a8f6041` | 133,551 | `pipeline` | `wire` | [open](https://api.github.com/search/repositories?q=kalshi%20prediction%20market%20created%3A%3E%3D2026-09-20&sort=stars&order=desc&per_page=25) |
| `E001361` | `github_repos` | 200 | 2026-09-27T00:13:12Z | `f2c07fba0d6a29a7` | 496,953 | `pipeline` | `wire` | [open](https://api.github.com/users/buffedlizard55-lab/repos?per_page=100&sort=updated) |
| `E001362` | `nominatim` | 200 | 2026-09-27T00:13:12Z | `2e693e681927c926` | 438 | `pipeline` | `wire` | [open](https://nominatim.openstreetmap.org/search?q=Seoul&format=json&limit=1) |
| `E001363` | `wikimedia_pageviews` | 200 | 2026-09-27T00:13:12Z | `68944eac93d3bb79` | 1,138 | `pipeline` | `wire` | [open](https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/Artificial_intelligence/daily/20260919/20260925) |
| `E001364` | `github_repo` | 200 | 2026-09-27T00:13:12Z | `534a2535ed8ffbcf` | 6,564 | `pipeline` | `wire` | [open](https://api.github.com/repos/browser-use/jev-ultrafast) |
| `E001365` | `github_releases` | 200 | 2026-09-27T00:13:12Z | `4f53cda18c2baa0c` | 2 | `pipeline` | `wire` | [open](https://api.github.com/repos/browser-use/jev-ultrafast/releases?per_page=1) |
| `E001366` | `github_repo` | 200 | 2026-09-27T00:13:12Z | `343010c140a552b7` | 6,018 | `pipeline` | `wire` | [open](https://api.github.com/repos/zai-org/ZCode) |
| `E001367` | `github_releases` | 200 | 2026-09-27T00:13:12Z | `13fdbde35d762e8e` | 5,423 | `pipeline` | `wire` | [open](https://api.github.com/repos/zai-org/ZCode/releases?per_page=1) |
| `E001368` | `github_repo` | 200 | 2026-09-27T00:13:12Z | `b87eb1fcead04637` | 5,500 | `pipeline` | `wire` | [open](https://api.github.com/repos/brayonpi/hexstellar) |
| `E001369` | `github_releases` | 200 | 2026-09-27T00:13:12Z | `2ab1e823c7832009` | 2,781 | `pipeline` | `wire` | [open](https://api.github.com/repos/brayonpi/hexstellar/releases?per_page=1) |
| `E001370` | `github_search` | 200 | 2026-09-27T00:13:12Z | `8cac6db345c74f62` | 5,061 | `pipeline` | `wire` | [open](https://api.github.com/search/repositories?q=created:%3E=2026-09-20&sort=stars&order=desc&per_page=1) |
| `E001371` | `github_repos` | 200 | 2026-09-27T00:13:12Z | `253b30b32d1ff35e` | 5,491 | `pipeline` | `wire` | [open](https://api.github.com/users/buffedlizard55-lab/repos?per_page=1) |
| `E001372` | `github_repo` | 200 | 2026-09-27T00:13:12Z | `c8caf6853fcc8432` | 5,825 | `pipeline` | `wire` | [open](https://api.github.com/repos/buffedlizard55-lab/MasterSelfLearn) |
| `E001373` | `github_releases` | 200 | 2026-09-27T00:13:12Z | `4f53cda18c2baa0c` | 2 | `pipeline` | `wire` | [open](https://api.github.com/repos/buffedlizard55-lab/MasterSelfLearn/releases?per_page=1) |
| `E001374` | `master_site_catalog` | 200 | 2026-09-27T00:13:12Z | `f49b45fef8daa854` | 727,536 | `pipeline` | `wire` | [open](https://api.github.com/repos/buffedlizard55-lab/MasterSite/contents/data/sites.js) |
| `E001375` | `pypi_json` | 200 | 2026-09-27T00:13:12Z | `bcfc6a202592e4e9` | 192,973 | `pipeline` | `wire` | [open](https://pypi.org/pypi/requests/json) |
| `E001376` | `npm_registry` | 200 | 2026-09-27T00:13:12Z | `80fde3eccb93e473` | 3,069 | `pipeline` | `wire` | [open](https://registry.npmjs.org/next/latest) |
| `E001377` | `wikimedia_pageviews` | 200 | 2026-09-27T00:13:12Z | `8e93bdbf2af1c096` | 1,138 | `pipeline` | `wire` | [open](https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/Artificial_intelligence/daily/20260914/20260920) |
| `E001378` | `federal_register` | 200 | 2026-09-27T00:13:12Z | `b6e8d8147f6d148b` | 36,511 | `pipeline` | `wire` | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=1&order=newest) |
| `E001379` | `hn_firebase` | 200 | 2026-09-27T00:13:12Z | `79394ad50231a228` | 4,501 | `pipeline` | `wire` | [open](https://hacker-news.firebaseio.com/v0/topstories.json) |
| `E001380` | `arxiv` | 200 | 2026-09-27T00:13:12Z | `adf8bcf1b41ebff3` | 2,747 | `pipeline` | `wire` | [open](https://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results=1) |
| `E001381` | `pubmed` | 200 | 2026-09-27T00:13:12Z | `2e2bf4d7e56be699` | 509 | `pipeline` | `wire` | [open](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=artificial+intelligence&retmax=1&retmode=json) |
| `E001382` | `openalex` | 200 | 2026-09-27T00:13:12Z | `2a3ce951f8704771` | 15,259 | `pipeline` | `wire` | [open](https://api.openalex.org/works?sort=publication_date:desc&per-page=1) |
| `E001383` | `crossref` | 200 | 2026-09-27T00:13:12Z | `be4ae007558ab7d8` | 4,204 | `pipeline` | `wire` | [open](https://api.crossref.org/works?rows=1&sort=created&order=desc) |
| `E001384` | `stackexchange` | 200 | 2026-09-27T00:13:12Z | `5b941f9ef8a152ca` | 890 | `pipeline` | `wire` | [open](https://api.stackexchange.com/2.3/questions?order=desc&sort=votes&site=stackoverflow&pagesize=1) |
| `E001385` | `huggingface` | 200 | 2026-09-27T00:13:12Z | `91a1625949c70b0e` | 542 | `pipeline` | `wire` | [open](https://huggingface.co/api/models?sort=trendingScore&limit=1) |
| `E001386` | `worldbank` | 200 | 2026-09-27T00:13:12Z | `0302192ef40cbef6` | 302 | `pipeline` | `wire` | [open](https://api.worldbank.org/v2/country/USA/indicator/NY.GDP.MKTP.CD?format=json&per_page=1) |
| `E001387` | `ecb_sdmx` | 200 | 2026-09-27T00:13:12Z | `cb4ff7c2521b49ab` | 3,064 | `pipeline` | `wire` | [open](https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A?lastNObservations=1&format=jsondata) |
| `E001388` | `frankfurter` | 200 | 2026-09-27T00:13:12Z | `2e164d2a233b98ef` | 85 | `pipeline` | `wire` | [open](https://api.frankfurter.app/latest?from=USD&to=EUR,KRW) |
| `E001389` | `europepmc` | 200 | 2026-09-27T00:13:12Z | `66040fc60246efaf` | 1,104 | `pipeline` | `wire` | [open](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=artificial+intelligence&format=json&pageSize=1) |
| `E001390` | `kalshi_public` | 200 | 2026-09-27T00:13:12Z | `4cf50a1566f845a5` | 2,332 | `pipeline` | `wire` | [open](https://api.elections.kalshi.com/trade-api/v2/markets?limit=1) |

`wire` means SHA-256 covers the exact complete bytes handed to the adapter;
`projection` means only a canonical parsed projection was retained. Projection
rows remain usable legacy evidence but are never relabelled as wire-verifiable.

## 4. Library accounting

| | |
|---|---|
| Topics tracked | 187 |
| Topics with ≥1 claim row naming them (row-provable) | 163 |
| Topics with only pre-schema-v2 credit (not row-provable) | 19 |
| Topics with neither | 5 |
| Candidate / active / retired / blocked | 12 / 175 / 0 / 0 |
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
