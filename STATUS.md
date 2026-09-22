# STATUS — cycle 16

Generated `2026-09-22T12:45:18Z` by `msl/docs.py`. Every figure here is read from the same
objects the site is built from.

## Last cycle

| | |
|---|---|
| Cycle | 16 |
| Mode | `github-actions` |
| Duration | 89813 ms |
| Reads (ok / failed) | 63 / 7 |
| Bytes read | 1,804,907 |
| Facts extracted | 666 |
| New claims | 666 |
| Claims rejected by the gate | 0 |
| Derived / rechecked / drifted | 357 / 40 / 0 |
| Topics (new) | 109 (6) |
| Insights published | 357 |
| Forecasts issued / scored | 1036 / 620 |
| Ideas (promoted) | 14 (0) |
| Irregularities open (new) | 30 (1) |
| Pipeline errors | 0 |

No pipeline stage raised.

## Open critical irregularities

| Id | Title | First seen | Reproduce |
|---|---|---|---|
| `IRR-043` | clinicaltrials could not be read | cycle 4 | `curl -sS -o /dev/null -w '%{http_code}\n' 'https://clinicaltrials.gov/api/v2/studies?pageSize=1'` |
| `IRR-046` | sec_edgar could not be read | cycle 4 | `curl -sS -o /dev/null -w '%{http_code}\n' 'https://data.sec.gov/submissions/CIK0000320193.json'` |
| `IRR-049` | nba_cdn could not be read | cycle 4 | `curl -sS -o /dev/null -w '%{http_code}\n' 'https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json'` |

## Register totals

105 registered — 6 critical,
58 warn, 41 info;
30 open, 75 resolved,
15 standing.

## Recent cycles

| Cycle | At (UTC) | Claims | Topics | New | Forecasts | Scored | Ideas | Irr open | Result |
|---|---|---|---|---|---|---|---|---|---|
| 7 | 2026-09-22T01:51:33Z | 5,374 | 55 | 6 | 738 | 401 | 14 | 30 | ok |
| 8 | 2026-09-22T01:57:26Z | 6,352 | 61 | 6 | 760 | 416 | 14 | 32 | ok |
| 9 | 2026-09-22T03:49:52Z | 7,076 | 67 | 6 | 760 | 0 | 14 | 40 | ok |
| 10 | 2026-09-22T03:50:22Z | 7,847 | 73 | 6 | 950 | 832 | 14 | 61 | ok |
| 11 | 2026-09-22T03:58:55Z | 8,618 | 79 | 6 | 894 | 603 | 14 | 45 | ok |
| 12 | 2026-09-22T04:12:37Z | 9,343 | 85 | 6 | 894 | 0 | 14 | 40 | ok |
| 13 | 2026-09-22T04:15:17Z | 10,334 | 91 | 6 | 834 | 1216 | 14 | 31 | ok |
| 14 | 2026-09-22T04:30:49Z | 11,344 | 97 | 6 | 804 | 572 | 14 | 29 | ok |
| 15 | 2026-09-22T07:16:15Z | 12,365 | 103 | 6 | 974 | 496 | 14 | 29 | ok |
| 16 | 2026-09-22T12:45:18Z | 13,388 | 109 | 6 | 1036 | 620 | 14 | 30 | ok |

## What runs next

`.github/workflows/think.yml` fires on `*/30 * * * *` and needs no input.
`probe.yml` live-reads every registered source daily and publishes the health
ledger. `tests.yml` runs the suite on every push and pull request.
