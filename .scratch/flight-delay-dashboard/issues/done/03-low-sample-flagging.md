# 03: Low-sample visual flagging

**What to build:** In any grouped view, a group backed by a small flight count is visually flagged (e.g. muted styling or an explicit annotation) rather than displayed at the same visual weight as a high-volume group, so the user doesn't mistake a noisy, low-sample rate for a meaningful one. Implemented in the shared chart component so it applies automatically to the Route view once ticket 04 lands.

**Blocked by:** 02 (Destination view)

**Status:** ready-for-agent

- [x] The chart component used to render grouped rates applies a distinct, visibly different treatment (e.g. muted color/opacity, or an inline annotation) to groups whose backing flight count falls below a reasonable low-sample threshold.
- [x] The flagging is visible in the Destination view, where some destinations have far fewer flights than others.
- [x] The flagging does not hide or remove low-sample groups from the ranking — it only changes how they're visually presented.
- [x] The threshold and treatment are implemented once, in the shared chart component, not duplicated per view.

## Implementation notes (2026-08-27)

- `flight_dashboard/metrics.py`: added `LOW_SAMPLE_THRESHOLD = 100` (chosen from
  this dataset's destination flight-count distribution — flags 12 of 105
  destinations, the bottom ~11%) and a new `is_low_sample` boolean column on
  `compute_metrics()`'s result, computed as `scheduled_count < LOW_SAMPLE_THRESHOLD`.
  Covered by two new pytest cases against the public `compute_metrics` contract
  (below/at-threshold), per this repo's testing boundary (ADR 0001).
- `flight_dashboard/app.py`: the shared `render_rates_chart()` now sets per-bar
  `marker_opacity` (1.0 normal, 0.35 for low-sample groups) and appends
  " (low sample)" to the hover tooltip via `customdata`. Since Origin,
  Destination, and Route views all call this one function, the flagging
  applies everywhere automatically — no per-view duplication. Ranking/table
  output is untouched; only the chart's visual weight changes.
- Verified: full pytest suite green (21 passed); manually inspected the
  resulting Plotly figure against the real `flights.csv` data (opacity array
  and hover text correct for known low-sample destinations like EYW, ANC);
  confirmed the Streamlit app boots (HTTP 200) under headless `streamlit run`.
  No `chromium-cli`/Playwright was available in this environment to capture
  an actual browser screenshot — a human should do a quick visual pass on
  the Destination view to confirm the muted bars look right, and consider
  running `/run-skill-generator` to give this repo a proper run skill for
  future UI verification.
