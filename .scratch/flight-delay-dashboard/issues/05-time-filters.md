# 05: Time filters (month, day of week, hour)

**What to build:** The user can filter the currently displayed view by month, day of week, and/or hour of scheduled departure — independently or combined — and the displayed rates recompute live using the metrics module's existing filter support from ticket 01.

**Blocked by:** 01 (Metrics module + default Origin view)

**Status:** ready-for-agent

- [ ] Filter controls exist for month, day of week, and hour of scheduled departure.
- [ ] Applying any single time filter recomputes and re-renders the current view's rates and counts using only the matching subset of flights.
- [ ] Combining multiple time filters (e.g. a specific month AND a specific hour) further narrows the population and recomputes correctly.
- [ ] Day of week is derived correctly from the flight's date.
- [ ] Filters apply correctly on the Origin view (Destination and Route views inherit the same filtering once they exist, via the shared metrics module call).
