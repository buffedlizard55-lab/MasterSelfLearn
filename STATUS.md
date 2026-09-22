# STATUS — cycle 4

Generated `2026-09-22T01:39:14Z` by `msl/docs.py`. Every figure here is read from the same
objects the site is built from.

## Last cycle

| | |
|---|---|
| Cycle | 4 |
| Mode | `github-actions` |
| Duration | 63829 ms |
| Reads (ok / failed) | 65 / 5 |
| Bytes read | 1,796,602 |
| Facts extracted | 677 |
| New claims | 677 |
| Claims rejected by the gate | 0 |
| Derived / rechecked / drifted | 252 / 29 / 0 |
| Topics (new) | 37 (6) |
| Insights published | 252 |
| Forecasts issued / scored | 463 / 82 |
| Ideas (promoted) | 14 (0) |
| Irregularities open (new) | 29 (12) |
| Pipeline errors | 0 |

No pipeline stage raised.

## Open critical irregularities

| Id | Title | First seen | Reproduce |
|---|---|---|---|
| — | *No critical irregularity is open.* | — | — |

## Register totals

54 registered — 0 critical,
17 warn, 37 info;
29 open, 25 resolved,
14 standing.

## Recent cycles

| Cycle | At (UTC) | Claims | Topics | New | Forecasts | Scored | Ideas | Irr open | Result |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 2026-09-22T01:34:57Z | 545 | 19 | 19 | 2 | 0 | 4 | 41 | ok |
| 2 | 2026-09-22T01:34:57Z | 1,059 | 25 | 6 | 357 | 2 | 4 | 41 | ok |
| 3 | 2026-09-22T01:34:57Z | 1,573 | 31 | 6 | 355 | 357 | 4 | 38 | ok |
| 4 | 2026-09-22T01:39:14Z | 2,502 | 37 | 6 | 463 | 82 | 14 | 29 | ok |

## What runs next

`.github/workflows/think.yml` fires on `*/30 * * * *` and needs no input.
`probe.yml` live-reads every registered source daily and publishes the health
ledger. `tests.yml` runs the suite on every push and pull request.
