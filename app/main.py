# -*- coding: utf-8 -*-
# Import required libraries
import pandas as pd
import numpy as np
import dash
import pathlib
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html


# Setup the app
app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
app.title = 'Yield Curves'
server = app.server

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()

app.layout = html.Div(
    [
        dcc.Store(id="click-output"),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                            ]
                        ),
                        dcc.Markdown(
                            """
                ### A Prescient Economic Predictor:
                
                ### The Yield Curve
                """.replace(
                                "  ", ""
                            ),
                            className="title",
                        ),
                    ]
                ),
                html.Div(
                    [
                        dcc.Slider(
                            min=0,
                            max=10,
                            value=0,
                            marks={
                                0: "1m",
                                1: "3m",
                                2: "6m",
                                3: "1y",
                                4: "2y",
                                5: "3y",
                                6: "5y",
                                7: "7y",
                                8: "10y",
                                9: "20y",
                                10: "30y",
                            },
                            id="slider",
                        )
                    ],
                    className="timeline-slider",
                ),
                html.Div(
                    [
                        html.Button(
                            "Back",
                            id="back",
                            style={"display": "inline-block"},
                            n_clicks=0,
                        ),
                        html.Button(
                            "Next",
                            id="next",
                            style={"display": "inline-block", "marginLeft": "10px"},
                            n_clicks=0,
                        ),
                    ],
                    className="page-buttons",
                ),
                html.Div(
                    [
                        dcc.Markdown(
                            """Want to learn more about Yield curves?
                            
                            """.replace(
                                "  ", ""
                            ),
                        ),
                        html.A(
                            html.Button("Yield Curves Explained", className="learn-more-button"),
                            href="https://www.investopedia.com/articles/investing/110714/understanding-treasury-yield-curve-rates.asp",
                            target="_blank",
                        )
                    ],
                    className="info-button",
                ),
                html.Div(
                    [
                        dcc.Markdown(
                            """The graph built by [@Daulet Nurmanbetov](https://dauletn.com/). Feel free to reach out to me to grab coffee together ☕ 
                            
                            This graph was inspired by [Plotly Dash](https://github.com/plotly/dash-sample-apps/tree/master/apps/dash-yield-curve)
                            """.replace(
                                "  ", ""
                            ),
                            className="acknowledgements",
                        ),
                    ]
                ),
            ],
            className="four columns sidebar",
        ),
        html.Div(
            [
                html.Div([dcc.Markdown(id="text")], className="text-box"),
                dcc.Graph(id="graph", style={"margin": "0px 20px", "height": "45vh"}, 
                          config={
                              "displaylogo": False,
                              "watermark": False,
                              "modeBarButtonsToRemove": [
                                  "orbitRotation","resetCameraDefault3d"
                              ]
                          }),
            ],
            id="page",
            className="eight columns",
        ),
    ],
    className="row flex-display",
    style={"height": "100vh"},
)

df = pd.read_csv(DATA_PATH.joinpath("yield_curve.csv"))

xlist = list(df["x"].dropna())
ylist = list(df["y"].dropna())

del df["x"]
del df["y"]

zlist = []
for row in df.iterrows():
    index, data = row
    zlist.append(data.tolist())

UPS = dict(x=0, y=0, z=1)

CENTERS = dict(x=0.5, y=0.8, z=0)

EYES = dict(x=3.7, y=3.2, z=0.75)

TEXTS = {
    0: """
    ##### Yield curve 101
    The yield curve shows how much it costs the federal government to borrow
    money for a given amount of time, revealing the relationship between long-
    and short-term interest rates.
    
    It is, inherently, a forecast for what the economy holds in the future —
    how much inflation there will be, for example, and how healthy growth will
    be over the years ahead — all embodied in the price of money today,
    tomorrow and many years from now.
    ___
    ###### 1-month Treasury
    """.replace(
        "  ", ""
    ),
    1: """
    &nbsp  
    &nbsp  
    &nbsp  
    &nbsp  
    &nbsp  
    &nbsp  
    &nbsp  
    &nbsp  
    ___
    ###### TARGET Treasury
    """,
}

ANNOTATIONS = {
    0: [],
    1: [],
    2: [],
    3: [],
    4: [],
    5: [],
}


