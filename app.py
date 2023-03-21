# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash_bootstrap_components as dbc
import demand_forecasting.plot as dfp
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import demand_forecasting.data as data
import demand_forecasting.predict as predict

from dash import Dash, dcc, html, Input, Output

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

colors = {"background": "#111111", "text": "#7FDBFF"}

df = data.load_all_data()
predictions = predict.generate_forecast()
reasons = ["Hol", "VFR", "Bus", "Oth"]  # reasons = med group
regions = ["NSW", "VIC", "QLD", "SA", "WA", "TAS", "NT"]  # region = pharmacy
city_labels = ["city", "noncity"]  # city = med

app.layout = html.Div(
    # style={"backgroundColor": colors["background"]},
    children=[
        html.H1(
            children="ForecasterRx",
            style={
                "textAlign": "center",
                "color": colors["text"],
            },
        ),
        html.Div(
            children="Pharmacy Demand Forecasting",
            style={
                "textAlign": "center",
                "color": colors["text"],
            },
        ),
        html.Div(
            className="row",
            children=[
                html.Div(
                    children=[
                        html.Label(
                            ["Pharmacy:"],
                            style={"font-weight": "bold", "text-align": "center"},
                        ),
                        dcc.Dropdown(
                            options=regions,
                            id="pharmacy-dropdown",
                        ),
                    ],
                    style=dict(width="33.33%"),
                ),
                html.Div(
                    children=[
                        html.Label(
                            ["Medication Group"],
                            style={"font-weight": "bold", "text-align": "center"},
                        ),
                        dcc.Dropdown(
                            options=reasons,
                            id="med-group-dropdown",
                            placeholder="Select a Medication Group",
                        ),
                    ],
                    style=dict(width="33.33%"),
                ),
            ],
            style=dict(display="flex"),
        ),
        dcc.Graph(
            id="demand-forecast",
        ),
    ],
)


@app.callback(
    Output("demand-forecast", "figure"),
    Input("pharmacy-dropdown", "value"),
    Input("med-group-dropdown", "value"),
)
def update_figure(region, reason):
    if region is None:
        if reason is None:
            series = "Total"
        else:
            series = reason
    else:
        if reason is None:
            series = region
        else:
            series = f"{region} - {reason.lower()}"
    fig = dfp.generate_forecast_plot(df, series, predictions)

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
