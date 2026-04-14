#!/usr/bin/env python3
"""
Generate contributions.csv — a schedule of fake commits to backfill the
GitHub contribution graph.

Date range  : 2025-09-10 → 2026-04-08 (inclusive)
Active days : all days in range that visually appear active in the graph
              (guessed from screenshot — edit INACTIVE to refine)
Bonus       : 10 randomly-selected inactive days added to the schedule
Ramp        : linear from ~1 to ~70 commits/day (by calendar position)
Jitter      : ±15 (result clamped to ≥1)
Seed        : 42 (fixed — keep reproducible)
"""

import csv
import random
from datetime import date, timedelta

SEED = 42
START = date(2025, 9, 10)
END = date(2026, 4, 8)
RAMP_MIN = 1
RAMP_MAX = 70
JITTER = 15
BONUS_DAYS = 10   # inactive days to randomly add to the schedule
OUTPUT = "contributions.csv"

# Days that visually appear inactive in the contribution graph.
# Estimated from the screenshot — adjust as needed.
INACTIVE = {
    date(2025, 9, 14),   # Sun
    date(2025, 9, 21),   # Sun
    date(2025, 9, 28),   # Sun
    date(2025, 10, 12),  # Sun
    date(2025, 10, 19),  # Sun
    date(2025, 11, 1),   # Sat
    date(2025, 11, 2),   # Sun
    date(2025, 11, 8),   # Sat
    date(2025, 11, 9),   # Sun
    date(2025, 11, 16),  # Sun
    date(2025, 11, 23),  # Sun
    date(2025, 11, 27),  # Thu — Thanksgiving
    date(2025, 12, 6),   # Sat
    date(2025, 12, 7),   # Sun
    date(2025, 12, 14),  # Sun
    date(2025, 12, 20),  # Sat
    date(2025, 12, 21),  # Sun
    date(2025, 12, 25),  # Christmas
    date(2025, 12, 26),  # Fri
    date(2025, 12, 27),  # Sat
    date(2025, 12, 28),  # Sun
    date(2026, 1, 1),    # New Year
    date(2026, 1, 4),    # Sun
    date(2026, 1, 11),   # Sun
    date(2026, 1, 17),   # Sat
    date(2026, 1, 18),   # Sun
    date(2026, 2, 1),    # Sun
    date(2026, 2, 8),    # Sun
    date(2026, 2, 14),   # Sat
    date(2026, 2, 15),   # Sun
    date(2026, 3, 8),    # Sun
    date(2026, 3, 14),   # Sat
    date(2026, 3, 15),   # Sun
    date(2026, 3, 22),   # Sun
    date(2026, 3, 29),   # Sun
    date(2026, 4, 5),    # Sun
}


def main():
    random.seed(SEED)

    all_days = []
    d = START
    while d <= END:
        all_days.append(d)
        d += timedelta(days=1)

    active = [d for d in all_days if d not in INACTIVE]
    inactive_pool = [d for d in all_days if d in INACTIVE]

    bonus = random.sample(inactive_pool, min(BONUS_DAYS, len(inactive_pool)))
    schedule = sorted(set(active) | set(bonus))

    total_span = (END - START).days  # calendar denominator for ramp

    rows = []
    for day in schedule:
        offset = (day - START).days
        base = RAMP_MIN + (RAMP_MAX - RAMP_MIN) * offset / total_span
        count = round(base) + random.randint(-JITTER, JITTER)
        count = max(1, count)
        rows.append((day.strftime("%Y-%m-%d"), count))

    with open(OUTPUT, "w", newline="") as f:
        writer = csv.writer(f, delimiter="|")
        writer.writerow(["day", "number_commits_to_add"])
        writer.writerows(rows)

    print(
        f"Written {len(rows)} rows to {OUTPUT}  "
        f"({len(active)} active + {len(bonus)} bonus days)"
    )


if __name__ == "__main__":
    main()
