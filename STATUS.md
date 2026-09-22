# STATUS — cycle 1

Generated `2026-09-21T12:00:00Z` by `msl/docs.py`. Every figure here is read from the same
objects the site is built from.

## Last cycle

| | |
|---|---|
| Cycle | 1 |
| Mode | `offline-fixtures` |
| Duration | 3 ms |
| Reads (ok / failed) | 0 / 0 |
| Bytes read | 0 |
| Facts extracted | 0 |
| New claims | 0 |
| Claims rejected by the gate | 0 |
| Derived / rechecked / drifted | 0 / 0 / 0 |
| Topics (new) | 13 (13) |
| Insights published | 0 |
| Forecasts issued / scored | 0 / 0 |
| Ideas (promoted) | 0 (0) |
| Irregularities open (new) | 42 (42) |
| Pipeline errors | 0 |

No pipeline stage raised.

## Open critical irregularities

| Id | Title | First seen | Reproduce |
|---|---|---|---|
| `IRR-033` | No successful read this cycle | cycle 1 | `python3 tools/probe_sources.py` |

## Register totals

42 registered — 1 critical,
5 warn, 36 info;
42 open, 0 resolved,
13 standing.

## Recent cycles

| Cycle | At (UTC) | Claims | Topics | New | Forecasts | Scored | Ideas | Irr open | Result |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 2026-09-21T12:00:00Z | 0 | 13 | 13 | 0 | 0 | 0 | 42 | ok |

## What runs next

`.github/workflows/think.yml` fires on `*/30 * * * *` and needs no input.
`probe.yml` live-reads every registered source daily and publishes the health
ledger. `tests.yml` runs the suite on every push and pull request.