# Make 3d graph
@app.callback(Output("graph", "figure"), [Input("slider", "value")])
def make_graph(value):

    if value is None:
        value = 0

    if value == 0: # 1-month
        z_secondary_beginning = [z[1] for z in zlist if z[0] == "None"]
        z_secondary_end = [z[0] for z in zlist if z[0] != "None"]
        z_secondary = z_secondary_beginning + z_secondary_end
        x_secondary = ["3-month"] * len(z_secondary_beginning) + ["1-month"] * len(
            z_secondary_end
        )
        y_secondary = ylist
        
    elif value == 9:
        z_secondary_beginning = [z[8] for z in zlist if z[9] == "None"]
        z_secondary_end = [z[9] for z in zlist if z[9] != "None"]
        z_secondary = z_secondary_beginning + z_secondary_end
        x_secondary = ["10-year"] * len(z_secondary_beginning) + ["20-year"] * len(
            z_secondary_end
        )
        y_secondary = ylist
        
    elif value == 10:
        z_secondary_1 = [z[9] if z[10] == "None" else z[10] for z in zlist]
        z_secondary = [zlist[i][8] if z == "None" else z for i, z in \
                       enumerate(z_secondary_1)]
        x_secondary_1 = [z[9] if z[10] == "None" else "30-year" for z in zlist]
        x_secondary_2 = ["20-year" if z != "None" and z != "30-year" else z for z in x_secondary_1]
        x_secondary = ["10-year" if z == "None" else z for z in x_secondary_2]
        y_secondary = ylist
        
    else: # 3-month to 30-years
        _column = value
        label = xlist[value]
        z_secondary = [z[_column] for z in zlist]
        x_secondary = [label for i in z_secondary]
        y_secondary = ylist
    
    opacity = 0.35

    trace1 = dict(
        type="surface",
        x=xlist,
        y=ylist,
        z=zlist,
        hoverinfo="x+y+z",
        lighting={
            "ambient": 0.95,
            "diffuse": 0.99,
            "fresnel": 0.01,
            "roughness": 0.01,
            "specular": 0.01,
        },
        colorscale=[
            [-0.8, "rgb(228,51,51)"],
            [-0.4, "rgb(228,111,111)"],
            [0, "rgb(230,245,254)"],
            [0.4, "rgb(123,171,203)"],
            [0.8, "rgb(40,119,174)"],
            [1, "rgb(37,61,81)"],
        ],
        opacity=opacity,
        showscale=False,
        zmax=9.18,
        zmin=0,
        scene="scene",
    )

    trace2 = dict(
        type="scatter3d",
        mode="lines",
        x=x_secondary,
        y=y_secondary,
        z=z_secondary,
        hoverinfo="x+y+z",
        line=dict(color="#444444"),
    )

    data = [trace1, trace2]

    layout = dict(
        autosize=True,
        font=dict(size=12, color="#CCCCCC"),
        margin=dict(t=5, l=5, b=5, r=5),
        showlegend=False,
        hovermode="closest",
        scene=dict(
            aspectmode="manual",
            aspectratio=dict(x=2, y=5, z=1.5),
            camera=dict(up=UPS, center=CENTERS, eye=EYES),
            annotations=[
                dict(
                    y=ylist[-1],
                    x="1-month",
                    z=0.048,
                    text=f"Latest data - {ylist[-1]}",
                    textangle=0,
                    ax=0,
                    ay=-75,
                    font=dict(color="black", size=12),
                    arrowcolor="black",
                    arrowsize=3,
                    arrowwidth=1,
                    arrowhead=1,
                ),
            ],
            xaxis={
                "showgrid": True,
                "title": "",
                "type": "category",
                "zeroline": False,
                "categoryorder": "array",
                "categoryarray": list(reversed(xlist)),
            },
            yaxis={"showgrid": True, "title": "", "type": "date", "zeroline": False},
        ),
    )

    figure = dict(data=data, layout=layout)
    return figure


# Make annotations
@app.callback(Output("text", "children"), [Input("slider", "value")])
def make_text(value):
    if value == 0 or value is None:
        resp = TEXTS[0]
    else:
        resp = TEXTS[1].replace("TARGET",xlist[value])

    return resp


# Button controls
@app.callback(
    [Output("slider", "value"), Output("click-output", "data")],
    [Input("back", "n_clicks"), Input("next", "n_clicks")],
    [State("slider", "value"), State("click-output", "data")],
)
def advance_slider(back, nxt, slider, last_history):

    try:
        if back > last_history["back"]:
            last_history["back"] = back
            return max(0, slider - 1), last_history

        if nxt > last_history["next"]:
            last_history["next"] = nxt
            return min(10, slider + 1), last_history

    # if last_history store is None
    except Exception as error:
        last_history = {"back": 0, "next": 0}
        return slider, last_history


# Run the Dash app
if __name__ == "__main__":
    app.run_server(host = '0.0.0.0', port = 5000, debug=True)
