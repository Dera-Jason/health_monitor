import dash_bootstrap_components as dbc
from dash import html
from datetime import date
from notification import create_notification

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
        html.Div(id="output", className="mt-4")
    ],
    className="mt-5"
)
