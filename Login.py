import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State
from datetime import date

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout for the patient login page
app.layout = dbc.Container(
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
                        dbc.Input(id="date", type="text", value=str(date.today()), readonly=True),  # Corrected 'readonly'
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
        dbc.Button("Submit", id="submit-button", color="primary", className="mt-4"),
        html.Div(id="output", className="mt-4")  # For displaying the result
    ],
    className="mt-5"
)

# Callback to capture form data and display it
@app.callback(
    Output("output", "children"),
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
        return ""

    # Check if all inputs are filled
    if all([first_name, last_name, age, date_value, weight, height]):
        return html.Div([
            html.H4("Patient Information:"),
            html.P(f"First Name: {first_name}"),
            html.P(f"Last Name: {last_name}"),
            html.P(f"Age: {age}"),
            html.P(f"Date: {date_value}"),
            html.P(f"Weight: {weight} kg"),
            html.P(f"Height: {height} cm")
        ])
    else:
        return html.P("Please fill in all fields.", className="text-danger")


# Run the Dash app
if __name__ == "__main__":
    app.run_server(debug=True)
