# STATUS — cycle 20

Generated `2026-09-22T19:23:59Z` by `msl/docs.py`. Every figure here is read from the same
objects the site is built from.

## Last cycle

| | |
|---|---|
| Cycle | 20 |
| Mode | `offline-fixtures` |
| Duration | 1,791 ms |
| Reads (ok / failed) | 22 / 0 |
| Bytes read | 0 |
| Facts extracted | 484 |
| New claims | 484 |
| Claims rejected by the gate this cycle | 0 |
| Gate rejections in append-only history | 0 |
| Derived / rechecked / drifted | 228 / 1,446 / 0 |
| Topics (new) | 133 (6) |
| Insights published | 271 |
| Forecasts issued / scored | 1091 / 496 |
| Ideas (promoted) | 25 (0) |
| Irregularities open (new) | 24 (0) |
| Pipeline errors | 0 |

No pipeline stage raised.

## Open critical irregularities

| Id | Title | First seen | Reproduce |
|---|---|---|---|
| — | *No critical irregularity is open.* | — | — |

## Register totals

119 registered — 6 critical,
69 warn, 44 info;
24 open, 95 resolved,
21 standing.

## Recent cycles

| Cycle | At (UTC) | Claims | Topics | New | Forecasts | Scored | Ideas | Irr open | Result |
|---|---|---|---|---|---|---|---|---|---|
| 11 | 2026-09-22T03:58:55Z | 8,618 | 79 | 6 | 894 | 603 | 14 | 45 | ok |
| 12 | 2026-09-22T04:12:37Z | 9,343 | 85 | 6 | 894 | 0 | 14 | 40 | ok |
| 13 | 2026-09-22T04:15:17Z | 10,334 | 91 | 6 | 834 | 1216 | 14 | 31 | ok |
| 14 | 2026-09-22T04:30:49Z | 11,344 | 97 | 6 | 804 | 572 | 14 | 29 | ok |
| 15 | 2026-09-22T07:16:15Z | 12,365 | 103 | 6 | 974 | 496 | 14 | 29 | ok |
| 16 | 2026-09-22T12:45:18Z | 13,388 | 109 | 6 | 1036 | 620 | 14 | 30 | ok |
| 17 | 2026-09-22T17:24:28Z | 14,042 | 115 | 6 | 1138 | 105 | 24 | 31 | ok |
| 18 | 2026-09-22T17:31:33Z | 15,107 | 121 | 6 | 1153 | 1215 | 24 | 32 | ok |
| 19 | 2026-09-22T19:08:58Z | 15,820 | 127 | 6 | 1143 | 2256 | 25 | 24 | ok |
| 20 | 2026-09-22T19:23:59Z | 16,532 | 133 | 6 | 1091 | 496 | 25 | 24 | ok |

## What runs next

`.github/workflows/think.yml` fires on `*/30 * * * *` and needs no input.
`probe.yml` live-reads every registered source daily and publishes the health
ledger. `tests.yml` runs the suite on every push and pull request.
