# 04: Route drill-down from Origin/Destination

**What to build:** From the Origin view, clicking a specific Origin drills into that Origin's Routes (Origin scoped, grouped by destination-as-route-endpoint); from the Destination view, clicking a specific Destination drills into the Origins that serve it, presented as Routes. In both cases the drill-down calls the metrics module with `groupBy: 'route'` scoped to the selected Origin or Destination, and Route is never offered as a flat, unscoped top-level list.

**Blocked by:** 02 (Destination view)

**Status:** ready-for-agent

- [ ] Clicking an Origin in the Origin view navigates to a Route-level view scoped to that Origin, ranked by Delay Rate descending, with the same three rates and counts as other views.
- [ ] Clicking a Destination in the Destination view navigates to a Route-level view scoped to that Destination, ranked by Delay Rate descending, with the same three rates and counts.
- [ ] There is no UI path that presents all Routes as a flat, unscoped top-level list.
- [ ] The user can navigate back out of a Route drill-down to the Origin or Destination view they came from.
