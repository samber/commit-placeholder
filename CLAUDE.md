# CLAUDE.md

This repo generates a commit schedule for backfilling the GitHub contribution graph with fake commits.

## Invariants — never break these

- `contributions.csv` is pipe-delimited (`|`) with a header row `day|number_commits_to_add`.
- `day` column is `YYYY-MM-DD`, sorted **ascending**.
- `number_commits_to_add` is always **≥ 1**.
- Date range: **2025-09-10 → 2026-04-08** (inclusive).

## Generation parameters (in `generate.py`)

- Linear ramp from **1 → 70** commits/day over the date range.
- Jitter: **±15** (random, seed=42).
- **10 days skipped** (simulated inactivity gaps); first and last dates are never skipped.
- Seed **42** — do not change unless regenerating from scratch for a new date range.

## Do not regenerate blindly

Once the downstream tool has used `contributions.csv` to create backdated commits, changing the seed or parameters will produce a different schedule, invalidating already-committed dates.

## Modifying the schedule

- To extend the date range: update `END` and re-run (existing rows are reproduced identically thanks to the fixed seed).
- To add/remove a specific day: edit `contributions.csv` directly rather than regenerating.
