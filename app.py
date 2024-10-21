from dash import dcc, html, Dash
from dash.dependencies import Input, Output
from home import home_layout  # Import the home layout
from login import login_layout  # Import the login layout
import dash_bootstrap_components as dbc

# Create the Dash app instance
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

# Define the layout for the app
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),  # Enables URL tracking
    html.Div(id='page-content'),  # Dynamic content will be loaded here
])


# Callback to handle page routing
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/" or pathname == "/home":
        return home_layout  # Load the home page
    elif pathname == "/login":
        return login_layout  # Load the login page
    else:
        return home_layout  # Default to home page if the route doesn't match


if __name__ == "__main__":
    app.run_server(debug=True)
