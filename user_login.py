import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from home import home_layout  # Import your home layout from home.py

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the login page layout
login_layout = dbc.Container(
    [
        html.H2("Login", className="text-center mb-4"),
        dbc.Form([
            dbc.Label("Username"),
            dbc.Input(type="text", id="login-username", placeholder="Enter your username"),
            dbc.Label("Password", className="mt-3"),
            dbc.Input(type="password", id="login-password", placeholder="Enter your password"),
            dbc.Button("Login", id="login-button", color="primary", className="mt-4", n_clicks=0),
            html.Div(id="login-output", className="mt-3"),
        ], className="w-50 mx-auto"),  # Form centered and sized at 50% width
    ],
    className="mt-5"  # Add margin at the top for spacing
)

# App layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),  # Handles routing
    html.Div(id='page-content', children=login_layout)  # Render login page by default
])

# Callback to handle login
@app.callback(
    [Output('login-output', 'children'), Output('url', 'pathname')],  # Two outputs: one for alert, one for redirect
    Input('login-button', 'n_clicks'),
    [State('login-username', 'value'),
     State('login-password', 'value')]
)
def login_user(n_clicks, username, password):
    if n_clicks > 0:
        if username == "admin" and password == "password123":  # Replace with actual authentication logic
            return dbc.Alert(f"Welcome {username}!", color="success"), '/home'  # Redirect to home on success
        else:
            return dbc.Alert("Invalid username or password!", color="danger"), dash.no_update  # No redirect on failure
    return "", dash.no_update  # Initial state, no message, no redirect

# Callback to render different page layouts based on URL
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/home':
        return home_layout  # Show the home page when the user logs in
    else:
        return login_layout  # Default to login page if no match

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
