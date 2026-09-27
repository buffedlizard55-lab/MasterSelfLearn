# STATUS — cycle 29

Generated `2026-09-27T00:13:12Z` by `msl/docs.py`. Every figure here is read from the same
objects the site is built from.

## Last cycle

| | |
|---|---|
| Cycle | 29 |
| Mode | `github-actions` |
| Duration | 24,291 ms |
| Reads (ok / failed) | 64 / 4 |
| Bytes read | 2,734,983 |
| Facts extracted | 768 |
| New claims | 768 |
| Claims rejected by the gate this cycle | 0 |
| Gate rejections in append-only history | 0 |
| Derived / rechecked / drifted | 463 / 3,058 / 0 |
| Topics (new) | 187 (6) |
| Insights published | 499 |
| Forecasts issued / scored | 1460 / 1277 |
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
| 20 | 2026-09-22T19:23:59Z | 16,532 | 133 | 6 | 1091 | 496 | 25 | 24 | ok |
| 21 | 2026-09-22T20:34:15Z | 17,640 | 139 | 6 | 1137 | 1856 | 28 | 27 | ok |
| 22 | 2026-09-22T20:52:29Z | 18,737 | 145 | 6 | 1070 | 749 | 28 | 29 | ok |
| 23 | 2026-09-22T23:28:37Z | 19,851 | 151 | 6 | 1116 | 684 | 28 | 27 | ok |
| 24 | 2026-09-22T23:43:29Z | 20,947 | 157 | 6 | 1056 | 717 | 28 | 27 | ok |
| 25 | 2026-09-23T01:42:26Z | 22,070 | 163 | 6 | 1110 | 655 | 28 | 27 | ok |
| 26 | 2026-09-23T07:19:33Z | 23,220 | 169 | 6 | 1224 | 653 | 28 | 27 | ok |
| 27 | 2026-09-23T12:54:12Z | 24,393 | 175 | 6 | 1269 | 799 | 28 | 27 | ok |
| 28 | 2026-09-26T21:39:23Z | 25,278 | 181 | 6 | 1291 | 2624 | 28 | 23 | ok |
| 29 | 2026-09-27T00:13:12Z | 26,509 | 187 | 6 | 1460 | 1277 | 28 | 27 | ok |

## What runs next

`.github/workflows/think.yml` fires on `*/30 * * * *` and needs no input.
`probe.yml` live-reads every registered source daily and publishes the health
ledger. `tests.yml` runs the suite on every push and pull request.
