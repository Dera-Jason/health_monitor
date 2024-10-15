from dash import dcc, html, dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import random

# Initialize the Dash app (not Flask)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])


# Initialize the Pleth Waveform
def generate_pleth_wave():
    return go.Figure(go.Scatter(
        y=[random.uniform(-0.2, 1.2) for _ in range(100)],  # Simulated random waveform
        mode='lines',
        line=dict(color='#00ccff', width=2)
    )).update_layout(
        paper_bgcolor='black', plot_bgcolor='black',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        height=200, margin=dict(l=0, r=0, t=10, b=10)
    )


# Home page layout
home_layout =  dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("Pleth", style={"color": "#00ccff", "font-size": "24px"}),
                        dcc.Graph(id="pleth-wave", config={'displayModeBar': False}, style={"height": "250px"})
                    ], width=9
                ),
                dbc.Col(
                    [
                        html.Label("HR", style={"color": "green", "font-size": "24px"}),
                        html.H2(id="heart-rate", style={"color": "green", "font-size": "50px"}),
                        html.Span("bpm", style={"color": "green", "font-size": "20px"})
                    ], width=3
                ),
            ], className="g-3", style={"padding": "20px"}
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("NBP (Systolic/Diastolic)", style={"color": "purple", "font-size": "24px"}),
                        html.H2(id="blood-pressure", style={"color": "purple", "font-size": "50px"}),
                        html.Span("mmHg", style={"color": "purple", "font-size": "20px"})
                    ], width=6
                ),
                dbc.Col(
                    [
                        html.Label("Temp", style={"color": "orange", "font-size": "24px"}),
                        html.H2(id="temperature", style={"color": "orange", "font-size": "50px"}),
                        html.Span("°C", style={"color": "orange", "font-size": "20px"})
                    ], width=6
                ),
            ], className="g-3", style={"padding": "20px"}
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Button("Add New Patient's Data", color="primary", style={"width": "100%", "font-size": "24px"}),
                    width=12  # Full width for the button
                ),
            ], className="g-3", style={"padding": "20px"}
        ),
        dcc.Interval(id="interval-component", interval=1000, n_intervals=0)  # Updates every second
    ],
    style={"height": "100vh", "width": "100vw", "background-color": "black", "padding": "20px"}
)


# Callback to update the home page values (place in `login.py` since app is there)
# Callback for updating values every second
@app.callback(
    [Output("heart-rate", "children"),
     Output("pleth-wave", "figure"),
     Output("blood-pressure", "children"),
     Output("temperature", "children")],
    [Input("interval-component", "n_intervals")]
)
def update_vitals(n):
    # Generate random values for vitals
    heart_rate = random.randint(60, 120)
    pleth_wave = generate_pleth_wave()
    systolic = random.randint(90, 140)
    diastolic = random.randint(60, 90)
    blood_pressure = f"{systolic}/{diastolic}"
    temperature = round(random.uniform(36.0, 38.0), 1)

    return heart_rate, pleth_wave, blood_pressure, temperature

