# VERIFICATION — line-by-line audit ledger

Generated `2026-09-22T01:34:57Z` at cycle 3. Read-only verifiers:
`python3 -m msl.cli verify-claims` and `python3 tools/probe_sources.py`.

## 1. Claim ledger composition

| Kind | Count | What it means |
|---|---|---|
| `captured` | 1,198 | A value lifted from a payload this project read |
| `documented` | 0 | A value from the operator's own published record |
| `negative` | 0 | Proof that something does **not** exist |
| `derived` | 375 | Arithmetic over claims above, formula recorded |
| **Total accepted** | **1,573** | |
| Rejected by the gate | 0 | Published, not swallowed |

## 2. Source registry

28 sources. `status` is written only by the probe.

| # | Id | Name | Operator | Status | Live reads | Last read (UTC) | HTTP | Links |
|---|---|---|---|---|---|---|---|---|
| 1 | `arxiv` | arXiv API | arXiv (Cornell University) | `registered` | 0 | — | — | [docs](https://info.arxiv.org/help/api/index.html) · [probe](https://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results=1) |
| 2 | `bls` | U.S. Bureau of Labor Statistics Public Data API v2 | U.S. Bureau of Labor Statistics | `registered` | 0 | — | — | [docs](https://www.bls.gov/developers/home.htm) · [probe](https://api.bls.gov/publicAPI/v2/timeseries/data/CUUR0000SA0) |
| 3 | `census_acs` | U.S. Census Bureau API (ACS 5-year) | U.S. Census Bureau | `registered` | 0 | — | — | [docs](https://www.census.gov/data/developers/data-sets.html) · [probe](https://api.census.gov/data/2022/acs/acs5?get=NAME,B01001_001E&for=state:06) |
| 4 | `clinicaltrials` | ClinicalTrials.gov API v2 | U.S. National Library of Medicine | `registered` | 0 | — | — | [docs](https://clinicaltrials.gov/data-api/api) · [probe](https://clinicaltrials.gov/api/v2/studies?pageSize=1) |
| 5 | `crossref` | Crossref REST API | Crossref | `registered` | 0 | — | — | [docs](https://www.crossref.org/documentation/retrieve-metadata/rest-api/) · [probe](https://api.crossref.org/works?rows=1&sort=created&order=desc) |
| 6 | `ecb_sdmx` | ECB Data Portal — SDMX REST (EXR daily) | European Central Bank | `registered` | 0 | — | — | [docs](https://data-explorer.ecb.europa.eu/) · [probe](https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A?lastNObservations=1&format=jsondata) |
| 7 | `europepmc` | Europe PMC REST | European Molecular Biology Laboratory | `registered` | 0 | — | — | [docs](https://europepmc.org/RestfulWebService) · [probe](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=artificial+intelligence&format=json&pageSize=1) |
| 8 | `federal_register` | Federal Register API v1 | U.S. National Archives / Office of the Federal Register | `verified-live-read` | 1 | 2026-09-21T22:58:00Z | 200 | [docs](https://www.federalregister.gov/developers/documentation/api/v1) · [probe](https://www.federalregister.gov/api/v1/documents.json?per_page=1&order=newest) |
| 9 | `frankfurter` | Frankfurter FX (ECB reference rates mirror) | Community service publishing ECB reference rates | `registered` | 0 | — | — | [docs](https://www.frankfurter.app/) · [probe](https://api.frankfurter.app/latest?from=USD&to=EUR,KRW) |
| 10 | `github_repos` | GitHub Repos API — owner corpus | GitHub, Inc. | `verified-live-read` | 2 | 2026-09-21T22:50:50Z | 200 | [docs](https://docs.github.com/en/rest/repos/repos) · [probe](https://api.github.com/users/buffedlizard55-lab/repos?per_page=1) |
| 11 | `github_search` | GitHub Search API — repositories | GitHub, Inc. | `verified-live-read` | 6 | 2026-09-21T22:50:50Z | 200 | [docs](https://docs.github.com/en/rest/search/search) · [probe](https://api.github.com/search/repositories?q=created:%3E=2026-09-14&sort=stars&order=desc&per_page=1) |
| 12 | `hn_firebase` | Hacker News official Firebase API | Hacker News / Y Combinator | `verified-live-read` | 1 | 2026-09-21T22:48:00Z | 200 | [docs](https://github.com/HackerNews/API) · [probe](https://hacker-news.firebaseio.com/v0/topstories.json) |
| 13 | `huggingface` | Hugging Face Hub API | Hugging Face, Inc. | `registered` | 0 | — | — | [docs](https://huggingface.co/docs/hub/api) · [probe](https://huggingface.co/api/models?sort=trendingScore&limit=1) |
| 14 | `kalshi_public` | Kalshi public market data | KalshiEX LLC | `registered` | 0 | — | — | [docs](https://trading-api.readme.io/reference/getmarkets) · [probe](https://api.elections.kalshi.com/trade-api/v2/markets?limit=1) |
| 15 | `mlb_statsapi` | MLB StatsAPI — schedule | Major League Baseball Advanced Media | `registered` | 0 | — | — | [docs](https://statsapi.mlb.com/) · [probe](https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=2026-09-20) |
| 16 | `nba_cdn` | NBA CDN — today's scoreboard | National Basketball Association | `registered` | 0 | — | — | [docs](https://cdn.nba.com/) · [probe](https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json) |
| 17 | `nhl_web` | NHL public web API — scoreboard | National Hockey League | `registered` | 0 | — | — | [docs](https://api-web.nhle.com/) · [probe](https://api-web.nhle.com/v1/scoreboard/now) |
| 18 | `nominatim` | OpenStreetMap Nominatim | OpenStreetMap Foundation | `registered` | 0 | — | — | [docs](https://nominatim.org/release-docs/latest/api/Search/) · [probe](https://nominatim.openstreetmap.org/search?q=Seoul&format=json&limit=1) |
| 19 | `npm_registry` | npm Registry — package metadata | GitHub, Inc. (npm) | `verified-live-read` | 2 | 2026-09-21T22:55:00Z | 200 | [docs](https://github.com/npm/registry) · [probe](https://registry.npmjs.org/next/latest) |
| 20 | `nws_alerts` | api.weather.gov — active alerts | U.S. National Weather Service (NOAA) | `registered` | 0 | — | — | [docs](https://www.weather.gov/documentation/services-web-api) · [probe](https://api.weather.gov/alerts/active?area=CA) |
| 21 | `openalex` | OpenAlex scholarly graph | OurResearch (open catalogue of scholarly works) | `registered` | 0 | — | — | [docs](https://docs.openalex.org/) · [probe](https://api.openalex.org/works?sort=publication_date:desc&per-page=1) |
| 22 | `pubmed` | NCBI PubMed E-utilities | U.S. National Library of Medicine | `registered` | 0 | — | — | [docs](https://www.ncbi.nlm.nih.gov/books/NBK25501/) · [probe](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=artificial+intelligence&retmax=1&retmode=json) |
| 23 | `pypi_json` | PyPI JSON API | Python Software Foundation | `verified-live-read` | 4 | 2026-09-21T22:52:00Z | 200 | [docs](https://docs.pypi.org/api/json/) · [probe](https://pypi.org/pypi/requests/json) |
| 24 | `sec_edgar` | SEC EDGAR — company submissions | U.S. Securities and Exchange Commission | `registered` | 0 | — | — | [docs](https://www.sec.gov/edgar/sec-api-documentation) · [probe](https://data.sec.gov/submissions/CIK0000320193.json) |
| 25 | `stackexchange` | Stack Exchange API 2.3 | Stack Exchange, Inc. | `registered` | 0 | — | — | [docs](https://api.stackexchange.com/docs) · [probe](https://api.stackexchange.com/2.3/questions?order=desc&sort=votes&site=stackoverflow&pagesize=1) |
| 26 | `usgs_fdsn` | USGS Earthquake Hazards — FDSN event service | U.S. Geological Survey | `verified-live-read` | 1 | 2026-09-21T22:58:00Z | 200 | [docs](https://earthquake.usgs.gov/fdsnws/event/1/) · [probe](https://earthquake.usgs.gov/fdsnws/event/1/count?format=geojson&starttime=2026-09-14&minmagnitude=5.0) |
| 27 | `wikimedia_pageviews` | Wikimedia Pageviews REST API | Wikimedia Foundation | `verified-live-read` | 1 | 2026-09-21T22:58:00Z | 200 | [docs](https://wikimedia.org/api/rest_v1/) · [probe](https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/Artificial_intelligence/daily/20260914/20260920) |
| 28 | `worldbank` | World Bank Open Data API | The World Bank | `registered` | 0 | — | — | [docs](https://datahelpdesk.worldbank.org/knowledgebase/articles/889392) · [probe](https://api.worldbank.org/v2/country/USA/indicator/NY.GDP.MKTP.CD?format=json&per_page=1) |

## 3. Most recent evidence rows

Every row is one outbound read, with the hash of what came back.

| Id | Source | HTTP | Captured (UTC) | SHA-256 (16) | Bytes | Capture mode | Wire-hash verifiable | URL |
|---|---|---|---|---|---|---|---|---|
| `E000001` | `federal_register` | 200 | 2026-09-21T22:58:00Z | `75c6f85d3c59152b` | 0 | `offline-fixture` | **no** | [open](https://www.federalregister.gov/api/v1/documents.json?per_page=2&order=newest&conditions%5Bterm%5D=artificial+intelligence) |
| `E000002` | `github_search` | 200 | 2026-09-21T23:23:48Z | `79f9fd4448941b2c` | 0 | `offline-fixture` | yes | [open](https://api.github.com/search/repositories?q=AI%20agents%20created%3A%3E%3D2026-08-22&sort=stars&order=desc&per_page=25) |
| `E000003` | `github_search` | 200 | 2026-09-21T23:23:49Z | `4ca9ecebbe93b49f` | 0 | `offline-fixture` | yes | [open](https://api.github.com/search/repositories?q=LLM%20reasoning%20created%3A%3E%3D2026-08-22&sort=stars&order=desc&per_page=25) |
| `E000004` | `github_search` | 200 | 2026-09-21T23:23:47Z | `0b7b90f72cd7204f` | 0 | `offline-fixture` | yes | [open](https://api.github.com/search/repositories?q=created%3A%3E%3D2026-09-14&sort=stars&order=desc&per_page=25) |
| `E000005` | `github_search` | 200 | 2026-09-21T23:23:50Z | `bb66caa1cb1bbcdc` | 0 | `offline-fixture` | yes | [open](https://api.github.com/search/repositories?q=prediction%20markets%20created%3A%3E%3D2026-06-23&sort=stars&order=desc&per_page=25) |
| `E000006` | `github_search` | 200 | 2026-09-21T23:23:51Z | `b6a0d82cf25219c6` | 0 | `offline-fixture` | yes | [open](https://api.github.com/search/repositories?q=sports%20analytics%20created%3A%3E%3D2026-06-23&sort=stars&order=desc&per_page=25) |
| `E000007` | `hn_firebase` | 200 | 2026-09-21T22:48:00Z | `5d329219ef76ef31` | 0 | `offline-fixture` | **no** | [open](https://hacker-news.firebaseio.com/v0/topstories.json) |
| `E000008` | `npm_registry` | 200 | 2026-09-21T23:18:26Z | `eea6c337451e9a0c` | 0 | `offline-fixture` | yes | [open](https://registry.npmjs.org/next/latest) |
| `E000009` | `npm_registry` | 200 | 2026-09-21T23:18:27Z | `61fff5eb6b3412bf` | 0 | `offline-fixture` | yes | [open](https://registry.npmjs.org/react/latest) |
| `E000010` | `npm_registry` | 200 | 2026-09-21T23:18:27Z | `5bf7d3fcc3deef06` | 0 | `offline-fixture` | yes | [open](https://registry.npmjs.org/typescript/latest) |
| `E000011` | `npm_registry` | 200 | 2026-09-21T23:18:27Z | `bdddcdf85c4c7450` | 0 | `offline-fixture` | yes | [open](https://registry.npmjs.org/vite/latest) |
| `E000012` | `github_repos` | 200 | 2026-09-21T23:18:26Z | `dc038d8e4f93cdeb` | 0 | `offline-fixture` | yes | [open](https://api.github.com/users/buffedlizard55-lab/repos?per_page=100&sort=updated) |
| `E000013` | `pypi_json` | 200 | 2026-09-21T23:19:23Z | `c2fb479a413b53e0` | 0 | `offline-fixture` | yes | [open](https://pypi.org/pypi/numpy/json) |
| `E000014` | `pypi_json` | 200 | 2026-09-21T23:19:23Z | `9b33e8fbc8dc6071` | 0 | `offline-fixture` | yes | [open](https://pypi.org/pypi/pandas/json) |
| `E000015` | `pypi_json` | 200 | 2026-09-21T23:18:26Z | `962970177b88d8c7` | 0 | `offline-fixture` | yes | [open](https://pypi.org/pypi/requests/json) |
| `E000016` | `pypi_json` | 200 | 2026-09-21T23:19:23Z | `548b57ac90879d90` | 0 | `offline-fixture` | yes | [open](https://pypi.org/pypi/scikit-learn/json) |
| `E000017` | `usgs_fdsn` | 200 | 2026-09-21T22:56:00Z | `1c518a97113f6d77` | 0 | `offline-fixture` | **no** | [open](https://earthquake.usgs.gov/fdsnws/event/1/count?format=geojson&starttime=2026-09-14&minmagnitude=5.0) |
| `E000018` | `wikimedia_pageviews` | 200 | 2026-09-21T22:58:00Z | `e60a37eff2a9a9f2` | 0 | `offline-fixture` | **no** | [open](https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/Artificial_intelligence/daily/20260914/20260920) |
| `E000019` | `github_search` | 200 | 2026-09-21T23:37:38Z | `1d8dfca28433d4db` | 0 | `offline-fixture` | yes | [open](https://api.github.com/search/repositories?q=AI%20agents%20created%3A%3E%3D2026-08-22&sort=stars&order=desc&per_page=25) |
| `E000020` | `github_search` | 200 | 2026-09-21T23:37:39Z | `d7134cbce5e1f5fa` | 0 | `offline-fixture` | yes | [open](https://api.github.com/search/repositories?q=LLM%20reasoning%20created%3A%3E%3D2026-08-22&sort=stars&order=desc&per_page=25) |
| `E000021` | `github_search` | 200 | 2026-09-21T23:37:37Z | `0dda95338742511b` | 0 | `offline-fixture` | yes | [open](https://api.github.com/search/repositories?q=created%3A%3E%3D2026-09-14&sort=stars&order=desc&per_page=25) |
| `E000022` | `github_search` | 200 | 2026-09-21T23:37:40Z | `47281c4652a7aafe` | 0 | `offline-fixture` | yes | [open](https://api.github.com/search/repositories?q=prediction%20markets%20created%3A%3E%3D2026-06-23&sort=stars&order=desc&per_page=25) |
| `E000023` | `github_search` | 200 | 2026-09-21T23:37:41Z | `b6a0d82cf25219c6` | 0 | `offline-fixture` | yes | [open](https://api.github.com/search/repositories?q=sports%20analytics%20created%3A%3E%3D2026-06-23&sort=stars&order=desc&per_page=25) |
| `E000024` | `npm_registry` | 200 | 2026-09-21T23:37:42Z | `eea6c337451e9a0c` | 0 | `offline-fixture` | yes | [open](https://registry.npmjs.org/next/latest) |
| `E000025` | `npm_registry` | 200 | 2026-09-21T23:37:42Z | `61fff5eb6b3412bf` | 0 | `offline-fixture` | yes | [open](https://registry.npmjs.org/react/latest) |
| `E000026` | `npm_registry` | 200 | 2026-09-21T23:37:42Z | `5bf7d3fcc3deef06` | 0 | `offline-fixture` | yes | [open](https://registry.npmjs.org/typescript/latest) |
| `E000027` | `npm_registry` | 200 | 2026-09-21T23:37:42Z | `bdddcdf85c4c7450` | 0 | `offline-fixture` | yes | [open](https://registry.npmjs.org/vite/latest) |
| `E000028` | `github_repos` | 200 | 2026-09-21T23:37:42Z | `6fd06a52f668c850` | 0 | `offline-fixture` | yes | [open](https://api.github.com/users/buffedlizard55-lab/repos?per_page=100&sort=updated) |
| `E000029` | `pypi_json` | 200 | 2026-09-21T23:37:42Z | `962970177b88d8c7` | 0 | `offline-fixture` | yes | [open](https://pypi.org/pypi/requests/json) |
| `E000030` | `github_search` | 200 | 2026-09-21T23:37:38Z | `1d8dfca28433d4db` | 0 | `offline-fixture` | yes | [open](https://api.github.com/search/repositories?q=AI%20agents%20created%3A%3E%3D2026-08-22&sort=stars&order=desc&per_page=25) |
| `E000031` | `github_search` | 200 | 2026-09-21T23:37:39Z | `d7134cbce5e1f5fa` | 0 | `offline-fixture` | yes | [open](https://api.github.com/search/repositories?q=LLM%20reasoning%20created%3A%3E%3D2026-08-22&sort=stars&order=desc&per_page=25) |
| `E000032` | `github_search` | 200 | 2026-09-21T23:37:37Z | `0dda95338742511b` | 0 | `offline-fixture` | yes | [open](https://api.github.com/search/repositories?q=created%3A%3E%3D2026-09-14&sort=stars&order=desc&per_page=25) |
| `E000033` | `github_search` | 200 | 2026-09-21T23:37:40Z | `47281c4652a7aafe` | 0 | `offline-fixture` | yes | [open](https://api.github.com/search/repositories?q=prediction%20markets%20created%3A%3E%3D2026-06-23&sort=stars&order=desc&per_page=25) |
| `E000034` | `github_search` | 200 | 2026-09-21T23:37:41Z | `b6a0d82cf25219c6` | 0 | `offline-fixture` | yes | [open](https://api.github.com/search/repositories?q=sports%20analytics%20created%3A%3E%3D2026-06-23&sort=stars&order=desc&per_page=25) |
| `E000035` | `npm_registry` | 200 | 2026-09-21T23:37:42Z | `eea6c337451e9a0c` | 0 | `offline-fixture` | yes | [open](https://registry.npmjs.org/next/latest) |
| `E000036` | `npm_registry` | 200 | 2026-09-21T23:37:42Z | `61fff5eb6b3412bf` | 0 | `offline-fixture` | yes | [open](https://registry.npmjs.org/react/latest) |
| `E000037` | `npm_registry` | 200 | 2026-09-21T23:37:42Z | `5bf7d3fcc3deef06` | 0 | `offline-fixture` | yes | [open](https://registry.npmjs.org/typescript/latest) |
| `E000038` | `npm_registry` | 200 | 2026-09-21T23:37:42Z | `bdddcdf85c4c7450` | 0 | `offline-fixture` | yes | [open](https://registry.npmjs.org/vite/latest) |
| `E000039` | `github_repos` | 200 | 2026-09-21T23:37:42Z | `6fd06a52f668c850` | 0 | `offline-fixture` | yes | [open](https://api.github.com/users/buffedlizard55-lab/repos?per_page=100&sort=updated) |
| `E000040` | `pypi_json` | 200 | 2026-09-21T23:37:42Z | `962970177b88d8c7` | 0 | `offline-fixture` | yes | [open](https://pypi.org/pypi/requests/json) |

`wire-hash verifiable = no` means the body was recorded by an interactive agent
read rather than by the pipeline, so the stored hash covers the recorded body and
not the bytes on the wire. Those rows are re-read by the next probe.

## 4. Library accounting

| | |
|---|---|
| Topics tracked | 31 |
| Topics with ≥1 verified claim | 5 |
| Topics with 0 verified claims | 26 |
| Candidate / active / retired / blocked | 10 / 20 / 0 / 1 |
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
