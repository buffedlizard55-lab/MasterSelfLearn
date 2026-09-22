# VERIFICATION — line-by-line audit ledger

Generated `2026-09-22T17:31:33Z` at cycle 18. Read-only verifiers:
`python3 -m msl.cli verify-claims` and `python3 tools/probe_sources.py`.

## 1. Claim ledger composition

| Kind | Count | What it means |
|---|---|---|
| `captured` | 9,986 | A value lifted from a payload this project read |
| `documented` | 0 | A value from the operator's own published record |
| `negative` | 6 | Proof that something does **not** exist |
| `derived` | 5,115 | Arithmetic over claims above, formula recorded |
| **Total accepted** | **15,107** | |
| Rejected by the gate | 0 | Published, not swallowed |

## 2. Source registry

30 sources. `status` is written only by the probe.

| # | Id | Name | Operator | Status | Live reads | Last read (UTC) | HTTP | Links |
|---|---|---|---|---|---|---|---|---|
| 1 | `arxiv` | arXiv API | arXiv (Cornell University) | `verified-live-read` | 13 | 2026-09-22T17:31:33Z | 200 | [docs](https://info.arxiv.org/help/api/index.html) · [probe](https://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results=1) |
| 2 | `bls` | U.S. Bureau of Labor Statistics Public Data API v2 | U.S. Bureau of Labor Statistics | `verified-live-read` | 7 | 2026-09-22T17:31:33Z | 200 | [docs](https://www.bls.gov/developers/home.htm) · [probe](https://api.bls.gov/publicAPI/v2/timeseries/data/CUUR0000SA0) |
| 3 | `census_acs` | U.S. Census Bureau API (ACS 5-year) | U.S. Census Bureau | `verified-live-read` | 1 | 2026-09-22T17:24:28Z | 200 | [docs](https://www.census.gov/data/developers/data-sets.html) · [probe](https://api.census.gov/data/2022/acs/acs5?get=NAME,B01001_001E&for=state:06) |
| 4 | `clinicaltrials` | ClinicalTrials.gov API v2 | U.S. National Library of Medicine | `blocked` | 0 | 2026-09-22T17:31:33Z | 403 | [docs](https://clinicaltrials.gov/data-api/api) · [probe](https://clinicaltrials.gov/api/v2/studies?pageSize=1) |
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
| 17 | `mlb_statsapi` | MLB StatsAPI — schedule | Major League Baseball Advanced Media | `verified-live-read` | 8 | 2026-09-22T17:31:33Z | 200 | [docs](https://statsapi.mlb.com/) · [probe](https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=2026-09-20) |
| 18 | `nba_cdn` | NBA CDN — today's scoreboard | National Basketball Association | `blocked` | 0 | 2026-09-22T17:31:33Z | 403 | [docs](https://cdn.nba.com/) · [probe](https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json) |
| 19 | `nhl_web` | NHL public web API — scoreboard | National Hockey League | `verified-live-read` | 7 | 2026-09-22T17:31:33Z | 200 | [docs](https://api-web.nhle.com/) · [probe](https://api-web.nhle.com/v1/scoreboard/now) |
| 20 | `nominatim` | OpenStreetMap Nominatim | OpenStreetMap Foundation | `verified-live-read` | 7 | 2026-09-22T17:31:33Z | 200 | [docs](https://nominatim.org/release-docs/latest/api/Search/) · [probe](https://nominatim.openstreetmap.org/search?q=Seoul&format=json&limit=1) |
| 21 | `npm_registry` | npm Registry — package metadata | GitHub, Inc. (npm) | `verified-live-read` | 9 | 2026-09-22T17:31:33Z | 200 | [docs](https://github.com/npm/registry) · [probe](https://registry.npmjs.org/next/latest) |
| 22 | `nws_alerts` | api.weather.gov — active alerts | U.S. National Weather Service (NOAA) | `verified-live-read` | 7 | 2026-09-22T17:31:33Z | 200 | [docs](https://www.weather.gov/documentation/services-web-api) · [probe](https://api.weather.gov/alerts/active?area=CA) |
| 23 | `openalex` | OpenAlex scholarly graph | OurResearch (open catalogue of scholarly works) | `verified-live-read` | 13 | 2026-09-22T17:31:33Z | 200 | [docs](https://docs.openalex.org/) · [probe](https://api.openalex.org/works?sort=publication_date:desc&per-page=1) |
| 24 | `pubmed` | NCBI PubMed E-utilities | U.S. National Library of Medicine | `verified-live-read` | 19 | 2026-09-22T17:31:33Z | 200 | [docs](https://www.ncbi.nlm.nih.gov/books/NBK25501/) · [probe](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=artificial+intelligence&retmax=1&retmode=json) |
| 25 | `pypi_json` | PyPI JSON API | Python Software Foundation | `verified-live-read` | 9 | 2026-09-22T17:31:33Z | 200 | [docs](https://docs.pypi.org/api/json/) · [probe](https://pypi.org/pypi/requests/json) |
| 26 | `sec_edgar` | SEC EDGAR — company submissions | U.S. Securities and Exchange Commission | `blocked` | 0 | 2026-09-22T17:31:33Z | 403 | [docs](https://www.sec.gov/edgar/sec-api-documentation) · [probe](https://data.sec.gov/submissions/CIK0000320193.json) |
| 27 | `stackexchange` | Stack Exchange API 2.3 | Stack Exchange, Inc. | `verified-live-read` | 13 | 2026-09-22T17:31:33Z | 200 | [docs](https://api.stackexchange.com/docs) · [probe](https://api.stackexchange.com/2.3/questions?order=desc&sort=votes&site=stackoverflow&pagesize=1) |
| 28 | `usgs_fdsn` | USGS Earthquake Hazards — FDSN event service | U.S. Geological Survey | `verified-live-read` | 9 | 2026-09-22T17:31:33Z | 200 | [docs](https://earthquake.usgs.gov/fdsnws/event/1/) · [probe](https://earthquake.usgs.gov/fdsnws/event/1/count?format=geojson&starttime=2026-09-14&minmagnitude=5.0) |
| 29 | `wikimedia_pageviews` | Wikimedia Pageviews REST API | Wikimedia Foundation | `verified-live-read` | 13 | 2026-09-22T17:31:33Z | 200 | [docs](https://wikimedia.org/api/rest_v1/) · [probe](https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/Artificial_intelligence/daily/20260914/20260920) |
| 30 | `worldbank` | World Bank Open Data API | The World Bank | `verified-live-read` | 13 | 2026-09-22T17:31:33Z | 200 | [docs](https://datahelpdesk.worldbank.org/knowledgebase/articles/889392) · [probe](https://api.worldbank.org/v2/country/USA/indicator/NY.GDP.MKTP.CD?format=json&per_page=1) |

## 3. Most recent evidence rows

Every row is one outbound read, with the hash of what came back.

| Id | Source | HTTP | Captured (UTC) | SHA-256 (16) | Bytes | Capture mode | Wire-hash verifiable | URL |
|---|---|---|---|---|---|---|---|---|
| `E000758` | `npm_registry` | 200 | 2026-09-22T17:31:33Z | `e4cd043c8c51480b` | 0 | `pipeline` | yes | [open](https://registry.npmjs.org/next/latest) |
| `E000759` | `wikimedia_pageviews` | 200 | 2026-09-22T17:31:33Z | `e60a37eff2a9a9f2` | 0 | `pipeline` | yes | [open](https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/Artificial_intelligence/daily/20260914/20260920) |
| `E000760` | `federal_register` | 200 | 2026-09-22T17:31:33Z | `e0c2219928591dcd` | 0 | `pipeline` | yes | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=1&order=newest) |
| `E000761` | `usgs_fdsn` | 200 | 2026-09-22T17:31:33Z | `e03d2fd1c6c497e9` | 0 | `pipeline` | yes | [open](https://earthquake.usgs.gov/fdsnws/event/1/count?format=geojson&starttime=2026-09-14&minmagnitude=5.0) |
| `E000762` | `hn_firebase` | 200 | 2026-09-22T17:31:33Z | `d67d660ba78843ef` | 0 | `pipeline` | yes | [open](https://hacker-news.firebaseio.com/v0/topstories.json) |
| `E000763` | `arxiv` | 200 | 2026-09-22T17:31:33Z | `0425092b419b8660` | 4,225 | `pipeline` | yes | [open](https://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results=1) |
| `E000764` | `pubmed` | 200 | 2026-09-22T17:31:33Z | `b06ef3a5d29eb9b9` | 0 | `pipeline` | yes | [open](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=artificial+intelligence&retmax=1&retmode=json) |
| `E000765` | `openalex` | 200 | 2026-09-22T17:31:33Z | `f255184ea043edf8` | 0 | `pipeline` | yes | [open](https://api.openalex.org/works?sort=publication_date:desc&per-page=1) |
| `E000766` | `crossref` | 200 | 2026-09-22T17:31:33Z | `4311b3e4f9a32b03` | 0 | `pipeline` | yes | [open](https://api.crossref.org/works?rows=1&sort=created&order=desc) |
| `E000767` | `stackexchange` | 200 | 2026-09-22T17:31:33Z | `0bf0a701091005a8` | 0 | `pipeline` | yes | [open](https://api.stackexchange.com/2.3/questions?order=desc&sort=votes&site=stackoverflow&pagesize=1) |
| `E000768` | `huggingface` | 200 | 2026-09-22T17:31:33Z | `d676623f014b36f9` | 0 | `pipeline` | yes | [open](https://huggingface.co/api/models?sort=trendingScore&limit=1) |
| `E000769` | `nws_alerts` | 200 | 2026-09-22T17:31:33Z | `fe57bd047b514787` | 0 | `pipeline` | yes | [open](https://api.weather.gov/alerts/active?area=CA) |
| `E000770` | `worldbank` | 200 | 2026-09-22T17:31:33Z | `57ee09ac4cf11069` | 0 | `pipeline` | yes | [open](https://api.worldbank.org/v2/country/USA/indicator/NY.GDP.MKTP.CD?format=json&per_page=1) |
| `E000771` | `ecb_sdmx` | 200 | 2026-09-22T17:31:33Z | `c5c45d6920d8d496` | 0 | `pipeline` | yes | [open](https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A?lastNObservations=1&format=jsondata) |
| `E000772` | `frankfurter` | 200 | 2026-09-22T17:31:33Z | `381be2b6421062ad` | 0 | `pipeline` | yes | [open](https://api.frankfurter.app/latest?from=USD&to=EUR,KRW) |
| `E000773` | `bls` | 200 | 2026-09-22T17:31:33Z | `b387740eafd70264` | 0 | `pipeline` | yes | [open](https://api.bls.gov/publicAPI/v2/timeseries/data/CUUR0000SA0) |
| `E000774` | `nominatim` | 200 | 2026-09-22T17:31:33Z | `9d37c36d1474d973` | 0 | `pipeline` | yes | [open](https://nominatim.openstreetmap.org/search?q=Seoul&format=json&limit=1) |
| `E000775` | `europepmc` | 200 | 2026-09-22T17:31:33Z | `1c7813ae14ce83aa` | 0 | `pipeline` | yes | [open](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=artificial+intelligence&format=json&pageSize=1) |
| `E000776` | `kalshi_public` | 200 | 2026-09-22T17:31:33Z | `1b76d3a2e51455b8` | 0 | `pipeline` | yes | [open](https://api.elections.kalshi.com/trade-api/v2/markets?limit=1) |
| `E000777` | `mlb_statsapi` | 200 | 2026-09-22T17:31:33Z | `380848368ace97b5` | 0 | `pipeline` | yes | [open](https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=2026-09-20) |
| `E000778` | `nhl_web` | 200 | 2026-09-22T17:31:33Z | `c8466c2c5de84065` | 0 | `pipeline` | yes | [open](https://api-web.nhle.com/v1/scoreboard/now) |
| `E000779` | `federal_register` | 200 | 2026-09-22T17:31:33Z | `07411d02f41e7b80` | 0 | `pipeline` | yes | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=reasoning) |
| `E000780` | `federal_register` | 200 | 2026-09-22T17:31:33Z | `78a7e5434d1dd48c` | 0 | `pipeline` | yes | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=agent) |
| `E000781` | `federal_register` | 200 | 2026-09-22T17:31:33Z | `fe3c47d93b552160` | 0 | `pipeline` | yes | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=model) |
| `E000782` | `federal_register` | 200 | 2026-09-22T17:31:33Z | `c361d387d18f7856` | 0 | `pipeline` | yes | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=transformer) |
| `E000783` | `arxiv` | 200 | 2026-09-22T17:31:33Z | `f5caa8ed115321eb` | 21,957 | `pipeline` | yes | [open](https://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results=8) |
| `E000784` | `openalex` | 200 | 2026-09-22T17:31:33Z | `b5ab158e450b0b78` | 0 | `pipeline` | yes | [open](https://api.openalex.org/works?sort=publication_date:desc&per-page=5&mailto=buffedlizard55@gmail.com) |
| `E000785` | `crossref` | 200 | 2026-09-22T17:31:33Z | `57c0586afda06994` | 0 | `pipeline` | yes | [open](https://api.crossref.org/works?rows=3&sort=created&order=desc&mailto=buffedlizard55@gmail.com) |
| `E000786` | `europepmc` | 200 | 2026-09-22T17:31:33Z | `1931e4be74802a38` | 0 | `pipeline` | yes | [open](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=artificial+intelligence&format=json&pageSize=3) |
| `E000787` | `huggingface` | 200 | 2026-09-22T17:31:33Z | `aefe9247fbee32d4` | 0 | `pipeline` | yes | [open](https://huggingface.co/api/models?sort=trendingScore&limit=10) |
| `E000788` | `github_search` | 200 | 2026-09-22T17:31:33Z | `8d440baab317a0ca` | 0 | `pipeline` | yes | [open](https://api.github.com/search/repositories?q=agent%20created%3A%3E%3D2026-06-24&sort=stars&order=desc&per_page=20) |
| `E000789` | `github_search` | 200 | 2026-09-22T17:31:33Z | `9ed4486fe49a7355` | 0 | `pipeline` | yes | [open](https://api.github.com/search/repositories?q=framework%20created%3A%3E%3D2026-06-24&sort=stars&order=desc&per_page=20) |
| `E000790` | `github_search` | 200 | 2026-09-22T17:31:33Z | `2bf2c46fdab848bf` | 0 | `pipeline` | yes | [open](https://api.github.com/search/repositories?q=agent%20framework%20created%3A%3E%3D2026-09-15&sort=stars&order=desc&per_page=25) |
| `E000791` | `stackexchange` | 200 | 2026-09-22T17:31:33Z | `67220c4e98d7fe81` | 0 | `pipeline` | yes | [open](https://api.stackexchange.com/2.3/questions?order=desc&sort=votes&site=stackoverflow&pagesize=5&tagged=python) |
| `E000792` | `federal_register` | 200 | 2026-09-22T17:31:33Z | `e4ae05a508f6710a` | 0 | `pipeline` | yes | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=artificial%20intelligence) |
| `E000793` | `federal_register` | 200 | 2026-09-22T17:31:33Z | `18dfef318fcab5ef` | 0 | `pipeline` | yes | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=health) |
| `E000794` | `federal_register` | 200 | 2026-09-22T17:31:33Z | `30106a6c299648e4` | 0 | `pipeline` | yes | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=energy) |
| `E000795` | `federal_register` | 200 | 2026-09-22T17:31:33Z | `c860bf76459fa921` | 0 | `pipeline` | yes | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=security) |
| `E000796` | `worldbank` | 200 | 2026-09-22T17:31:33Z | `6553a6ca496b6e6d` | 0 | `pipeline` | yes | [open](https://api.worldbank.org/v2/country/USA/indicator/NY.GDP.MKTP.CD?format=json&per_page=3) |
| `E000797` | `ecb_sdmx` | 200 | 2026-09-22T17:31:33Z | `3d37e0bddf51e2cd` | 0 | `pipeline` | yes | [open](https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A?lastNObservations=3&format=jsondata) |
| `E000798` | `frankfurter` | 200 | 2026-09-22T17:31:33Z | `9eacd95b762066bd` | 0 | `pipeline` | yes | [open](https://api.frankfurter.app/latest?from=USD&to=EUR,KRW,JPY) |
| `E000799` | `usgs_fdsn` | 200 | 2026-09-22T17:31:33Z | `22a174c8d56b27a6` | 0 | `pipeline` | yes | [open](https://earthquake.usgs.gov/fdsnws/event/1/count?format=geojson&starttime=2026-09-09&endtime=2026-09-15&minmagnitude=5.0) |
| `E000800` | `pubmed` | 200 | 2026-09-22T17:31:33Z | `14398236a7e8b413` | 0 | `pipeline` | yes | [open](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=trial&retmax=1&retmode=json) |
| `E000801` | `federal_register` | 200 | 2026-09-22T17:31:33Z | `e58059054f6d29f8` | 0 | `pipeline` | yes | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=public%20health) |
| `E000802` | `federal_register` | 200 | 2026-09-22T17:31:33Z | `f86462d8803caf8a` | 0 | `pipeline` | yes | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=surveillance) |
| `E000803` | `federal_register` | 200 | 2026-09-22T17:31:33Z | `b510a7e519653cde` | 0 | `pipeline` | yes | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest&conditions%5Bterm%5D=data%20exchange) |
| `E000804` | `pubmed` | 200 | 2026-09-22T17:31:33Z | `2817f2beb6de6333` | 0 | `pipeline` | yes | [open](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=cdc&retmax=1&retmode=json) |
| `E000805` | `kalshi_public` | 200 | 2026-09-22T17:31:33Z | `3a9700ab05e95101` | 0 | `pipeline` | yes | [open](https://api.elections.kalshi.com/trade-api/v2/markets?limit=5) |
| `E000806` | `mlb_statsapi` | 200 | 2026-09-22T17:31:33Z | `c8174762b99d1fb2` | 0 | `pipeline` | yes | [open](https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=2026-09-15) |
| `E000807` | `github_search` | 200 | 2026-09-22T17:31:33Z | `47cb0eac8c1e7c6b` | 0 | `pipeline` | yes | [open](https://api.github.com/search/repositories?q=kalshi%20created%3A%3E%3D2026-06-24&sort=stars&order=desc&per_page=20) |
| `E000808` | `github_search` | 200 | 2026-09-22T17:31:33Z | `a748df0135cecd2b` | 0 | `pipeline` | yes | [open](https://api.github.com/search/repositories?q=prediction%20market%20created%3A%3E%3D2026-06-24&sort=stars&order=desc&per_page=20) |
| `E000809` | `github_search` | 200 | 2026-09-22T17:31:33Z | `b388f411ff06cf14` | 0 | `pipeline` | yes | [open](https://api.github.com/search/repositories?q=kalshi%20prediction%20market%20created%3A%3E%3D2026-09-15&sort=stars&order=desc&per_page=25) |
| `E000810` | `github_repos` | 200 | 2026-09-22T17:31:33Z | `aea8bc99fca23076` | 0 | `pipeline` | yes | [open](https://api.github.com/users/buffedlizard55-lab/repos?per_page=100&sort=updated) |
| `E000811` | `wikimedia_pageviews` | 200 | 2026-09-22T17:31:33Z | `2cb3b522b0a3827a` | 0 | `pipeline` | yes | [open](https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/Artificial_intelligence/daily/20260909/20260915) |
| `E000812` | `github_repo` | 200 | 2026-09-22T17:31:33Z | `ae0a546031927075` | 0 | `pipeline` | yes | [open](https://api.github.com/repos/browser-use/jev-ultrafast) |
| `E000813` | `github_releases` | 200 | 2026-09-22T17:31:33Z | `4f53cda18c2baa0c` | 0 | `pipeline` | yes | [open](https://api.github.com/repos/browser-use/jev-ultrafast/releases?per_page=1) |
| `E000814` | `github_repo` | 200 | 2026-09-22T17:31:33Z | `a5a862c39d3ad05c` | 0 | `pipeline` | yes | [open](https://api.github.com/repos/zai-org/ZCode) |
| `E000815` | `github_releases` | 200 | 2026-09-22T17:31:33Z | `4f53cda18c2baa0c` | 0 | `pipeline` | yes | [open](https://api.github.com/repos/zai-org/ZCode/releases?per_page=1) |
| `E000816` | `github_repo` | 200 | 2026-09-22T17:31:33Z | `10b6e01f64b6c2bc` | 0 | `pipeline` | yes | [open](https://api.github.com/repos/brayonpi/hexstellar) |
| `E000817` | `github_releases` | 200 | 2026-09-22T17:31:33Z | `e37e72a0a81dbbf4` | 0 | `pipeline` | yes | [open](https://api.github.com/repos/brayonpi/hexstellar/releases?per_page=1) |

`wire-hash verifiable = no` means the body was recorded by an interactive agent
read rather than by the pipeline, so the stored hash covers the recorded body and
not the bytes on the wire. Those rows are re-read by the next probe.

## 4. Library accounting

| | |
|---|---|
| Topics tracked | 121 |
| Topics with ≥1 verified claim | 12 |
| Topics with 0 verified claims | 109 |
| Candidate / active / retired / blocked | 4 / 116 / 0 / 1 |
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
