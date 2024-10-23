import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State
from datetime import date
import psycopg2  # Import psycopg2 to connect to PostgreSQL


# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

# PostgreSQL connection string (replace with your actual connection details)
DB_CONNECTION = "postgresql://postgres.ysthgyildvykrrxyremj:vg1okT8Ht5kiayW4@aws-0-eu-central-1.pooler.supabase.com:6543/postgres"

# Define the layout for the application, including routing
app.layout = dbc.Container(
    [
        dcc.Location(id="url", refresh=False),  # For routing
        html.Div(id="page-content"),  # Dynamic content will be loaded here
        dbc.Toast(
            id="toast",
            header="Notification",
            is_open=False,  # Initially not open
            duration=4000,  # Display duration in milliseconds
            dismissable=True,  # Allow it to be dismissed
            icon='success',
            style={"position": "fixed", "top": "20px", "right": "20px"},
        )
    ]
)

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
        html.Div(id="output", className="mt-4"),  # For displaying the result
    ],
    className="mt-5"
)

# Function to insert patient data into PostgreSQL
def insert_patient_data(first_name, last_name, age, date_value, weight, height):
    try:
        conn = psycopg2.connect(DB_CONNECTION)
        cursor = conn.cursor()

        query = """
        INSERT INTO patients (first_name, last_name, age, date, weight, height)
        VALUES (%s, %s, %s, %s, %s, %s);
        """
        cursor.execute(query, (first_name, last_name, age, date_value, weight, height))
        conn.commit()
        cursor.close()
        conn.close()

        return "Data saved successfully!"
    except Exception as e:
        return f"Error saving data: {e}"


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
     State("height", "value")]
)
def display_patient_data(n_clicks, first_name, last_name, age, date_value, weight, height):
    if n_clicks is None:
        return "", "/", False, ""  # No toast open

    if all([first_name, last_name, age, date_value, weight, height]):
        save_message = insert_patient_data(first_name, last_name, age, date_value, weight, height)
        toast_message = "Form submitted successfully!"  # Set the toast message
        return (
            html.Div([html.H4("Patient Information"), html.P(f"First Name: {first_name}"), save_message]),
            "/home",
            True,  # Show toast after submission
            toast_message  # Pass the toast message
        )
    else:
        return html.P("Please fill in all fields.", className="text-danger"), "", False, ""  # No toast open


# Callback to handle page routing
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/home":
        print(pathname)
        from home import home_layout
        return home_layout  # Return the layout for the home page
    else:
        print(pathname)
        return login_layout  # Default to the login page


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
