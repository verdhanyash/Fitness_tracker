"""Dashboard page layouts."""
from dash import html, dcc
import dash_bootstrap_components as dbc


def login_layout():
    """Login page layout."""
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H2("Fitness & Health Tracker", className="text-center mb-4 mt-5"),
                html.P("Track your workouts and health metrics", className="text-center text-muted mb-4"),
                
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Login", className="card-title mb-4"),
                        dbc.Input(id="login-username", placeholder="Username", className="mb-3"),
                        dbc.Input(id="login-password", type="password", placeholder="Password", className="mb-3"),
                        dbc.Button("Login", id="login-button", color="primary", className="w-100 mb-3"),
                        html.Div(id="login-error", className="text-danger"),
                        html.Hr(),
                        html.P("Don't have an account?", className="text-center mb-2"),
                        dbc.Button("Register", id="show-register", color="secondary", outline=True, className="w-100")
                    ])
                ], className="shadow")
            ], width={"size": 4, "offset": 4})
        ])
    ], fluid=True)


def register_layout():
    """Registration page layout."""
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H2("Create Account", className="text-center mb-4 mt-5"),
                
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Register", className="card-title mb-4"),
                        dbc.Input(id="register-username", placeholder="Username", className="mb-3"),
                        dbc.Input(id="register-email", type="email", placeholder="Email", className="mb-3"),
                        dbc.Input(id="register-password", type="password", placeholder="Password", className="mb-3"),
                        dbc.Button("Register", id="register-button", color="primary", className="w-100 mb-3"),
                        html.Div(id="register-error", className="text-danger"),
                        html.Div(id="register-success", className="text-success"),
                        html.Hr(),
                        dbc.Button("Back to Login", id="show-login", color="secondary", outline=True, className="w-100")
                    ])
                ], className="shadow")
            ], width={"size": 4, "offset": 4})
        ])
    ], fluid=True)


