# 02: Destination view

**What to build:** The user can switch the dashboard from the Origin view to a Destination view, seeing all destinations ranked from highest to lowest Delay Rate, each with the same three rates (Delay Rate, Cancellation Rate, Unknown Outcome Rate) visually distinguished, plus backing flight counts — reusing the metrics module built in ticket 01 with `groupBy: 'dest'`.

**Blocked by:** 01 (Metrics module + default Origin view)

**Status:** ready-for-agent

- [ ] A control lets the user switch between the Origin view and the Destination view.
- [ ] The Destination view lists all destinations present in the dataset, sorted by Delay Rate descending by default.
- [ ] Each destination's Delay Rate, Cancellation Rate, and Unknown Outcome Rate are visually distinguished, matching the visual treatment used in the Origin view.
- [ ] Each destination's backing flight count is visible alongside its rates.
- [ ] Switching between Origin and Destination views does not require a page reload.
