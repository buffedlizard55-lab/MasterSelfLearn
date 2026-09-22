# STATUS — cycle 12

Generated `2026-09-22T04:12:37Z` by `msl/docs.py`. Every figure here is read from the same
objects the site is built from.

## Last cycle

| | |
|---|---|
| Cycle | 12 |
| Mode | `offline-fixtures` |
| Duration | 0 ms |
| Reads (ok / failed) | 18 / 0 |
| Bytes read | 0 |
| Facts extracted | 0 |
| New claims | 420 |
| Claims rejected by the gate | 0 |
| Derived / rechecked / drifted | 0 / 40 / 0 |
| Topics (new) | 85 (6) |
| Insights published | 305 |
| Forecasts issued / scored | 894 / 0 |
| Ideas (promoted) | 14 (0) |
| Irregularities open (new) | 40 (0) |
| Pipeline errors | 0 |

No pipeline stage raised.

## Open critical irregularities

| Id | Title | First seen | Reproduce |
|---|---|---|---|
| — | *No critical irregularity is open.* | — | — |

## Register totals

103 registered — 3 critical,
59 warn, 41 info;
40 open, 63 resolved,
15 standing.

## Recent cycles

| Cycle | At (UTC) | Claims | Topics | New | Forecasts | Scored | Ideas | Irr open | Result |
|---|---|---|---|---|---|---|---|---|---|
| 3 | 2026-09-22T01:34:57Z | 1,573 | 31 | 6 | 355 | 357 | 4 | 38 | ok |
| 4 | 2026-09-22T01:39:14Z | 2,502 | 37 | 6 | 463 | 82 | 14 | 29 | ok |
| 5 | 2026-09-22T01:41:22Z | 3,449 | 43 | 6 | 688 | 148 | 14 | 30 | ok |
| 6 | 2026-09-22T01:47:08Z | 4,405 | 49 | 6 | 723 | 371 | 14 | 30 | ok |
| 7 | 2026-09-22T01:51:33Z | 5,374 | 55 | 6 | 738 | 401 | 14 | 30 | ok |
| 8 | 2026-09-22T01:57:26Z | 6,352 | 61 | 6 | 760 | 416 | 14 | 32 | ok |
| 9 | 2026-09-22T03:49:52Z | 7,076 | 67 | 6 | 760 | 0 | 14 | 40 | ok |
| 10 | 2026-09-22T03:50:22Z | 7,847 | 73 | 6 | 950 | 832 | 14 | 61 | ok |
| 11 | 2026-09-22T03:58:55Z | 8,618 | 79 | 6 | 894 | 603 | 14 | 45 | ok |
| 12 | 2026-09-22T04:12:37Z | 9,343 | 85 | 6 | 894 | 0 | 14 | 40 | ok |

## What runs next

`.github/workflows/think.yml` fires on `*/30 * * * *` and needs no input.
`probe.yml` live-reads every registered source daily and publishes the health
ledger. `tests.yml` runs the suite on every push and pull request.
