# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

app = Dash(__name__)

colors = {"background": "#111111", "text": "#7FDBFF"}

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame(
    {
        "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
        "Amount": [4, 1, 2, 2, 4, 5],
        "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"],
    }
)
df2 = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv"
)

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

fig.update_layout(
    plot_bgcolor=colors["background"],
    paper_bgcolor=colors["background"],
    font_color=colors["text"],
)

app.layout = html.Div(
    style={"backgroundColor": colors["background"]},
    children=[
        html.H1(
            children="Hello Dash",
            style={
                "textAlign": "center",
                "color": colors["text"],
            },
        ),
        html.Div(
            children="Dash: A web application framework for your data.",
            style={
                "textAlign": "center",
                "color": colors["text"],
            },
        ),
        dcc.Graph(
            id="example-graph-2",
            figure=fig,
        ),
        dcc.Graph(id="graph-with-slider"),
        dcc.Slider(
            df2["year"].min(),
            df2["year"].max(),
            step=None,
            value=df2["year"].min(),
            marks={str(year): str(year) for year in df2["year"].unique()},
            id="year-slider",
        ),
    ],
)


@app.callback(Output("graph-with-slider", "figure"), Input("year-slider", "value"))
def update_figure(selected_year):
    filtered_df = df2[df2.year == selected_year]

    fig = px.scatter(
        filtered_df,
        x="gdpPercap",
        y="lifeExp",
        size="pop",
        color="continent",
        hover_name="country",
        log_x=True,
        size_max=55,
    )

    fig.update_layout(transition_duration=500)

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
