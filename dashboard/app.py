"""Main Dash dashboard application."""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

# Create Dash app with Bootstrap theme
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
    title="Fitness & Health Tracker"
)

server = app.server

# App layout with URL routing and token storage
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Store(id='auth-token', storage_type='session'),
    dcc.Store(id='user-data', storage_type='session'),
    dcc.Interval(id='refresh-interval', interval=30000, n_intervals=0),  # 30s refresh
    html.Div(id='page-content')
])

# Import callbacks (must be after app creation)
from dashboard import callbacks


if __name__ == "__main__":
    from app.config import DASHBOARD_HOST, DASHBOARD_PORT
    app.run(host=DASHBOARD_HOST, port=DASHBOARD_PORT, debug=True)
