# STATUS — cycle 3

Generated `2026-09-22T01:34:57Z` by `msl/docs.py`. Every figure here is read from the same
objects the site is built from.

## Last cycle

| | |
|---|---|
| Cycle | 3 |
| Mode | `offline-fixtures` |
| Duration | 122 ms |
| Reads (ok / failed) | 11 / 0 |
| Bytes read | 0 |
| Facts extracted | 389 |
| New claims | 389 |
| Claims rejected by the gate | 0 |
| Derived / rechecked / drifted | 125 / 1 / 0 |
| Topics (new) | 31 (6) |
| Insights published | 125 |
| Forecasts issued / scored | 355 / 357 |
| Ideas (promoted) | 4 (0) |
| Irregularities open (new) | 38 (1) |
| Pipeline errors | 0 |

No pipeline stage raised.

## Open critical irregularities

| Id | Title | First seen | Reproduce |
|---|---|---|---|
| — | *No critical irregularity is open.* | — | — |

## Register totals

42 registered — 0 critical,
5 warn, 37 info;
38 open, 4 resolved,
14 standing.

## Recent cycles

| Cycle | At (UTC) | Claims | Topics | New | Forecasts | Scored | Ideas | Irr open | Result |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 2026-09-22T01:34:57Z | 545 | 19 | 19 | 2 | 0 | 4 | 41 | ok |
| 2 | 2026-09-22T01:34:57Z | 1,059 | 25 | 6 | 357 | 2 | 4 | 41 | ok |
| 3 | 2026-09-22T01:34:57Z | 1,573 | 31 | 6 | 355 | 357 | 4 | 38 | ok |

## What runs next

`.github/workflows/think.yml` fires on `*/30 * * * *` and needs no input.
`probe.yml` live-reads every registered source daily and publishes the health
ledger. `tests.yml` runs the suite on every push and pull request.
