# 06: Filter/drill-down state bar + reset

**What to build:** At all times, the dashboard clearly shows the user's current view (Origin, Destination, or a Route drill-down, including which Origin/Destination they drilled from) and any active time filters (month, day of week, hour), so the user always understands exactly what population of flights the displayed numbers represent. A single control resets the dashboard back to the default unfiltered Origin view.

**Blocked by:** 04 (Route drill-down from Origin/Destination), 05 (Time filters)

**Status:** ready-for-agent

- [ ] A persistent element (e.g. a breadcrumb/filter bar) displays the current view type (Origin/Destination/Route) and, when drilled down, which Origin or Destination the Route view is scoped to.
- [ ] The same element displays any active time filters (month, day of week, hour) in human-readable form.
- [ ] A single reset control clears all filters and drill-down state, returning to the default unfiltered Origin view sorted by Delay Rate descending.
- [ ] The state bar updates immediately as the user changes filters or drills down/back, with no stale or missing state.
