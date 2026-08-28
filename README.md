# Flight Delay Dashboard

See [`project.md`](project.md) for what this is and [`CONTEXT.md`](CONTEXT.md) for the domain vocabulary.

## Data

Download the dataset and place it in the project root as flights.csv:

https://www.kaggle.com/datasets/mahoora00135/flights

The app expects the following columns to be present: `month`, `day`, `dep_delay`, `arr_delay`, `carrier`, `origin`, `dest`, `hour`, `time_hour`, `name`.

## Setup

This project is managed with [uv](https://docs.astral.sh/uv/). Install uv, then:

```sh
uv sync
```

This provisions the pinned Python version (`.python-version`), creates `.venv`, and installs dependencies from `uv.lock`.

## Running

```sh
uv run pytest
uv run streamlit run flight_dashboard/app.py
```

`uv run` picks up the project's venv automatically — no manual activation needed.

## Dependencies

- Runtime dependencies: `[project.dependencies]` in `pyproject.toml`.
- Dev-only dependencies (e.g. `pytest`): `[dependency-groups] dev` in `pyproject.toml`, included by default in `uv sync`.
- `uv.lock` pins exact resolved versions and is committed to the repo — it's also what Streamlit Community Cloud reads to reproduce this environment at deploy time.

To add or update a dependency: `uv add <package>` (or `uv add --group dev <package>` for dev-only tools), then commit the updated `pyproject.toml` and `uv.lock`.
