# STATUS — cycle 26

Generated `2026-09-23T07:19:33Z` by `msl/docs.py`. Every figure here is read from the same
objects the site is built from.

## Last cycle

| | |
|---|---|
| Cycle | 26 |
| Mode | `github-actions` |
| Duration | 30,645 ms |
| Reads (ok / failed) | 63 / 4 |
| Bytes read | 2,413,508 |
| Facts extracted | 742 |
| New claims | 742 |
| Claims rejected by the gate this cycle | 0 |
| Gate rejections in append-only history | 0 |
| Derived / rechecked / drifted | 408 / 2,469 / 0 |
| Topics (new) | 169 (6) |
| Insights published | 423 |
| Forecasts issued / scored | 1224 / 653 |
| Ideas (promoted) | 28 (1) |
| Irregularities open (new) | 27 (0) |
| Pipeline errors | 0 |

No pipeline stage raised.

## Open critical irregularities

| Id | Title | First seen | Reproduce |
|---|---|---|---|
| `IRR-043` | clinicaltrials could not be read | cycle 4 | `curl -sS -o /dev/null -w '%{http_code}\n' 'https://clinicaltrials.gov/api/v2/studies?pageSize=1&countTotal=true&query.term=artificial%20intelligence'` |
| `IRR-046` | sec_edgar could not be read | cycle 4 | `curl -sS -o /dev/null -w '%{http_code}\n' 'https://data.sec.gov/submissions/CIK0000320193.json'` |
| `IRR-049` | nba_cdn could not be read | cycle 4 | `curl -sS -o /dev/null -w '%{http_code}\n' 'https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json'` |

## Register totals

123 registered — 6 critical,
72 warn, 45 info;
27 open, 96 resolved,
21 standing.

## Recent cycles

| Cycle | At (UTC) | Claims | Topics | New | Forecasts | Scored | Ideas | Irr open | Result |
|---|---|---|---|---|---|---|---|---|---|
| 17 | 2026-09-22T17:24:28Z | 14,042 | 115 | 6 | 1138 | 105 | 24 | 31 | ok |
| 18 | 2026-09-22T17:31:33Z | 15,107 | 121 | 6 | 1153 | 1215 | 24 | 32 | ok |
| 19 | 2026-09-22T19:08:58Z | 15,820 | 127 | 6 | 1143 | 2256 | 25 | 24 | ok |
| 20 | 2026-09-22T19:23:59Z | 16,532 | 133 | 6 | 1091 | 496 | 25 | 24 | ok |
| 21 | 2026-09-22T20:34:15Z | 17,640 | 139 | 6 | 1137 | 1856 | 28 | 27 | ok |
| 22 | 2026-09-22T20:52:29Z | 18,737 | 145 | 6 | 1070 | 749 | 28 | 29 | ok |
| 23 | 2026-09-22T23:28:37Z | 19,851 | 151 | 6 | 1116 | 684 | 28 | 27 | ok |
| 24 | 2026-09-22T23:43:29Z | 20,947 | 157 | 6 | 1056 | 717 | 28 | 27 | ok |
| 25 | 2026-09-23T01:42:26Z | 22,070 | 163 | 6 | 1110 | 655 | 28 | 27 | ok |
| 26 | 2026-09-23T07:19:33Z | 23,220 | 169 | 6 | 1224 | 653 | 28 | 27 | ok |

## What runs next

`.github/workflows/think.yml` fires on `*/30 * * * *` and needs no input.
`probe.yml` live-reads every registered source daily and publishes the health
ledger. `tests.yml` runs the suite on every push and pull request.
