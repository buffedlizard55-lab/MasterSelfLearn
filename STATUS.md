# STATUS — cycle 6

Generated `2026-09-22T01:47:08Z` by `msl/docs.py`. Every figure here is read from the same
objects the site is built from.

## Last cycle

| | |
|---|---|
| Cycle | 6 |
| Mode | `github-actions` |
| Duration | 62358 ms |
| Reads (ok / failed) | 64 / 6 |
| Bytes read | 1,790,314 |
| Facts extracted | 671 |
| New claims | 671 |
| Claims rejected by the gate | 0 |
| Derived / rechecked / drifted | 285 / 40 / 0 |
| Topics (new) | 49 (6) |
| Insights published | 285 |
| Forecasts issued / scored | 723 / 371 |
| Ideas (promoted) | 14 (0) |
| Irregularities open (new) | 30 (3) |
| Pipeline errors | 0 |

No pipeline stage raised.

## Open critical irregularities

| Id | Title | First seen | Reproduce |
|---|---|---|---|
| — | *No critical irregularity is open.* | — | — |

## Register totals

59 registered — 0 critical,
22 warn, 37 info;
30 open, 29 resolved,
14 standing.

## Recent cycles

| Cycle | At (UTC) | Claims | Topics | New | Forecasts | Scored | Ideas | Irr open | Result |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 2026-09-22T01:34:57Z | 545 | 19 | 19 | 2 | 0 | 4 | 41 | ok |
| 2 | 2026-09-22T01:34:57Z | 1,059 | 25 | 6 | 357 | 2 | 4 | 41 | ok |
| 3 | 2026-09-22T01:34:57Z | 1,573 | 31 | 6 | 355 | 357 | 4 | 38 | ok |
| 4 | 2026-09-22T01:39:14Z | 2,502 | 37 | 6 | 463 | 82 | 14 | 29 | ok |
| 5 | 2026-09-22T01:41:22Z | 3,449 | 43 | 6 | 688 | 148 | 14 | 30 | ok |
| 6 | 2026-09-22T01:47:08Z | 4,405 | 49 | 6 | 723 | 371 | 14 | 30 | ok |

## What runs next

`.github/workflows/think.yml` fires on `*/30 * * * *` and needs no input.
`probe.yml` live-reads every registered source daily and publishes the health
ledger. `tests.yml` runs the suite on every push and pull request.
