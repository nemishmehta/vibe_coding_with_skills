"""Tests for the metrics module's public contract: compute_metrics(flights, group_by, filters).

Only compute_metrics is exercised here -- no test reaches into internal
classification helpers, per the testing decisions in spec.md.
"""

import numpy as np
import pandas as pd
import pytest

from flight_dashboard.metrics import compute_metrics


def make_flights(rows):
    """Build a flights DataFrame from partial row dicts, filled with defaults."""
    defaults = dict(
        year=2013, month=1, day=1, hour=7,
        dep_time=800.0, arr_delay=0.0,
        origin="JFK", dest="LAX",
    )
    return pd.DataFrame([{**defaults, **row} for row in rows])


def test_on_time_flight_is_not_delayed():
    flights = make_flights([{"arr_delay": 5.0}])
    result = compute_metrics(flights, group_by="origin")
    assert result.loc[0, "delay_rate"] == 0.0
    assert result.loc[0, "rated_count"] == 1


def test_delayed_flight_is_delayed():
    flights = make_flights([{"arr_delay": 20.0}])
    result = compute_metrics(flights, group_by="origin")
    assert result.loc[0, "delay_rate"] == 1.0


def test_boundary_14_minutes_is_not_delayed():
    flights = make_flights([{"arr_delay": 14.0}])
    result = compute_metrics(flights, group_by="origin")
    assert result.loc[0, "delay_rate"] == 0.0


def test_boundary_15_minutes_is_delayed():
    flights = make_flights([{"arr_delay": 15.0}])
    result = compute_metrics(flights, group_by="origin")
    assert result.loc[0, "delay_rate"] == 1.0


def test_cancelled_flight_excluded_from_delay_rate_denominator():
    flights = make_flights([
        {"dep_time": np.nan, "arr_delay": np.nan},  # cancelled
        {"arr_delay": 20.0},  # delayed
    ])
    result = compute_metrics(flights, group_by="origin")
    row = result.iloc[0]
    assert row["cancelled_count"] == 1
    assert row["rated_count"] == 1  # cancelled flight excluded from Delay Rate's denominator
    assert row["delay_rate"] == 1.0  # the one rated flight was delayed
    assert row["cancellation_rate"] == 0.5  # denominator is all scheduled flights
    assert row["scheduled_count"] == 2


def test_unknown_outcome_flight_excluded_from_delay_and_counted_separately():
    flights = make_flights([
        {"dep_time": 800.0, "arr_delay": np.nan},  # departed, no arrival delay
        {"arr_delay": 0.0},  # on time
    ])
    result = compute_metrics(flights, group_by="origin")
    row = result.iloc[0]
    assert row["unknown_count"] == 1
    assert row["rated_count"] == 1
    assert row["delay_rate"] == 0.0
    assert row["cancellation_rate"] == 0.0
    assert row["unknown_outcome_rate"] == 0.5


def test_groups_by_origin():
    flights = make_flights([
        {"origin": "JFK", "arr_delay": 20.0},
        {"origin": "JFK", "arr_delay": 0.0},
        {"origin": "EWR", "arr_delay": 20.0},
    ])
    result = compute_metrics(flights, group_by="origin").set_index("origin")
    assert result.loc["JFK", "delay_rate"] == 0.5
    assert result.loc["EWR", "delay_rate"] == 1.0


def test_groups_by_dest():
    flights = make_flights([
        {"dest": "LAX", "arr_delay": 20.0},
        {"dest": "SFO", "arr_delay": 0.0},
    ])
    result = compute_metrics(flights, group_by="dest").set_index("dest")
    assert result.loc["LAX", "delay_rate"] == 1.0
    assert result.loc["SFO", "delay_rate"] == 0.0


def test_groups_by_route():
    flights = make_flights([
        {"origin": "JFK", "dest": "LAX", "arr_delay": 20.0},
        {"origin": "EWR", "dest": "LAX", "arr_delay": 0.0},
    ])
    result = compute_metrics(flights, group_by="route").set_index("route")
    assert result.loc["JFK-LAX", "delay_rate"] == 1.0
    assert result.loc["EWR-LAX", "delay_rate"] == 0.0