def dashboard_layout():
    """Main dashboard layout with charts and CRUD forms."""
    return dbc.Container([
        # Header
        dbc.Navbar([
            dbc.Container([
                dbc.NavbarBrand("Fitness & Health Tracker", className="ms-2"),
                dbc.Nav([
                    html.Span(id="user-display", className="navbar-text me-3"),
                    dbc.Button("Logout", id="logout-button", color="light", size="sm")
                ], className="ms-auto")
            ])
        ], color="primary", dark=True, className="mb-4"),
        
        # Date filter
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                html.Label("Date Range Filter"),
                                dcc.DatePickerRange(
                                    id="date-filter",
                                    display_format="YYYY-MM-DD",
                                    className="w-100"
                                )
                            ], width=6),
                            dbc.Col([
                                html.Label("Workout Type"),
                                dcc.Dropdown(
                                    id="workout-type-filter",
                                    options=[
                                        {"label": "All", "value": ""},
                                        {"label": "Running", "value": "running"},
                                        {"label": "Cycling", "value": "cycling"},
                                        {"label": "Swimming", "value": "swimming"},
                                        {"label": "Weightlifting", "value": "weightlifting"},
                                        {"label": "Yoga", "value": "yoga"},
                                        {"label": "HIIT", "value": "hiit"},
                                        {"label": "Walking", "value": "walking"}
                                    ],
                                    value="",
                                    clearable=False
                                )
                            ], width=4),
                            dbc.Col([
                                html.Label(" "),
                                dbc.Button("Refresh", id="refresh-button", color="primary", className="w-100 mt-1")
                            ], width=2)
                        ])
                    ])
                ], className="mb-4")
            ])
        ]),
        
        # Charts Row 1
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Workout Distribution"),
                    dbc.CardBody([dcc.Graph(id="workout-pie-chart")])
                ])
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Calories Burned Over Time"),
                    dbc.CardBody([dcc.Graph(id="calories-line-chart")])
                ])
            ], width=6)
        ], className="mb-4"),
        
        # Charts Row 2
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Daily Steps"),
                    dbc.CardBody([dcc.Graph(id="steps-bar-chart")])
                ])
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Weight Trend"),
                    dbc.CardBody([dcc.Graph(id="weight-line-chart")])
                ])
            ], width=6)
        ], className="mb-4"),
        
        # Charts Row 3
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Sleep & Water Intake"),
                    dbc.CardBody([dcc.Graph(id="sleep-water-chart")])
                ])
            ], width=12)
        ], className="mb-4"),

        # CRUD Forms Row
        dbc.Row([
            # Fitness Record Form
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Add Fitness Record"),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                html.Label("Date"),
                                dcc.DatePickerSingle(id="fitness-date", date=None)
                            ], width=6),
                            dbc.Col([
                                html.Label("Workout Type"),
                                dcc.Dropdown(
                                    id="fitness-workout-type",
                                    options=[
                                        {"label": "Running", "value": "running"},
                                        {"label": "Cycling", "value": "cycling"},
                                        {"label": "Swimming", "value": "swimming"},
                                        {"label": "Weightlifting", "value": "weightlifting"},
                                        {"label": "Yoga", "value": "yoga"},
                                        {"label": "HIIT", "value": "hiit"},
                                        {"label": "Walking", "value": "walking"}
                                    ]
                                )
                            ], width=6)
                        ], className="mb-3"),
                        dbc.Row([
                            dbc.Col([
                                html.Label("Duration (min)"),
                                dbc.Input(id="fitness-duration", type="number", min=1)
                            ], width=4),
                            dbc.Col([
                                html.Label("Calories"),
                                dbc.Input(id="fitness-calories", type="number", min=0)
                            ], width=4),
                            dbc.Col([
                                html.Label("Distance (km)"),
                                dbc.Input(id="fitness-distance", type="number", min=0, step=0.1)
                            ], width=4)
                        ], className="mb-3"),
                        dbc.Input(id="fitness-notes", placeholder="Notes (optional)", className="mb-3"),
                        dbc.Button("Add Record", id="add-fitness-button", color="success", className="w-100"),
                        html.Div(id="fitness-form-message", className="mt-2")
                    ])
                ])
            ], width=6),
            
            # Health Metric Form
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Add Health Metric"),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                html.Label("Date"),
                                dcc.DatePickerSingle(id="health-date", date=None)
                            ], width=6),
                            dbc.Col([
                                html.Label("Weight (kg)"),
                                dbc.Input(id="health-weight", type="number", min=0, step=0.1)
                            ], width=6)
                        ], className="mb-3"),
                        dbc.Row([
                            dbc.Col([
                                html.Label("Steps"),
                                dbc.Input(id="health-steps", type="number", min=0)
                            ], width=4),
                            dbc.Col([
                                html.Label("Water (L)"),
                                dbc.Input(id="health-water", type="number", min=0, step=0.1)
                            ], width=4),
                            dbc.Col([
                                html.Label("Sleep (hrs)"),
                                dbc.Input(id="health-sleep", type="number", min=0, step=0.5)
                            ], width=4)
                        ], className="mb-3"),
                        dbc.Row([
                            dbc.Col([
                                html.Label("Heart Rate (bpm)"),
                                dbc.Input(id="health-heartrate", type="number", min=30, max=220)
                            ], width=6)
                        ], className="mb-3"),
                        dbc.Button("Add Metric", id="add-health-button", color="success", className="w-100"),
                        html.Div(id="health-form-message", className="mt-2")
                    ])
                ])
            ], width=6)
        ], className="mb-4"),

        # Data Tables Row
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Recent Fitness Records"),
                    dbc.CardBody([
                        html.Div(id="fitness-records-table")
                    ])
                ])
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Recent Health Metrics"),
                    dbc.CardBody([
                        html.Div(id="health-metrics-table")
                    ])
                ])
            ], width=6)
        ])
    ], fluid=True)
