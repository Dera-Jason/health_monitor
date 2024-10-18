from dash import dcc, html, dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import random

# Initialize the Dash app with suppress_callback_exceptions
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY], suppress_callback_exceptions=True)


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
home_layout = dbc.Container(
    [
        dcc.Location(id='url'),  # Added for routing purposes
        # Heart rate row
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("HR", style={"color": "green", "font-size": "24px"}),
                        html.H2(id="heart-rate", style={"color": "green", "font-size": "50px"}),
                        html.Span("bpm", style={"color": "green", "font-size": "20px"}),
                        html.Div(id="hr-limit-form", style={"display": "none"}),  # Form hidden initially
                        dbc.Button("Set Limit", id="set-hr-limit-btn", n_clicks=0, color="warning", style={"margin-top": "8px"}),
                        html.Div(id="hr-submit-msg", style={"color": "green", "margin-top": "10px"})  # Success message
                    ], width=3
                ),
                # Pleth wave column
                dbc.Col(
                    [
                        html.Label("Pleth", style={"color": "#00ccff", "font-size": "24px"}),
                        dcc.Graph(id="pleth-wave", config={'displayModeBar': False}, style={"height": "250px"})
                    ], width=9
                ),
            ], className="g-3", style={"padding": "20px"}
        ),

        # Blood Pressure
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("NBP (Systolic/Diastolic)", style={"color": "purple", "font-size": "24px"}),
                        html.H2(id="blood-pressure", style={"color": "purple", "font-size": "50px"}),
                        html.Span("mmHg", style={"color": "purple", "font-size": "20px"}),
                        dbc.Button("Set Limit", id="set-hr-limit-btn", color="warning", style={"margin-top": "10px"}),
                        html.Div(id="hr-limit-form", style={"display": "none"}),  # Form hidden initially
                        html.Div(id="hr-submit-msg", style={"color": "green", "margin-top": "10px"})  # Success message
                    ], width=6
                ),
                dbc.Col(
                    [
                        html.Label("Temp", style={"color": "orange", "font-size": "24px"}),
                        html.H2(id="temperature", style={"color": "orange", "font-size": "50px"}),
                        html.Span("°C", style={"color": "orange", "font-size": "20px"}),
                        dbc.Button("Set Limit", id="set-hr-limit-btn", color="warning", style={"margin-top": "10px"}),
                        html.Div(id="hr-limit-form", style={"display": "none"}),  # Form hidden initially
                        html.Div(id="hr-submit-msg", style={"color": "green", "margin-top": "10px"})  # Success message
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

# Set the layout of the app to home_layout
app.layout = home_layout


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
    heart_rate = random.randint(60, 100)
    pleth_wave = generate_pleth_wave()
    systolic = random.randint(90, 120)
    diastolic = random.randint(60, 80)
    blood_pressure = f"{systolic}/{diastolic}"
    temperature = round(random.uniform(36.0, 38.0), 1)

    return heart_rate, pleth_wave, blood_pressure, temperature


# def limit_dropdown(vital_type):
#     return dbc.FormGroup(
#         [
#             dbc.Label(f"Set High Limit for {vital_type}", style={"color": "white"}),
#             dcc.Dropdown(
#                 id=f"{vital_type}-high",
#                 options=[{'label': str(i), 'value': i} for i in range(50, 201)],
#                 placeholder="Select high limit"
#             ),
#             dbc.Label(f"Set Low Limit for {vital_type}", style={"color": "white"}),
#             dcc.Dropdown(
#                 id=f"{vital_type}-low",
#                 options=[{'label': str(i), 'value': i} for i in range(0, 101)],
#                 placeholder="Select low limit"
#             ),
#             dbc.Button("Submit", id="submit-heart-rate-limit", color="success", n_clicks=0)
#         ]
#     )

#
# # Callback to show the heart rate limit dropdowns when "Set Limit" is clicked and handle submission
# @app.callback(
#     [Output("hr-limit-form", "children"),
#      Output("hr-limit-form", "style"),
#      Output("hr-submit-msg", "children")],
#     [Input("set-hr-limit-btn-hr", "n_clicks"),
#      Input("set-hr-limit-btn-bp", "n_clicks"),
#      Input("set-hr-limit-btn-temp", "n_clicks"),
#      Input("submit-heart-rate-limit", "n_clicks")],
#     [State("heart-rate-high", "value"), State("heart-rate-low", "value")],
#     prevent_initial_call=True
# )

# def show_hr_limit_form(set_btn_clicks, submit_btn_clicks, high_limit, low_limit):
#     ctx = dash.callback_context
#
#     if ctx.triggered and ctx.triggered[0]['prop_id'] == 'set-hr-limit-btn.n_clicks':
#         form = limit_dropdown("heart-rate")  # Use the dropdown function
#         return form, {"display": "block"}, dash.no_update  # Show form, no message yet
#
#     elif ctx.triggered and ctx.triggered[0]['prop_id'] == 'submit-heart-rate-limit.n_clicks':
#         success_message = html.Div("Heart rate limits submitted successfully!", style={"color": "green"})
#         return dash.no_update, {"display": "none"}, success_message  # Hide form, show success message
#
#     return dash.no_update, dash.no_update, dash.no_update


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
