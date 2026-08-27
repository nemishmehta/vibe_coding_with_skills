# Switch to a Streamlit + pandas stack

The dashboard was originally planned as a client-side-only React + Vite SPA specifically so it could run with no backend and no server round-trip — the Traveler just opens a static page. We're replacing that with a single Python codebase: a hosted Streamlit app with pandas for the metrics module and Plotly for charting. This trades away the "fully static, no server" property in exchange for a much simpler, single-language stack for a data-heavy dashboard like this one.

## Considered Options

- **Pyodide/WASM** — would have preserved the no-server property by running Python in-browser, but adds significant startup latency and bundle weight for little benefit here.
- **Python backend + keep the React frontend** — smallest diff from the original plan, but leaves two runtimes/languages instead of consolidating on one, and still introduces a backend/API where none existed before.
- **Flask/FastAPI + server-rendered templates** — a more traditional web-app shape, but more code to hand-build (routing, templates, chart embedding) than Streamlit gives for free.

## Consequences

- The "no backend/API," "no server round-trip," and the server-round-trip clause of user story #17 in `spec.md` are retired — the app now requires a running, hosted Streamlit process. "No account/login, just open a link" is preserved by hosting it (e.g. Streamlit Community Cloud) rather than requiring a local run.
- The metrics module's contract (records/DataFrame + `groupBy` + filters → per-group rates and counts) carries over unchanged in shape; only the underlying data structure moves from plain records to a pandas DataFrame.
- The pure-function-only testing boundary is unchanged: pytest still targets only the metrics module, now with pandas-based fixtures; Streamlit UI stays manual/visual-check, same rationale as before.
