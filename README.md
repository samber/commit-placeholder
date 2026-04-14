# commit-placeholders

Source of truth for backfilling fake commits into the GitHub contribution graph.

## What this repo does

`contributions.csv` holds a schedule of (date, commit-count) pairs. A separate tool reads the CSV and creates empty commits backdated to each date, filling in the target contribution graph.

## CSV schema

File: `contributions.csv` — pipe-delimited, header row included.

| Column | Format | Description |
|---|---|---|
| `day` | `YYYY-MM-DD` | Target date, sorted ascending |
| `number_commits_to_add` | integer ≥ 1 | How many commits to create on that date |

Example:

```
day|number_commits_to_add
2025-09-10|7
2025-09-11|3
2025-09-13|12
```

## Regenerating the CSV

```bash
python3 generate.py
```

Parameters (edit the constants at the top of `generate.py`):

| Param | Value | Meaning |
|---|---|---|
| `START` | 2025-09-10 | First day |
| `END` | 2026-04-08 | Last day |
| `RAMP_MIN` | 1 | Commits on the first day |
| `RAMP_MAX` | 70 | Commits on the last day |
| `JITTER` | 15 | Random ±offset applied to each count |
| `SKIP_COUNT` | 10 | Days omitted to simulate gaps |
| `SEED` | 42 | Fixed seed — guarantees reproducibility |

> **Warning**: once the downstream commit-writing tool has run, do not regenerate with a different seed. Changing the seed shifts which days are skipped and what counts are used, making the schedule inconsistent with already-created commits.
