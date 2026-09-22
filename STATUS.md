# STATUS — cycle 24

Generated `2026-09-22T23:43:29Z` by `msl/docs.py`. Every figure here is read from the same
objects the site is built from.

## Last cycle

| | |
|---|---|
| Cycle | 24 |
| Mode | `github-actions` |
| Duration | 31,077 ms |
| Reads (ok / failed) | 62 / 4 |
| Bytes read | 2,226,743 |
| Facts extracted | 724 |
| New claims | 724 |
| Claims rejected by the gate this cycle | 0 |
| Gate rejections in append-only history | 0 |
| Derived / rechecked / drifted | 372 / 2,122 / 0 |
| Topics (new) | 157 (6) |
| Insights published | 408 |
| Forecasts issued / scored | 1056 / 717 |
| Ideas (promoted) | 28 (1) |
| Irregularities open (new) | 27 (2) |
| Pipeline errors | 0 |

No pipeline stage raised.

## Open critical irregularities

| Id | Title | First seen | Reproduce |
|---|---|---|---|
| `IRR-043` | clinicaltrials could not be read | cycle 4 | `curl -sS -o /dev/null -w '%{http_code}\n' 'https://clinicaltrials.gov/api/v2/studies?pageSize=1&countTotal=true&query.term=artificial%20intelligence'` |
| `IRR-046` | sec_edgar could not be read | cycle 4 | `curl -sS -o /dev/null -w '%{http_code}\n' 'https://data.sec.gov/submissions/CIK0000320193.json'` |
| `IRR-049` | nba_cdn could not be read | cycle 4 | `curl -sS -o /dev/null -w '%{http_code}\n' 'https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json'` |

## Register totals

122 registered — 6 critical,
71 warn, 45 info;
27 open, 95 resolved,
21 standing.

## Recent cycles

| Cycle | At (UTC) | Claims | Topics | New | Forecasts | Scored | Ideas | Irr open | Result |
|---|---|---|---|---|---|---|---|---|---|
| 15 | 2026-09-22T07:16:15Z | 12,365 | 103 | 6 | 974 | 496 | 14 | 29 | ok |
| 16 | 2026-09-22T12:45:18Z | 13,388 | 109 | 6 | 1036 | 620 | 14 | 30 | ok |
| 17 | 2026-09-22T17:24:28Z | 14,042 | 115 | 6 | 1138 | 105 | 24 | 31 | ok |
| 18 | 2026-09-22T17:31:33Z | 15,107 | 121 | 6 | 1153 | 1215 | 24 | 32 | ok |
| 19 | 2026-09-22T19:08:58Z | 15,820 | 127 | 6 | 1143 | 2256 | 25 | 24 | ok |
| 20 | 2026-09-22T19:23:59Z | 16,532 | 133 | 6 | 1091 | 496 | 25 | 24 | ok |
| 21 | 2026-09-22T20:34:15Z | 17,640 | 139 | 6 | 1137 | 1856 | 28 | 27 | ok |
| 22 | 2026-09-22T20:52:29Z | 18,737 | 145 | 6 | 1070 | 749 | 28 | 29 | ok |
| 23 | 2026-09-22T23:28:37Z | 19,851 | 151 | 6 | 1116 | 684 | 28 | 27 | ok |
| 24 | 2026-09-22T23:43:29Z | 20,947 | 157 | 6 | 1056 | 717 | 28 | 27 | ok |

## What runs next

`.github/workflows/think.yml` fires on `*/30 * * * *` and needs no input.
`probe.yml` live-reads every registered source daily and publishes the health
ledger. `tests.yml` runs the suite on every push and pull request.
