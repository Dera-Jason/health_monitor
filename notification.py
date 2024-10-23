import dash_bootstrap_components as dbc
from dash import html, dcc


def create_notification():
    # This function creates a simple toast notification
    return dbc.Toast(
        [
            html.Div("Form submitted successfully!", className="mb-2"),
        ],
        id="toast-notification",
        header="Notification",
        is_open=False,  # Will be triggered on form submission
        dismissable=True,  # Allows users to close the toast
        duration=5000,  # Toast will disappear after 5 seconds
        icon="success",  # You can customize the icon (like 'primary', 'danger', etc.)
        style={"position": "fixed", "top": 10, "right": 10, "width": 350},
    )
