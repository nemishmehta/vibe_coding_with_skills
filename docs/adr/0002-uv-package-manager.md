# Use uv as the Python package manager

We're managing this project's dependencies, Python version, and script execution with [uv](https://docs.astral.sh/uv/) instead of plain pip + venv, Poetry, PDM, or conda. uv gives a single fast tool for dependency resolution, a committed lockfile, and Python version provisioning, with no extra runtime beyond the `uv` binary itself. Dev-only tooling (`pytest`) lives in `[dependency-groups]` (PEP 735) rather than `[project.optional-dependencies]`, since it's never meant to be installed as a package extra.

## Considered Options

- **pip + venv** — no lockfile by default (would need `pip-tools` bolted on), slower resolution, no built-in Python version management.
- **Poetry** — has a lockfile and Python version handling, but is slower than uv and Streamlit Community Cloud reads a bare `pyproject.toml` (no `uv.lock` present) as a Poetry project specifically — mixing the two would be ambiguous.
- **conda** — heavier tooling than this project's dependency set (pandas/streamlit/plotly) needs.

## Consequences

- `uv.lock` must be committed and kept in sync — Streamlit Community Cloud detects dependency files in priority order (`uv.lock` → Pipfile → environment.yml → requirements.txt → `pyproject.toml`-as-Poetry). Without a committed `uv.lock`, this project's `pyproject.toml` would be misread as a Poetry project at deploy time, not resolved via uv.
- Local dev and CI (if added later) should invoke everything through `uv run` (e.g. `uv run pytest`, `uv run streamlit run ...`) rather than assuming an activated venv.
- `requires-python` is `>=3.11`, with `.python-version` pinned to `3.12` to match Streamlit Community Cloud's own default Python version.
