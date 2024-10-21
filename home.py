# home.py
from dash import dcc, html
import dash_bootstrap_components as dbc

home_layout = html.Div(
    [
        # First Row - Heart rate and graph
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            [
                                html.Label("Heart Rate (HR)", style={"color": "green", "font-size": "24px"}),
                                html.H2("120", id="heart-rate", style={"color": "green", "font-size": "50px"}),
                                html.Span("bpm", style={"color": "green", "font-size": "20px"}),
                            ],
                            className="data-box"
                        ),
                    ],
                    width={"size": 3},
                    xs=12, sm=6, md=6, lg=3, xl=3,
                ),
                dbc.Col(
                    [
                        dcc.Graph(id="pleth-wave", config={'displayModeBar': False}, style={"height": "150px"})
                    ],
                    width={"size": 9},
                    xs=12, sm=6, md=6, lg=9, xl=9
                ),
                # SPO2 Section with reading and graph (Second Row)
                dbc.Col(
                    [
                        html.Div(
                            [
                                html.Label("SPO2", style={"color": "blue", "font-size": "24px"}),
                                html.H2("99%", id="spo2-value", style={"color": "blue", "font-size": "50px"}),
                                html.Span("%", style={"color": "blue", "font-size": "20px"}),
                            ],
                            className="data-box"
                        ),
                    ],
                    width={"size": 3},
                    xs=12, sm=6, md=6, lg=3, xl=3,
                ),
                dbc.Col(
                    [
                        dcc.Graph(id="spo2-wave", config={'displayModeBar': False}, style={"height": "150px"})
                    ],
                    width={"size": 9},
                    xs=12, sm=6, md=6, lg=9, xl=9
                ),
            ], className="g-3", style={"padding": "20px"}
        ),

        # Third Row - Blood Pressure and Temperature (SPO2 removed)
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        [
                            html.H2("Blood Pressure (NBP)", className="label"),
                            html.H1(
                                [
                                    html.Sup("Sys", style={"font-size": "12px", "vertical-align": "super",
                                                           "margin-right": "4px"}), "****",
                                    "/",
                                    "***", html.Sup("Dia", style={"font-size": "12px", "vertical-align": "super",
                                                                  "margin-left": "4px"})
                                ],
                                className="value"),
                        ],
                        className="data-box"
                    ),
                    width={"size": 6},
                    xs=12, sm=6, md=6, lg=6, xl=6,
                ),
                dbc.Col(
                    html.Div(
                        [
                            html.H2("Temperature (Temp)", className="label"),
                            html.H1("36.9°C", className="value"),
                        ],
                        className="data-box"
                    ),
                    width={"size": 6},
                    xs=12, sm=6, md=6, lg=6, xl=6,
                ),
            ],
            className="row-style"
        ),

        # Fourth Row - Buttons for actions
        dbc.Row(
            [
                dbc.Col(
                    dbc.Button("Login Another Patient", color="primary", className="action-btn", href="/login"),
                    width={"size": 6},
                    xs=12, sm=6, md=6, lg=6, xl=6
                ),
                dbc.Col(
                    dbc.Button("View Patient History", color="primary", className="action-btn", href="/history"),
                    width={"size": 6},
                    xs=12, sm=6, md=6, lg=6, xl=6
                ),
            ], className="row-style"
        )
    ],
    className="main-container",
)
