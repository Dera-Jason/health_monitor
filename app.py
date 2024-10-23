from dash import dcc, html, Dash
from dash.dependencies import Input, Output, State
# from heartrate_monitor import HeartRateMonitor
from home import home_layout  # Import the home layout
from login import login_layout  # Import the login layout
import dash_bootstrap_components as dbc
from notification import create_notification
from database import insert_patient_data
from threading import Thread
import time

# # Sensor imports
# from MainsWithArdino import HeartRateMonitor  # Assuming this class is well defined
# from MainsWithArdino import DS18B20          # Temperature sensor class
# import serial

# Create the Dash app instance
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

# Define the layout for the app
app.layout = dbc.Container(
    [
        dcc.Location(id='url', refresh=False),  # Enables URL tracking
        html.Div(id='page-content'),  # Dynamic content will be loaded here
        # dcc.Interval(id='interval-component', interval=1000, n_intervals=0),  # Interval to update sensor data every second
        create_notification()  # Use the notification from notification.py
    ]
)


# Callback to capture form data, display it, and save to PostgreSQL, then redirect
@app.callback(
    [Output("output", "children"),
     Output("url", "pathname"),  # Redirect to /home after submission
     Output("toast-notification", "is_open"),  # Control the toast visibility
     Output("toast-notification", "children")],  # Set the toast message
    [Input("submit-button", "n_clicks")],
    [State("first-name", "value"),
     State("last-name", "value"),
     State("age", "value"),
     State("date", "value"),
     State("weight", "value"),
     State("height", "value"),
     State("gender", "value")],
)
def display_patient_data(n_clicks, first_name, last_name, age, date_value, weight, height, gender):
    if n_clicks is None:
        return "", "/", False, ""  # No toast open

    if all([first_name, last_name, age, date_value, weight, height, gender]):
        save_message = insert_patient_data(first_name, last_name, age, date_value, weight, height, gender)
        toast_message = "Form submitted successfully!"  # Set the toast message
        return (
            html.Div([html.H4("Patient Information"), html.P(f"First Name: {first_name}"), save_message]),
            "/home",
            True,  # Show toast after submission
            toast_message  # Pass the toast message
        )
    else:
        return html.P("Please fill in all fields.", className="text-danger"), "", False, ""  # No toast open


# Callback to update the page content based on the URL
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/login':
        return login_layout
    else:
        return home_layout


# # Callback to handle page routing
# @app.callback(Output("page-content", "children"), [Input("url", "pathname")])
# def display_page(pathname):
#     if pathname == "/" or pathname == "/home":
#         return home_layout  # Load the home page
#     elif pathname == "/login":
#         return login_layout  # Load the login page
#     else:
#         return home_layout  # Default to home page if the route doesn't match


# Callback to update sensor data on the UI
@app.callback(
    [Output("heart-rate", "children"),
     Output("spo2-value", "children"),
     Output("pleth-wave", "figure"),
     Output("spo2-wave", "figure")],
    [Input('interval-component', 'n_intervals')]
)
def update_sensor_data(n):
    # Get the latest heart rate from HeartRateMonitor
    hrm = HeartRateMonitor(print_raw=False)
    hrm.start_sensor()
    heart_rate = hrm.get_current_heart_rate() or "N/A"  # Fallback if None

    # Get the latest temperature from DS18B20
    temp_sensor = DS18B20()
    temp_sensor.find_sensors()
    temp_sensor.read_temp()  # Assuming this reads temperature
    temp_celsius = temp_sensor.rows[0][2] if temp_sensor.rows else "N/A"  # Assuming this is the temperature in Celsius

    # Simulating Pleth and SPO2 Waveforms
    pleth_wave_figure = {
        'data': [{'x': list(range(10)), 'y': [heart_rate * 0.5 for _ in range(10)]}],  # Simulated pleth graph
        'layout': {'title': 'Pleth Waveform', 'height': 150, 'xaxis': {'showticklabels': False}}
    }

    spo2_wave_figure = {
        'data': [{'x': list(range(10)), 'y': [99 for _ in range(10)]}],  # Simulated SPO2 graph
        'layout': {'title': 'SPO2 Waveform', 'height': 150, 'xaxis': {'showticklabels': False}}
    }

    # Return the updated values to the respective UI elements
    return str(heart_rate), "99%", pleth_wave_figure, spo2_wave_figure


if __name__ == "__main__":
    app.run_server(debug=True)
