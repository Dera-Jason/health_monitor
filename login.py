import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State
from database import insert_patient_data
from datetime import date
from notification import create_notification

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

login_layout = dbc.Container(
    [
        html.H2("Enter Patient Data", className="text-center mb-4"),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Label("First Name"),
                        dbc.Input(id="first-name", type="text", placeholder="Enter first name"),
                    ],
                    width=6
                ),
                dbc.Col(
                    [
                        dbc.Label("Last Name"),
                        dbc.Input(id="last-name", type="text", placeholder="Enter last name"),
                    ],
                    width=6
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Label("Age"),
                        dbc.Input(id="age", type="number", placeholder="Enter age"),
                    ],
                    width=6
                ),
                dbc.Col(
                    [
                        dbc.Label("Date"),
                        dbc.Input(id="date", type="text", value=str(date.today()), readonly=True),
                    ],
                    width=6
                ),
            ],
            className="mt-3"
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Label("Weight (kg)"),
                        dbc.Input(id="weight", type="number", placeholder="Enter weight"),
                    ],
                    width=6
                ),
                dbc.Col(
                    [
                        dbc.Label("Height (cm)"),
                        dbc.Input(id="height", type="number", placeholder="Enter height"),
                    ],
                    width=6
                ),
            ],
            className="mt-3"
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Label("Gender"),
                        dbc.RadioItems(
                            options=[
                                {"label": "Male", "value": "Male"},
                                {"label": "Female", "value": "Female"}
                            ],
                            id="gender",
                            inline=True,
                        ),
                    ],
                    width=6
                ),
            ],
            className="mt-3"
        ),
        dbc.Button("Submit", id="submit-button", color="primary", className="mt-4"),
        html.Div(id="output", className="mt-4"),
        create_notification() # Add the toast notification here
    ],
    className="mt-5"
)


@app.callback(
    [Output("output", "children"),
     Output("toast-notification", "is_open"),  # Add notification state to the output
     Output("url", "pathname")],
    [Input("submit-button", "n_clicks")],
    [State("first-name", "value"),
     State("last-name", "value"),
     State("age", "value"),
     State("date", "value"),
     State("weight", "value"),
     State("height", "value"),
     State("gender", "value")]
)
def display_patient_data(n_clicks, first_name, last_name, age, date_value, weight, height, gender):
    if n_clicks is None:
        print(f"Submit button clicked {n_clicks} times.")  # Debug: Check how many times button is clicked
        # Check the inputs being passed
        print(
            f"First Name: {first_name}, Last Name: {last_name}, Age: {age}, Date: {date_value}, Weight: {weight}, Height: {height}, Gender: {gender}")
        return "", False, "/"  # Default state

    if all([first_name, last_name, age, date_value, weight, height, gender]):
        # Insert into database
        try:
            save_message = insert_patient_data(first_name, last_name, age, date_value, weight, height, gender)
            print(f"Data saved: {save_message}")  # Debug: Check if the data was saved
            return html.P(save_message, className="text-success"), True, "/home"  # Success
        except Exception as e:
            print(f"Error saving data: {e}")  # Debug: Capture any errors during save
            return html.P(f"Error: {e}", className="text-danger"), False, "/login"
    else:
        print("Please fill in all fields.")  # Debug: Ensure all fields are filled
        return html.P("Please fill in all fields.", className="text-danger"), False, "/login"  # No notification

