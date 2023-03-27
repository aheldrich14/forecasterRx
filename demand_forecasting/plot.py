import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pathlib
import plotly.graph_objects as go

import demand_forecasting.data as data
import demand_forecasting.predict as predict


def generate_forecast_plot(df, series, predictions):
    historical = df[:-9]
    actuals = df[-10:]
    predictions = predictions[predictions["series"] == series]
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=historical["time"],
            y=historical[series],
            line_color="DarkBlue",
            name=series,
            marker=dict(
                color="DarkBlue",
                size=6,
            ),
            mode="lines+markers",
            hovertemplate="Actual: %{y}<br><extra></extra>",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=actuals["time"],
            y=actuals[series],
            line_color="DarkBlue",
            name=series,
            marker=dict(
                color="DarkBlue",
                size=6,
            ),
            mode="markers",
            showlegend=False,
            hovertemplate="Actual: %{y}<br><extra></extra>",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=predictions["time"],
            y=predictions[5],
            # fill='tonexty',
            # fillcolor='rgba(0,100,80,0.2)',
            line_color="rgba(255,255,255,0)",
            showlegend=False,
            name="5%",
            hovertemplate="5%: %{y}<br><extra></extra>",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=predictions["time"],
            y=predictions[95],
            fill="tonexty",
            fillcolor="rgba(0,0,255,0.2)",
            line_color="rgba(255,255,255,0)",
            name="90%",
            hovertemplate="95%: %{y}<br><extra></extra>",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=predictions["time"],
            y=predictions[25],
            line_color="rgba(255,255,255,0)",
            showlegend=False,
            name="25%",
            hovertemplate="25%: %{y}<br><extra></extra>",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=predictions["time"],
            y=predictions[75],
            fill="tonexty",
            fillcolor="rgba(0,0,255,0.6)",
            line_color="rgba(255,255,255,0)",
            name="50%",
            hovertemplate="75%: %{y}<br><extra></extra>",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=predictions["time"],
            y=predictions[50],
            line_color="black",
            line_width=1,
            name="Forecast",
            mode="lines",
            hovertemplate="50%: %{y}<br><extra></extra>",
        )
    )
    fig.update_xaxes(title_text="Time")
    fig.update_yaxes(title_text="Dispenses")
    fig.update_layout(title_text=f"Forecasted Usage for {series}")

    return fig
