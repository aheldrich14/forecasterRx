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
            line_color="rgb(0,100,80)",
            name=series,
            marker=dict(
                color="LightSkyBlue",
                size=5,
            ),
            mode="lines+markers",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=actuals["time"],
            y=actuals[series],
            line_color="rgb(0,100,80)",
            name=series,
            marker=dict(
                color="LightSkyBlue",
                size=5,
            ),
            mode="markers",
            showlegend=False,
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
        )
    )
    fig.add_trace(
        go.Scatter(
            x=predictions["time"],
            y=predictions[95],
            fill="tonexty",
            fillcolor="rgba(0,100,80,0.2)",
            line_color="rgba(255,255,255,0)",
            # showlegend=False,
            name="90%",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=predictions["time"],
            y=predictions[25],
            # fill='tonexty',
            # fillcolor='rgba(0,100,80,0.2)',
            line_color="rgba(255,255,255,0)",
            showlegend=False,
        )
    )
    fig.add_trace(
        go.Scatter(
            x=predictions["time"],
            y=predictions[75],
            fill="tonexty",
            fillcolor="rgba(0,100,80,0.6)",
            line_color="rgba(255,255,255,0)",
            # showlegend=False,
            name="50%",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=predictions["time"],
            y=predictions[50],
            line_color="black",
            # showlegend=False,
            name="Forecast",
            mode="lines",
        )
    )
    fig.update_xaxes(title_text="Time")
    fig.update_yaxes(title_text="Dispenses")

    return fig
