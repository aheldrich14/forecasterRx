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

colors = {"background": "#111111", "text": "DarkBlue"}

df = data.load_all_data()
predictions = predict.generate_forecast()
reasons = ["Hol", "VFR", "Bus", "Oth"]  # reasons = med group
regions = ["NSW", "VIC", "QLD", "SA", "WA", "TAS", "NT"]  # region = pharmacy
city_labels = ["city", "noncity"]  # city = med

usage_card = html.Div(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5(
                        "Forecasted Usage",
                        className="card-title",
                        id="usage-header",
                        style={"text-align": "center"},
                    ),
                    dcc.Slider(min=1, max=10, value=10, step=1, id="usage-days"),
                    html.Div(
                        id="usage-low",
                        style={"text-align": "center"},
                    ),
                    html.Div(
                        id="usage-med",
                        style={"text-align": "center"},
                    ),
                    html.Div(
                        id="usage-high",
                        style={"text-align": "center"},
                    ),
                ]
            ),
            className="w-50",
        ),
    ]
)

app.layout = html.Div(
    # style={"backgroundColor": colors["background"]},
    children=[
        html.H1(
            children="ForecasterRx",
            style={
                "textAlign": "center",
            },
        ),
        html.Div(
            children="Pharmacy Demand Forecasting",
            style={
                "textAlign": "center",
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
        usage_card,
    ],
)


@app.callback(
    Output("demand-forecast", "figure"),
    Input("pharmacy-dropdown", "value"),
    Input("med-group-dropdown", "value"),
)
def update_figure(region, reason):
    series = predict.get_hierarchy_str(region, reason)
    fig = dfp.generate_forecast_plot(df, series, predictions)

    return fig


@app.callback(
    Output("usage-low", "children"),
    Input("usage-days", "value"),
    Input("pharmacy-dropdown", "value"),
    Input("med-group-dropdown", "value"),
)
def calc_low_usage(days, region, reason):
    usage = predict.calc_total_usage(predictions, region, reason, 25)

    return f"Aggresive: {usage.iloc[days - 1]:,}"


@app.callback(
    Output("usage-med", "children"),
    Input("usage-days", "value"),
    Input("pharmacy-dropdown", "value"),
    Input("med-group-dropdown", "value"),
)
def calc_med_usage(days, region, reason):
    usage = predict.calc_total_usage(predictions, region, reason, 50)

    return f"Recommended: {usage.iloc[days - 1]:,}"


@app.callback(
    Output("usage-high", "children"),
    Input("usage-days", "value"),
    Input("pharmacy-dropdown", "value"),
    Input("med-group-dropdown", "value"),
)
def calc_high_usage(days, region, reason):
    usage = predict.calc_total_usage(predictions, region, reason, 95)

    return f"Conservative: {usage.iloc[days - 1]:,}"


@app.callback(
    Output("usage-header", "children"),
    Input("usage-days", "value"),
)
def update_usage_header(
    days,
):
    plural = "s" if days > 1 else ""
    return f"Forecasted usage for next {days} day{plural}"


if __name__ == "__main__":
    app.run_server(debug=True)
