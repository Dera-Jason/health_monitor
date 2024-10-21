from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from datetime import date
from dotenv import load_dotenv
import time
import psycopg2
import os

# Load environment variables from .env file
load_dotenv()

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

# PostgreSQL connection string (replace with your actual connection details)
db_connection = os.environ["DB_CONNECTION"]

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

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    dbc.Toast(
        id="toast",
        header="Notification",
        is_open=False,
        duration=4000,
        dismissable=True,
        style={"position": "fixed", "top": "20px", "right": "20px"},
    ),
])

# Layout for the patient login page
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
        # New Gender Section
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
        dcc.Location(id='url-redirect', refresh=True),  # Hidden Location for redirecting
        html.Div(id="output", className="mt-4"),  # For displaying the result
    ],
    className="mt-5"
)


# Function to insert patient data into PostgreSQL
def insert_patient_data(first_name, last_name, age, date_value, weight, height, gender):
    try:
        with psycopg2.connect(db_connection) as conn:
            with conn.cursor() as cursor:
                query = """
                INSERT INTO patients (first_name, last_name, age, date, weight, height, gender)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
                """
                cursor.execute(query, (first_name, last_name, age, date_value, weight, height, gender))
                conn.commit()
                # cursor.close()
                # conn.close()

        return "Data saved successfully!"
    except Exception as e:
        return f"Error saving data: {e}"


dcc.Loading(
    id="loading",
    type="default",
    children=html.Div(id="output")
)


# Callback to capture form data, display it, and save to PostgreSQL, then redirect
@app.callback(
    [Output("output", "children"),
     Output("url", "pathname"),  # Redirect to /home after submission
     Output("toast", "is_open"),  # Control the toast visibility
     Output("toast", "children")],  # Set the toast message
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


# Define the main layout of the app
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),  # Enables the URL tracking
    html.Div(id='page-content')])


# Callback to update the page content based on the URL
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/login':
        return login_layout
    elif pathname == '/history':
        return html.Div("Patient History Page")  # Placeholder for Patient History
    else:
        return home_layout


# Callback to handle form submission and redirect to home page
@app.callback(
    Output('url-redirect', 'href'),
    [Input('submit-button', 'n_clicks')],
    [State('first-name', 'value'), State('last-name', 'value'), State('age', 'value')]
)
def submit_form(n_clicks, first_name, last_name, age):
    if n_clicks is not None and first_name and last_name and age:
        time.sleep(1)  # Simulate processing delay
        return '/'  # Redirect to home page
    return None


# Running the app
if __name__ == "__main__":
    app.run_server(debug=True)
