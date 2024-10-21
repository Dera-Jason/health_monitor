from dash import dcc, html
import dash_bootstrap_components as dbc
from dash import Dash, Input, Output
import random  # Temporary for simulation, replace with actual sensor data

from MainsWithArdino import read_ecg_values, temperature_monitor

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define your layout
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
                                html.H2(id="heart-rate", style={"color": "green", "font-size": "50px"}),
                                # Updated to be dynamic
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
            ], className="g-3", style={"padding": "20px"}
        ),

        # Second Row - SPO2 Section
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            [
                                html.Label("SPO2", style={"color": "blue", "font-size": "24px"}),
                                html.H2(id="spo2-value", style={"color": "blue", "font-size": "50px"}),
                                # Updated to be dynamic
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
            ]
        ),

        # Third Row - Blood Pressure and Temperature
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        [
                            html.H2("Blood Pressure (NBP)", className="label"),
                            html.H1(
                                id="blood-pressure",  # Updated to be dynamic
                                className="value"
                            ),
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
                            html.H1(id="temperature", className="value"),  # Updated to be dynamic
                        ],
                        className="data-box"
                    ),
                    width={"size": 6},
                    xs=12, sm=6, md=6, lg=6, xl=6,
                ),
            ],
            className="row-style"
        ),

        # Fourth Row - Action Buttons
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
        ),

        # Interval component to trigger updates
        dcc.Interval(id='interval-component', interval=1 * 1000, n_intervals=0),  # Updates every second
    ],
    className="main-container",
)

app.layout = home_layout


# Callback to update the heart rate, SPO2, blood pressure, and temperature
@app.callback(
    [
        Output('heart-rate', 'children'),
        Output('spo2-value', 'children'),
        Output('blood-pressure', 'children'),
        Output('temperature', 'children'),
    ],
    Input('interval-component', 'n_intervals')
)
def update_metrics(n):
    # Replace these with actual data from your sensors (this is simulation)
    heart_rate = read_ecg_values()  # Simulate heart rate data
    spo2 = random.randint(95, 100)  # Simulate SPO2 data
    systolic = random.randint(110, 130)
    diastolic = random.randint(70, 90)
    temperature = temperature_monitor()

    # Return the updated values to the UI
    return str(heart_rate), f"{spo2}%", f"{systolic}/{diastolic}", f"{temperature}°C"


if __name__ == "__main__":
    app.run_server(debug=True)