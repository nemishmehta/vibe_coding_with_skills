"""The dashboard's single computation seam: flights DataFrame -> per-group rates.

See CONTEXT.md for the domain vocabulary (Delayed/Cancelled/Unknown Outcome
Flight, Delay Rate, Cancellation Rate) that this module implements.
"""

import numpy as np
import pandas as pd

GROUP_BY_DIMENSIONS = {"origin", "dest", "route"}

RESULT_COLUMNS = [
    "scheduled_count",
    "cancelled_count",
    "unknown_count",
    "rated_count",
    "delay_rate",
    "cancellation_rate",
    "unknown_outcome_rate",
]


def compute_metrics(flights: pd.DataFrame, group_by: str, filters: dict | None = None) -> pd.DataFrame:
    if group_by not in GROUP_BY_DIMENSIONS:
        raise ValueError(f"group_by must be one of {sorted(GROUP_BY_DIMENSIONS)}, got {group_by!r}")

    df = flights.copy()
    if group_by == "route":
        df["route"] = df["origin"] + "-" + df["dest"]

    df = _apply_filters(df, filters or {})

    if df.empty:
        return pd.DataFrame(columns=[group_by, *RESULT_COLUMNS])

    cancelled = df["dep_time"].isna()
    unknown = ~cancelled & df["arr_delay"].isna()
    rated = ~cancelled & ~unknown
    delayed = rated & (df["arr_delay"] >= 15)

    df = df.assign(_cancelled=cancelled, _unknown=unknown, _rated=rated, _delayed=delayed)

    result = df.groupby(group_by).agg(
        scheduled_count=(group_by, "size"),
        cancelled_count=("_cancelled", "sum"),
        unknown_count=("_unknown", "sum"),
        rated_count=("_rated", "sum"),
        _delayed_count=("_delayed", "sum"),
    ).reset_index()

    result["delay_rate"] = np.where(
        result["rated_count"] > 0, result["_delayed_count"] / result["rated_count"], 0.0
    )
    result["cancellation_rate"] = result["cancelled_count"] / result["scheduled_count"]
    result["unknown_outcome_rate"] = result["unknown_count"] / result["scheduled_count"]

    result = result.drop(columns=["_delayed_count"])
    return result.sort_values("delay_rate", ascending=False).reset_index(drop=True)


def _apply_filters(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    if "month" in filters:
        df = df[df["month"] == filters["month"]]
    if "hour" in filters:
        df = df[df["hour"] == filters["hour"]]
    if "day_of_week" in filters:
        day_of_week = pd.to_datetime(df[["year", "month", "day"]]).dt.weekday
        df = df[day_of_week == filters["day_of_week"]]
    if "origin" in filters:
        df = df[df["origin"] == filters["origin"]]
    if "dest" in filters:
        df = df[df["dest"] == filters["dest"]]
    return df
