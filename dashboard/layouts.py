"""Dashboard page layouts - Minimalistic Design."""
from dash import html, dcc
import dash_bootstrap_components as dbc


def login_layout():
    """Login page layout."""
    return html.Div([
        html.Div([
            html.H1("fitness tracker", style={
                'fontSize': '2rem',
                'fontWeight': '600',
                'letterSpacing': '-1px',
                'marginBottom': '0.5rem'
            }),
            html.P("track your workouts and health metrics", style={
                'color': '#888888',
                'fontSize': '0.875rem',
                'marginBottom': '3rem'
            }),
            
            dbc.Card([
                dbc.CardBody([
                    html.H4("login", style={
                        'fontWeight': '600',
                        'marginBottom': '1.5rem',
                        'fontSize': '1.125rem'
                    }),
                    dbc.Input(id="login-username", placeholder="username", 
                             style={'marginBottom': '1rem'}),
                    dbc.Input(id="login-password", type="password", placeholder="password",
                             style={'marginBottom': '1.5rem'}),
                    dbc.Button("login", id="login-button", color="primary", 
                              style={'width': '100%', 'marginBottom': '1rem'}),
                    html.Div(id="login-error", style={'color': '#ef4444', 'fontSize': '0.875rem'}),
                    html.Hr(style={'margin': '1.5rem 0'}),
                    html.P("don't have an account?", style={
                        'textAlign': 'center',
                        'color': '#888888',
                        'fontSize': '0.875rem',
                        'marginBottom': '0.75rem'
                    }),
                    dbc.Button("register", id="show-register", outline=True,
                              style={'width': '100%'})
                ])
            ], style={'maxWidth': '360px', 'margin': '0 auto', 'border': '1px solid #e5e5e5'})
        ], style={
            'textAlign': 'center',
            'paddingTop': '10vh',
            'minHeight': '100vh',
            'backgroundColor': '#ffffff'
        })
    ])


def register_layout():
    """Registration page layout."""
    return html.Div([
        html.Div([
            html.H1("create account", style={
                'fontSize': '2rem',
                'fontWeight': '600',
                'letterSpacing': '-1px',
                'marginBottom': '3rem'
            }),
            
            dbc.Card([
                dbc.CardBody([
                    html.H4("register", style={
                        'fontWeight': '600',
                        'marginBottom': '1.5rem',
                        'fontSize': '1.125rem'
                    }),
                    dbc.Input(id="register-username", placeholder="username",
                             style={'marginBottom': '1rem'}),
                    dbc.Input(id="register-email", type="email", placeholder="email",
                             style={'marginBottom': '1rem'}),
                    dbc.Input(id="register-password", type="password", placeholder="password",
                             style={'marginBottom': '1.5rem'}),
                    dbc.Button("register", id="register-button", color="primary",
                              style={'width': '100%', 'marginBottom': '1rem'}),
                    html.Div(id="register-error", style={'color': '#ef4444', 'fontSize': '0.875rem'}),
                    html.Div(id="register-success", style={'color': '#10b981', 'fontSize': '0.875rem'}),
                    html.Hr(style={'margin': '1.5rem 0'}),
                    dbc.Button("back to login", id="show-login", outline=True,
                              style={'width': '100%'})
                ])
            ], style={'maxWidth': '360px', 'margin': '0 auto', 'border': '1px solid #e5e5e5'})
        ], style={
            'textAlign': 'center',
            'paddingTop': '10vh',
            'minHeight': '100vh',
            'backgroundColor': '#ffffff'
        })
    ])


