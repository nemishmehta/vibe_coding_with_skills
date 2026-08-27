"""Streamlit entry point. Manual/visual-check only, per ADR 0001 — no automated
tests target this module; flight_dashboard.metrics is the tested seam."""

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


@st.cache_data
def load_flights() -> pd.DataFrame:
    return pd.read_csv(FLIGHTS_CSV_PATH)


def render_rates_chart(metrics: pd.DataFrame, group_col: str) -> go.Figure:
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
        xaxis_title=group_col.capitalize(),
    )
    fig.update_xaxes(categoryorder="array", categoryarray=metrics[group_col])
    return fig


def main() -> None:
    st.set_page_config(page_title="Flight Delay Dashboard", layout="wide")
    st.title("Flight Delay Dashboard")
    st.caption("When and where are you most likely to get delayed? 2013 NYC-departure flights.")

    flights = load_flights()
    metrics = compute_metrics(flights, group_by="origin")

    st.plotly_chart(render_rates_chart(metrics, "origin"), use_container_width=True)

    st.dataframe(
        metrics.rename(columns={
            "origin": "Origin",
            "scheduled_count": "Flights",
            "delay_rate": "Delay Rate",
            "cancellation_rate": "Cancellation Rate",
            "unknown_outcome_rate": "Unknown Outcome Rate",
        })[["Origin", "Flights", "Delay Rate", "Cancellation Rate", "Unknown Outcome Rate"]],
        hide_index=True,
        use_container_width=True,
        column_config={
            "Delay Rate": st.column_config.NumberColumn(format="percent"),
            "Cancellation Rate": st.column_config.NumberColumn(format="percent"),
            "Unknown Outcome Rate": st.column_config.NumberColumn(format="percent"),
        },
    )


if __name__ == "__main__":
    main()
