"""Streamlit entry point. Manual/visual-check only, per ADR 0001 — no automated
tests target this module; flight_dashboard.metrics is the tested seam."""

import calendar
import pathlib

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from flight_dashboard.metrics import compute_metrics

FLIGHTS_CSV_PATH = pathlib.Path(__file__).resolve().parent.parent / "flights.csv"

RATE_SERIES = [
    ("delay_rate", "Delay Rate", "#EF553B"),
    ("cancellation_rate", "Cancellation Rate", "#636EFA"),
    ("unknown_outcome_rate", "Unknown Outcome Rate", "#AB63FA"),
]

# Display label -> (metrics module group_by key, chart x-axis title)
VIEWS = {
    "Origin": "origin",
    "Destination": "dest",
}

# group_by dimension of the top-level view a Route drill-down was launched from ->
# the preposition used when describing the scoped Route view (e.g. "Routes from JFK").
DRILLDOWN_PREPOSITION = {"origin": "from", "dest": "to"}

MONTH_OPTIONS = [("All months", None)] + [
    (calendar.month_name[m], m) for m in range(1, 13)
]
DAY_OF_WEEK_OPTIONS = [("All days", None)] + [
    (calendar.day_name[d], d) for d in range(7)
]
HOUR_OPTIONS = [("All hours", None)] + [(f"{h:02d}:00", h) for h in range(24)]


def select_filter(label: str, options: list[tuple[str, int | None]]) -> int | None:
    index = st.selectbox(label, range(len(options)), format_func=lambda i: options[i][0])
    return options[index][1]


@st.cache_data
def load_flights() -> pd.DataFrame:
    return pd.read_csv(FLIGHTS_CSV_PATH)


def render_rates_chart(metrics: pd.DataFrame, group_col: str, axis_label: str) -> go.Figure:
    fig = go.Figure()
    for column, label, color in RATE_SERIES:
        fig.add_bar(
            name=label,
            x=metrics[group_col],
            y=metrics[column],
            marker_color=color,
            customdata=metrics["scheduled_count"],
            hovertemplate=f"%{{x}}<br>{label}: %{{y:.1%}}<br>Flights: %{{customdata}}<extra></extra>",
        )
    fig.update_layout(
        barmode="group",
        yaxis_tickformat=".0%",
        yaxis_title="Rate",
        xaxis_title=axis_label,
    )
    fig.update_xaxes(categoryorder="array", categoryarray=metrics[group_col])
    return fig


def render_metrics_table(metrics: pd.DataFrame, group_col: str, group_label: str):
    """Renders the ranked metrics table and returns its selection event, so callers
    can drill down into whichever row the user clicks."""
    display = metrics.rename(columns={
        group_col: group_label,
        "scheduled_count": "Flights",
        "delay_rate": "Delay Rate",
        "cancellation_rate": "Cancellation Rate",
        "unknown_outcome_rate": "Unknown Outcome Rate",
    })[[group_label, "Flights", "Delay Rate", "Cancellation Rate", "Unknown Outcome Rate"]]
    return st.dataframe(
        display,
        hide_index=True,
        use_container_width=True,
        on_select="rerun",
        selection_mode="single-row",
        column_config={
            "Delay Rate": st.column_config.NumberColumn(format="percent"),
            "Cancellation Rate": st.column_config.NumberColumn(format="percent"),
            "Unknown Outcome Rate": st.column_config.NumberColumn(format="percent"),
        },
    )


def main() -> None:
    st.set_page_config(page_title="Flight Delay Dashboard", layout="wide")
    st.title("Flight Delay Dashboard")
    st.caption("When and where are you most likely to get delayed? 2013 NYC-departure flights.")

    if "drilldown" not in st.session_state:
        st.session_state.drilldown = None
    drilldown = st.session_state.drilldown

    month_col, day_col, hour_col = st.columns(3)
    with month_col:
        month = select_filter("Month", MONTH_OPTIONS)
    with day_col:
        day_of_week = select_filter("Day of week", DAY_OF_WEEK_OPTIONS)
    with hour_col:
        hour = select_filter("Hour of scheduled departure", HOUR_OPTIONS)

    time_filters = {
        key: value
        for key, value in (("month", month), ("day_of_week", day_of_week), ("hour", hour))
        if value is not None
    }

    flights = load_flights()

    if drilldown is None:
        view_label = st.radio("View", list(VIEWS.keys()), horizontal=True)
        group_by = VIEWS[view_label]

        metrics = compute_metrics(flights, group_by=group_by, filters=time_filters)
        st.plotly_chart(render_rates_chart(metrics, group_by, view_label), use_container_width=True)

        st.caption(f"Click a row to drill down into that {view_label}'s Routes.")
        event = render_metrics_table(metrics, group_by, view_label)
        selected_rows = event.selection.rows
        if selected_rows:
            selected_value = metrics.iloc[selected_rows[0]][group_by]
            st.session_state.drilldown = {"from_view": view_label, "dim": group_by, "value": selected_value}
            st.rerun()
    else:
        from_view = drilldown["from_view"]
        dim = drilldown["dim"]
        value = drilldown["value"]

        if st.button(f"← Back to {from_view} view"):
            st.session_state.drilldown = None
            st.rerun()

        preposition = DRILLDOWN_PREPOSITION[dim]
        st.subheader(f"Routes {preposition} {value}")

        route_filters = {**time_filters, dim: value}
        metrics = compute_metrics(flights, group_by="route", filters=route_filters)
        st.plotly_chart(render_rates_chart(metrics, "route", "Route"), use_container_width=True)
        render_metrics_table(metrics, "route", "Route")


if __name__ == "__main__":
    main()