def dashboard_layout():
    """Main dashboard layout with charts and CRUD forms."""
    return html.Div([
        # Black Header
        html.Div([
            html.Div([
                html.Span("fitness tracker", style={
                    'fontWeight': '600',
                    'fontSize': '1.125rem',
                    'letterSpacing': '-0.5px'
                }),
                html.Div([
                    html.Span(id="user-display", style={
                        'color': '#888888',
                        'marginRight': '1.5rem',
                        'fontSize': '0.875rem'
                    }),
                    dbc.Button("logout", id="logout-button", size="sm", outline=True,
                              style={
                                  'color': '#ffffff',
                                  'borderColor': '#333333',
                                  'fontSize': '0.75rem'
                              })
                ], style={'display': 'flex', 'alignItems': 'center'})
            ], style={
                'display': 'flex',
                'justifyContent': 'space-between',
                'alignItems': 'center',
                'maxWidth': '1400px',
                'margin': '0 auto',
                'padding': '0 2rem'
            })
        ], style={
            'backgroundColor': '#000000',
            'color': '#ffffff',
            'padding': '1rem 0'
        }),
        
        # Main Content
        html.Div([
            # Filters Row
            html.Div([
                dbc.Card([
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                html.Label("date range"),
                                dcc.DatePickerRange(
                                    id="date-filter",
                                    display_format="YYYY-MM-DD"
                                )
                            ], width=5),
                            dbc.Col([
                                html.Label("workout type"),
                                dcc.Dropdown(
                                    id="workout-type-filter",
                                    options=[
                                        {"label": "all", "value": ""},
                                        {"label": "running", "value": "running"},
                                        {"label": "cycling", "value": "cycling"},
                                        {"label": "swimming", "value": "swimming"},
                                        {"label": "weightlifting", "value": "weightlifting"},
                                        {"label": "yoga", "value": "yoga"},
                                        {"label": "hiit", "value": "hiit"},
                                        {"label": "walking", "value": "walking"}
                                    ],
                                    value="",
                                    clearable=False,
                                    style={'fontSize': '0.875rem'}
                                )
                            ], width=4),
                            dbc.Col([
                                html.Label(" ", style={'display': 'block'}),
                                dbc.Button("refresh", id="refresh-button", color="primary",
                                          style={'width': '100%', 'marginTop': '0.25rem'})
                            ], width=3)
                        ])
                    ], style={'padding': '1rem'})
                ], style={'marginBottom': '1.5rem'})
            ]),
            
            # Charts Row 1
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("workout distribution"),
                        dbc.CardBody([dcc.Graph(id="workout-pie-chart", config={'displayModeBar': False})])
                    ])
                ], width=6),
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("calories burned"),
                        dbc.CardBody([dcc.Graph(id="calories-line-chart", config={'displayModeBar': False})])
                    ])
                ], width=6)
            ], style={'marginBottom': '1.5rem'}),
            
            # Charts Row 2
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("daily steps"),
                        dbc.CardBody([dcc.Graph(id="steps-bar-chart", config={'displayModeBar': False})])
                    ])
                ], width=6),
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("weight trend"),
                        dbc.CardBody([dcc.Graph(id="weight-line-chart", config={'displayModeBar': False})])
                    ])
                ], width=6)
            ], style={'marginBottom': '1.5rem'}),
            
            # Charts Row 3
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("sleep & hydration"),
                        dbc.CardBody([dcc.Graph(id="sleep-water-chart", config={'displayModeBar': False})])
                    ])
                ], width=12)
            ], style={'marginBottom': '1.5rem'}),

            # CRUD Forms Row
            dbc.Row([
                # Fitness Record Form
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("add fitness record"),
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    html.Label("date"),
                                    dcc.DatePickerSingle(id="fitness-date", date=None)
                                ], width=6),
                                dbc.Col([
                                    html.Label("workout type"),
                                    dcc.Dropdown(
                                        id="fitness-workout-type",
                                        options=[
                                            {"label": "running", "value": "running"},
                                            {"label": "cycling", "value": "cycling"},
                                            {"label": "swimming", "value": "swimming"},
                                            {"label": "weightlifting", "value": "weightlifting"},
                                            {"label": "yoga", "value": "yoga"},
                                            {"label": "hiit", "value": "hiit"},
                                            {"label": "walking", "value": "walking"}
                                        ],
                                        style={'fontSize': '0.875rem'}
                                    )
                                ], width=6)
                            ], style={'marginBottom': '1rem'}),
                            dbc.Row([
                                dbc.Col([
                                    html.Label("duration (min)"),
                                    dbc.Input(id="fitness-duration", type="number", min=1)
                                ], width=4),
                                dbc.Col([
                                    html.Label("calories"),
                                    dbc.Input(id="fitness-calories", type="number", min=0)
                                ], width=4),
                                dbc.Col([
                                    html.Label("distance (km)"),
                                    dbc.Input(id="fitness-distance", type="number", min=0, step=0.1)
                                ], width=4)
                            ], style={'marginBottom': '1rem'}),
                            dbc.Input(id="fitness-notes", placeholder="notes (optional)",
                                     style={'marginBottom': '1rem'}),
                            dbc.Button("add record", id="add-fitness-button", color="primary",
                                      style={'width': '100%'}),
                            html.Div(id="fitness-form-message", style={'marginTop': '0.75rem', 'fontSize': '0.875rem'})
                        ])
                    ])
                ], width=6),
                
                # Health Metric Form
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("add health metric"),
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    html.Label("date"),
                                    dcc.DatePickerSingle(id="health-date", date=None)
                                ], width=6),
                                dbc.Col([
                                    html.Label("weight (kg)"),
                                    dbc.Input(id="health-weight", type="number", min=0, step=0.1)
                                ], width=6)
                            ], style={'marginBottom': '1rem'}),
                            dbc.Row([
                                dbc.Col([
                                    html.Label("steps"),
                                    dbc.Input(id="health-steps", type="number", min=0)
                                ], width=4),
                                dbc.Col([
                                    html.Label("water (L)"),
                                    dbc.Input(id="health-water", type="number", min=0, step=0.1)
                                ], width=4),
                                dbc.Col([
                                    html.Label("sleep (hrs)"),
                                    dbc.Input(id="health-sleep", type="number", min=0, step=0.5)
                                ], width=4)
                            ], style={'marginBottom': '1rem'}),
                            dbc.Row([
                                dbc.Col([
                                    html.Label("heart rate (bpm)"),
                                    dbc.Input(id="health-heartrate", type="number", min=30, max=220)
                                ], width=6)
                            ], style={'marginBottom': '1rem'}),
                            dbc.Button("add metric", id="add-health-button", color="primary",
                                      style={'width': '100%'}),
                            html.Div(id="health-form-message", style={'marginTop': '0.75rem', 'fontSize': '0.875rem'})
                        ])
                    ])
                ], width=6)
            ], style={'marginBottom': '1.5rem'}),
            
            # Data Tables Row
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("recent fitness records"),
                        dbc.CardBody([
                            html.Div(id="fitness-records-table")
                        ])
                    ])
                ], width=6),
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("recent health metrics"),
                        dbc.CardBody([
                            html.Div(id="health-metrics-table")
                        ])
                    ])
                ], width=6)
            ])
        ], style={
            'maxWidth': '1400px',
            'margin': '0 auto',
            'padding': '2rem'
        })
    ], style={'backgroundColor': '#ffffff', 'minHeight': '100vh'})
