# STATUS — cycle 28

Generated `2026-09-26T21:39:23Z` by `msl/docs.py`. Every figure here is read from the same
objects the site is built from.

## Last cycle

| | |
|---|---|
| Cycle | 28 |
| Mode | `offline-fixtures` |
| Duration | 4,682 ms |
| Reads (ok / failed) | 22 / 0 |
| Bytes read | 0 |
| Facts extracted | 484 |
| New claims | 484 |
| Claims rejected by the gate this cycle | 0 |
| Gate rejections in append-only history | 0 |
| Derived / rechecked / drifted | 401 / 2,843 / 0 |
| Topics (new) | 181 (6) |
| Insights published | 446 |
| Forecasts issued / scored | 1291 / 2624 |
| Ideas (promoted) | 28 (0) |
| Irregularities open (new) | 23 (0) |
| Pipeline errors | 0 |

No pipeline stage raised.

## Open critical irregularities

| Id | Title | First seen | Reproduce |
|---|---|---|---|
| — | *No critical irregularity is open.* | — | — |

## Register totals

123 registered — 6 critical,
72 warn, 45 info;
23 open, 100 resolved,
21 standing.

## Recent cycles

| Cycle | At (UTC) | Claims | Topics | New | Forecasts | Scored | Ideas | Irr open | Result |
|---|---|---|---|---|---|---|---|---|---|
| 19 | 2026-09-22T19:08:58Z | 15,820 | 127 | 6 | 1143 | 2256 | 25 | 24 | ok |
| 20 | 2026-09-22T19:23:59Z | 16,532 | 133 | 6 | 1091 | 496 | 25 | 24 | ok |
| 21 | 2026-09-22T20:34:15Z | 17,640 | 139 | 6 | 1137 | 1856 | 28 | 27 | ok |
| 22 | 2026-09-22T20:52:29Z | 18,737 | 145 | 6 | 1070 | 749 | 28 | 29 | ok |
| 23 | 2026-09-22T23:28:37Z | 19,851 | 151 | 6 | 1116 | 684 | 28 | 27 | ok |
| 24 | 2026-09-22T23:43:29Z | 20,947 | 157 | 6 | 1056 | 717 | 28 | 27 | ok |
| 25 | 2026-09-23T01:42:26Z | 22,070 | 163 | 6 | 1110 | 655 | 28 | 27 | ok |
| 26 | 2026-09-23T07:19:33Z | 23,220 | 169 | 6 | 1224 | 653 | 28 | 27 | ok |
| 27 | 2026-09-23T12:54:12Z | 24,393 | 175 | 6 | 1269 | 799 | 28 | 27 | ok |
| 28 | 2026-09-26T21:39:23Z | 25,278 | 181 | 6 | 1291 | 2624 | 28 | 23 | ok |

## What runs next

`.github/workflows/think.yml` fires on `*/30 * * * *` and needs no input.
`probe.yml` live-reads every registered source daily and publishes the health
ledger. `tests.yml` runs the suite on every push and pull request.