def test_sorted_by_delay_rate_descending():
    flights = make_flights([
        {"origin": "JFK", "arr_delay": 0.0},
        {"origin": "EWR", "arr_delay": 20.0},
    ])
    result = compute_metrics(flights, group_by="origin")
    assert list(result["origin"]) == ["EWR", "JFK"]


def test_month_filter():
    flights = make_flights([
        {"month": 1, "arr_delay": 20.0},
        {"month": 6, "arr_delay": 0.0},
    ])
    result = compute_metrics(flights, group_by="origin", filters={"month": 1})
    assert result.loc[0, "scheduled_count"] == 1
    assert result.loc[0, "delay_rate"] == 1.0


def test_hour_filter():
    flights = make_flights([
        {"hour": 8, "arr_delay": 20.0},
        {"hour": 17, "arr_delay": 0.0},
    ])
    result = compute_metrics(flights, group_by="origin", filters={"hour": 8})
    assert result.loc[0, "scheduled_count"] == 1
    assert result.loc[0, "delay_rate"] == 1.0


def test_day_of_week_filter():
    # 2013-01-01 is a Tuesday (weekday()==1); 2013-01-05 is a Saturday (weekday()==5)
    flights = make_flights([
        {"year": 2013, "month": 1, "day": 1, "arr_delay": 20.0},
        {"year": 2013, "month": 1, "day": 5, "arr_delay": 0.0},
    ])
    result = compute_metrics(flights, group_by="origin", filters={"day_of_week": 1})
    assert result.loc[0, "scheduled_count"] == 1
    assert result.loc[0, "delay_rate"] == 1.0


def test_combined_month_and_hour_filters():
    flights = make_flights([
        {"month": 1, "hour": 8, "arr_delay": 20.0},   # matches both filters
        {"month": 1, "hour": 17, "arr_delay": 0.0},   # wrong hour
        {"month": 6, "hour": 8, "arr_delay": 0.0},    # wrong month
    ])
    result = compute_metrics(flights, group_by="origin", filters={"month": 1, "hour": 8})
    assert result.loc[0, "scheduled_count"] == 1
    assert result.loc[0, "delay_rate"] == 1.0


def test_drilldown_scopes_route_view_to_one_origin():
    flights = make_flights([
        {"origin": "JFK", "dest": "LAX", "arr_delay": 20.0},
        {"origin": "EWR", "dest": "LAX", "arr_delay": 0.0},
    ])
    result = compute_metrics(flights, group_by="route", filters={"origin": "JFK"})
    assert list(result["route"]) == ["JFK-LAX"]


def test_drilldown_scopes_route_view_to_one_dest():
    flights = make_flights([
        {"origin": "JFK", "dest": "LAX", "arr_delay": 20.0},
        {"origin": "JFK", "dest": "SFO", "arr_delay": 0.0},
    ])
    result = compute_metrics(flights, group_by="route", filters={"dest": "LAX"})
    assert list(result["route"]) == ["JFK-LAX"]


def test_empty_filtered_population_does_not_throw():
    flights = make_flights([{"month": 1, "arr_delay": 20.0}])
    result = compute_metrics(flights, group_by="origin", filters={"month": 12})
    assert result.empty
    assert list(result.columns[:1]) == ["origin"]


def test_all_cancelled_group_has_zero_delay_rate_not_nan():
    flights = make_flights([
        {"dep_time": np.nan, "arr_delay": np.nan},
        {"dep_time": np.nan, "arr_delay": np.nan},
    ])
    result = compute_metrics(flights, group_by="origin")
    assert result.loc[0, "rated_count"] == 0
    assert result.loc[0, "delay_rate"] == 0.0
    assert result.loc[0, "cancellation_rate"] == 1.0


def test_invalid_group_by_raises():
    flights = make_flights([{}])
    with pytest.raises(ValueError):
        compute_metrics(flights, group_by="carrier")
