Status: ready-for-agent

# Flight Delay Dashboard

## Problem Statement

A Traveler deciding when and from where to fly out of the NYC area (EWR, JFK, or LGA) has no easy way to see which airports, destinations, routes, or times of year/day carry the highest risk of arriving late. The raw data (`flights.csv`, ~337k 2013 NYC-departure flights) exists, but it's a flat CSV — not something a Traveler can visually explore to answer "when and where am I most likely to get delayed?"

## Solution

Build an interactive dashboard that lets a Traveler explore Delay Rate, Cancellation Rate, and Unknown Outcome Rate across Origin, Destination, and Route, filtered and grouped by time (month, day of week, hour of scheduled departure). The dashboard ranks and visualizes these rates so the Traveler can immediately spot the riskiest airports, destinations, routes, and times — and drill from a broad view (Origin or Destination) down to the Route level for more specific answers.

## User Stories

1. As a Traveler, I want to see the Delay Rate for each of the three NYC Origin airports (EWR, JFK, LGA), so that I can pick the airport least likely to make me late.
2. As a Traveler, I want to see the Cancellation Rate for each Origin airport, so that I can factor cancellation risk into my airport choice separately from delay risk.
3. As a Traveler, I want to see the Unknown Outcome rate for each Origin airport, so that the dashboard's numbers visibly account for every flight, not just the ones with a clean outcome.
4. As a Traveler, I want to see Delay Rate ranked across Destinations, so that I can spot which destinations are riskiest regardless of which NYC airport I fly from.
5. As a Traveler, I want to see Cancellation Rate ranked across Destinations, so that I can see which destinations are prone to cancellations.
6. As a Traveler, I want to drill down from an Origin into that Origin's Destinations, so that I can see delay risk for "flights out of JFK" specifically rather than all NYC flights.
7. As a Traveler, I want to drill down from a Destination into the Origins that serve it, so that I can see whether my choice of NYC airport changes my risk for a specific destination.
8. As a Traveler, I want to view a specific Route (an Origin–Destination pair) as the most granular drill-down, so that I can get the most specific answer once I've narrowed down my airport and destination.
9. As a Traveler, I want Routes to only be reachable via drill-down from an Origin or Destination view, not offered as a flat top-level list, so that I'm not overwhelmed by hundreds of routes before narrowing my search.
10. As a Traveler, I want to filter the dashboard by month, so that I can see how delay and cancellation risk change with season (e.g., is summer or winter worse?).
11. As a Traveler, I want to filter the dashboard by day of week, so that I can see whether flying on a weekday vs. weekend changes my risk.
12. As a Traveler, I want to filter the dashboard by hour of scheduled departure, so that I can see whether early-morning or late-evening flights are more or less likely to be delayed.
13. As a Traveler, I want to combine time filters (e.g., a specific month AND a specific hour range) with an Origin/Destination/Route view, so that I can answer a specific question like "how risky is a Friday evening flight out of LGA in December?"
14. As a Traveler, I want groups (Origins, Destinations, or Routes) ranked from highest to lowest Delay Rate by default, so that the riskiest options are immediately visible without me having to sort manually.
15. As a Traveler, I want to see the underlying flight count behind each rate, so that I can judge whether a rate is based on enough flights to be meaningful (e.g., a Route with only 3 flights shouldn't be trusted the same as one with 3,000).
16. As a Traveler, I want Delay Rate, Cancellation Rate, and Unknown Outcome Rate to be visually distinguished from one another, so that I don't mistake a cancellation-prone route for a delay-prone one.
17. As a Traveler, I want the dashboard to load and be usable without any account, login, or install step, so that I can just open a link and start exploring.
18. As a Traveler, I want the current filters and view (Origin/Destination/Route, time filters) to be clear at all times, so that I understand exactly what population of flights the numbers on screen represent.
19. As a Traveler, I want to reset all filters back to the unfiltered, top-level Origin view, so that I can start a new exploration without reloading the page.
20. As a Traveler, I want the dashboard to clearly communicate when a filtered slice has zero or very few flights, so that I don't misread a missing bar or a noisy rate as meaningful signal.

## Implementation Decisions

- **Stack**: a single Python codebase — a [Streamlit](https://streamlit.io) app for the UI, [pandas](https://pandas.pydata.org) for data handling, and [Plotly](https://plotly.com/python/) for charting. Hosted (e.g. Streamlit Community Cloud) so the Traveler reaches it as a link, with no local install. See [ADR-0001](../../docs/adr/0001-streamlit-python-stack.md) for why this replaced the original client-side React + Vite plan.
- **Data loading**: `flights.csv` is read once into a pandas DataFrame via `st.cache_data` (using the CSV columns: `year`, `month`, `day`, `dep_time`, `sched_dep_time`, `dep_delay`, `arr_time`, `sched_arr_time`, `arr_delay`, `carrier`, `flight`, `tailnum`, `origin`, `dest`, `air_time`, `distance`, `hour`, `minute`, `time_hour`, `name`). This cached DataFrame is the input to the metrics module. No external pre-aggregation.
- **The one seam — a pure metrics module**: a single pure function/module is the sole computation boundary between raw flight data and the UI. Its contract:
  - Input: the flight DataFrame, a `groupBy` dimension (`origin`, `dest`, or `route`), and an optional set of filters (`month`, `dayOfWeek`, `hour`, and optionally a fixed `origin`/`dest` to scope a drill-down).
  - Output: one row per group value, each containing: the group key, Delay Rate, Cancellation Rate, Unknown Outcome Rate, and the flight count backing each rate (departed-and-recorded count for Delay Rate's denominator, scheduled count for Cancellation Rate's denominator).
  - Classification rules encoded here, per the domain glossary: a flight is **Cancelled** if it has no recorded departure time; otherwise it's **Unknown Outcome** if it has no recorded arrival delay; otherwise it's **Delayed** if `arr_delay >= 15`. Delay Rate excludes Cancelled and Unknown Outcome flights from its denominator; Cancellation Rate's denominator is all scheduled flights in the filtered population.
  - The UI layer (filter controls, ranked bar charts, drill-down navigation) calls this module and renders its output — it contains no delay/cancellation/unknown classification logic of its own.
- **Route as drill-down, not a top-level view**: the UI only exposes `groupBy: 'route'` when the user has already selected a specific Origin or Destination to drill into, matching the domain glossary's definition of Route as a granularity beneath Origin/Destination.
- **Time dimensions**: Month and Hour of scheduled departure come directly from the `month` and `hour` columns. Day of week is derived from `year`/`month`/`day`. These three are available as independent, combinable filters on any view (Origin, Destination, or Route).
- **Default view and sort**: the dashboard opens on the unfiltered Origin view (EWR/JFK/LGA), sorted by Delay Rate descending. Every grouped view (Origin, Destination, Route) is sorted by Delay Rate descending by default.
- **Visualization**: ranked bar charts per group built with Plotly (`st.plotly_chart`), with Delay Rate, Cancellation Rate, and Unknown Outcome Rate visually distinguished by color, and the backing flight count shown via hover tooltip on each bar.
- **Low-sample handling**: groups with a small flight count are visually flagged (e.g., muted trace styling or an explicit annotation) rather than silently presented at equal visual weight to high-volume groups.
- **Filter state**: current Origin/Destination/Route selection and active time filters are always visible in the UI (e.g., a filter bar/breadcrumb driven by `st.session_state`), with a single control to reset back to the default unfiltered Origin view.

## Testing Decisions

- A good test here exercises the metrics module's public contract only — given an input flight DataFrame, a `groupBy`, and filters, assert on the returned rates/counts. No test should reach into how the module internally classifies a flight or structures intermediate data.
- The metrics module is the only module with a dedicated automated test suite (pytest), per the single-seam decision above. Streamlit UI/interaction is validated by manual/visual checks, not unit tests.
- Fixture coverage for the metrics module should include: a normal on-time flight, a normal delayed flight, a boundary flight at exactly 14 minutes late (not Delayed), a boundary flight at exactly 15 minutes late (Delayed), a Cancelled flight (no departure time), an Unknown Outcome flight (departed, no arrival delay), correct grouping across multiple Origins/Destinations/Routes, correct behavior when time filters are applied, and a group whose filtered population is empty (should not divide by zero or throw).
- This is a greenfield module with no prior test suite in the repo to follow as precedent; the test suite for this module establishes the pattern for any future computation modules in this codebase.

## Out of Scope

- Any separate backend API or database beyond the Streamlit app itself — no additional service sits between the UI and the metrics module.
- User accounts, saved views, or personalization.
- Carrier-level (airline) breakdown or analysis — not part of the "when and where" question this dashboard answers, even though `carrier` is present in the data.
- Cause-of-delay analysis (e.g., weather) — not present in `flights.csv`.
- Any data beyond the bundled 2013 NYC-departure dataset (no live/real-time data, no other years or airports).
- Booking, trip planning, or recommendation features beyond visualizing historical rates.
- Formal responsive/mobile design requirements beyond basic usability.

## Further Notes

- All dashboard numbers reflect the fixed 2013 NYC-departure dataset and won't generalize to current flight schedules or delay patterns — this is a historical exploration tool, not a live risk predictor.
- Unknown Outcome Flights are a small slice of the data (~0.35%) — the dashboard should show this rate for completeness (per the domain glossary) without giving it visual weight disproportionate to its size.
- "Month," "day of week," and "hour of scheduled departure" are used here as plain, schema-derived terms rather than formally defined domain glossary terms — if these become more central to future dashboard work, they're a candidate for a `/domain-modeling` pass to formalize into `CONTEXT.md`.
