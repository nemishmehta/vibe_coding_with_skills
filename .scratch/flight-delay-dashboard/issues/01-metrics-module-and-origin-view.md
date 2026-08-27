# 01: Metrics module + default Origin view

**What to build:** Opening the dashboard shows the three NYC Origin airports (EWR, JFK, LGA) ranked from highest to lowest Delay Rate, each with its Delay Rate, Cancellation Rate, and Unknown Outcome Rate visually distinguished from one another, plus the flight count backing each rate. This is powered by a fully implemented, pure metrics module — the dashboard's single computation seam — built to its complete contract now even though only the Origin view is wired up to the UI in this ticket.

The metrics module takes the parsed flight records, a `groupBy` dimension (`origin`, `dest`, or `route`), and an optional set of filters (`month`, `dayOfWeek`, `hour`, and optionally a fixed `origin`/`dest` to scope a drill-down), and returns one row per group with its Delay Rate, Cancellation Rate, Unknown Outcome Rate, and backing flight counts. Classification: a flight with no recorded departure time is Cancelled; otherwise a flight with no recorded arrival delay is Unknown Outcome; otherwise a flight is Delayed if `arr_delay >= 15`. Delay Rate's denominator excludes Cancelled and Unknown Outcome flights; Cancellation Rate's denominator is all scheduled flights in the filtered population.

**Blocked by:** None (can start immediately)

**Status:** ready-for-agent

- [ ] `flights.csv` is bundled as a static asset and parsed once into an in-memory array of flight records on app load, with no backend/server involved.
- [ ] The metrics module correctly classifies a normal on-time flight, a normal delayed flight, a flight at exactly 14 minutes late (not Delayed), a flight at exactly 15 minutes late (Delayed), a Cancelled flight (no departure time), and an Unknown Outcome flight (departed, no arrival delay).
- [ ] The metrics module correctly groups by `origin`, `dest`, and `route`, correctly applies `month`/`dayOfWeek`/`hour` filters (individually and combined), and does not divide by zero or throw when a filtered group's population is empty.
- [ ] The metrics module has an automated unit test suite covering the above, testing only its public input/output contract (no reaching into internal classification helpers).
- [ ] The dashboard's default screen (no filters, no drill-down) renders the Origin view: EWR/JFK/LGA sorted by Delay Rate descending.
- [ ] Each Origin's Delay Rate, Cancellation Rate, and Unknown Outcome Rate are visually distinguished (e.g. separate series/colors) rather than blended into one number.
- [ ] Each Origin's backing flight count is visible (e.g. as a label or tooltip) alongside its rates.
- [ ] The dashboard loads and is fully usable with no login, account, or server round-trip.
