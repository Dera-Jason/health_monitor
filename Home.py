from dash import dcc, html, dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import random

from urllib3.util.connection import allowed_gai_family

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY], suppress_callback_exceptions=True)


def generate_pleth_wave():
    return go.Figure(go.Scatter(
        y=[random.uniform(-0.2, 1.2) for _ in range(100)],
        mode='lines',
        line=dict(color='#00ccff', width=2)
    )).update_layout(
        paper_bgcolor='black', plot_bgcolor='black',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        height=200, margin=dict(l=0, r=0, t=10, b=10)
    )


home_layout = dbc.Container([
    dcc.Location(id="url", refresh=False),  # For routing
    html.Div(id="page-content"),  # Dynamic content will be loaded here
    dbc.Row([
        dbc.Col([
            html.Label("Pleth", style={"color": "#00ccff", "font-size": "24px"}),
            dcc.Graph(id="pleth-wave", config={'displayModeBar': False}, style={"height": "250px"})
        ], width=9),
        dbc.Col([
            html.Label("HR", style={"color": "green", "font-size": "24px"}),
            html.H2(id="heart-rate", style={"color": "green", "font-size": "50px"}),
            html.Span("bpm", style={"color": "green", "font-size": "20px"})
        ], width=3),
    ], className="g-3", style={"padding": "20px"}),
    dbc.Row([
        dbc.Col([
            html.Label("NBP (Systolic/Diastolic)", style={"color": "purple", "font-size": "24px"}),
            html.H2(id="blood-pressure", style={"color": "purple", "font-size": "50px"}),
            html.Span("mmHg", style={"color": "purple", "font-size": "20px"})
        ], width=6),
        dbc.Col([
            html.Label("Temp", style={"color": "orange", "font-size": "24px"}),
            html.H2(id="temperature", style={"color": "orange", "font-size": "50px"}),
            html.Span("°C", style={"color": "orange", "font-size": "20px"})
        ], width=6),
    ], className="g-3", style={"padding": "20px"}),
    dbc.Row([
        dbc.Col(
            dbc.Button("Add New Patient's Data", id="add-data-button", color="primary",
                       style={"width": "100%", "font-size": "24px"}),
            width=12
        ),
    ], className="g-3", style={"padding": "20px"}),
    dcc.Interval(id="interval-component", interval=1000, n_intervals=0)
], style={"height": "200vh", "width": "200vw", "background-color": "black", "padding": "20px"})

app.layout = home_layout


@app.callback(
    [Output("heart-rate", "children"),
     Output("pleth-wave", "figure"),
     Output("blood-pressure", "children"),
     Output("temperature", "children")],
    [Input("interval-component", "n_intervals")]
)
def update_vitals(n):
    heart_rate = random.randint(60, 120)
    pleth_wave = generate_pleth_wave()
    systolic = random.randint(90, 140)
    diastolic = random.randint(60, 90)
    blood_pressure = f"{systolic}/{diastolic}"
    temperature = round(random.uniform(36.0, 38.0), 1)
    return heart_rate, pleth_wave, blood_pressure, temperature


# login_layout = dbc.Container([
#     dcc.Location(id='url'),  # For handling routing
#     dbc.Row([
#         dbc.Col([
#             html.H2("Login", style={"textAlign": "center", "color": "#00ccff"}),
#             dbc.Form([
#                 dbc.Label("Username", style={"color": "#00ccff"}),
#                 dbc.Input(type="text", id="username", placeholder="Enter your username"),
#             ]),
#             dbc.Form([
#                 dbc.Label("Password", style={"color": "#00ccff"}),
#                 dbc.Input(type="password", id="password", placeholder="Enter your password"),
#             ]),
#             dbc.Button("Login", id="login-button", color="primary", style={"width": "100%"}),
#         ], width=6),
#     ], justify="center", style={"height": "100vh"}),
# ])

# Home page layout
home_layout = dbc.Container(
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
                    dbc.Button("Add New Patient's Data", id="new-patient-button", color="primary",
                               style={"width": "100%", "font-size": "24px"}),
                    width=12  # Full width for the button
                ),
            ], className="g-3", style={"padding": "20px"}
        ),
        dcc.Interval(id="interval-component", interval=1000, n_intervals=0)  # Updates every second
    ],
    style={"height": "100vh", "width": "100vw", "background-color": "black", "padding": "20px"}
)


# Callback to redirect to login page when button is clicked
@app.callback(
    Output("url", "pathname"),
    Input("new-patient-button", "n_clicks")
)
def go_to_login(n_clicks):
    if n_clicks:
        return "/login"  # Redirect to login page
    return dash.no_update


# Callback to handle page routing
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/home":
        return home_layout  # Return the layout for the home page
    elif pathname == "/login":
        from Login import login_layout
        return login_layout  # Return the layout for the login page
    else:
        from Login import login_layout
        return login_layout  # Default to the login page


# @app.callback(
#     Output("url", "pathname"),
#     Input("add-data-button", "n_clicks"),
#     prevent_initial_call=True
# )
# def navigate_to_login(n_clicks):
#     if n_clicks:
#         return "/login"  # Redirect to login page
#     return dash.no_update


if __name__ == "__main__":
    app.run_server(debug=True)
