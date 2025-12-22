"""Dashboard callbacks for interactivity."""
from dash import Input, Output, State, callback, html, no_update
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import date

from dashboard.api_client import APIClient
from dashboard.layouts import login_layout, register_layout, dashboard_layout


# Page routing callback
@callback(
    Output('page-content', 'children'),
    Input('url', 'pathname'),
    State('auth-token', 'data')
)
def display_page(pathname, token):
    """Route to appropriate page based on auth status."""
    if token:
        return dashboard_layout()
    if pathname == '/register':
        return register_layout()
    return login_layout()


# Navigation callbacks
@callback(
    Output('url', 'pathname', allow_duplicate=True),
    Input('show-register', 'n_clicks'),
    prevent_initial_call=True
)
def go_to_register(n_clicks):
    if n_clicks:
        return '/register'
    return no_update


@callback(
    Output('url', 'pathname', allow_duplicate=True),
    Input('show-login', 'n_clicks'),
    prevent_initial_call=True
)
def go_to_login(n_clicks):
    if n_clicks:
        return '/login'
    return no_update


# Login callback
@callback(
    Output('auth-token', 'data'),
    Output('user-data', 'data'),
    Output('login-error', 'children'),
    Output('url', 'pathname', allow_duplicate=True),
    Input('login-button', 'n_clicks'),
    State('login-username', 'value'),
    State('login-password', 'value'),
    prevent_initial_call=True
)
def handle_login(n_clicks, username, password):
    if not n_clicks:
        return no_update, no_update, no_update, no_update
    
    if not username or not password:
        return no_update, no_update, "Please enter username and password", no_update
    
    client = APIClient()
    result = client.login(username, password)
    
    if "error" in result:
        return no_update, no_update, "Invalid credentials", no_update
    
    token = result.get("access_token")
    return token, {"username": username}, "", "/"


# Register callback
@callback(
    Output('register-error', 'children'),
    Output('register-success', 'children'),
    Input('register-button', 'n_clicks'),
    State('register-username', 'value'),
    State('register-email', 'value'),
    State('register-password', 'value'),
    prevent_initial_call=True
)
def handle_register(n_clicks, username, email, password):
    if not n_clicks:
        return no_update, no_update
    
    if not username or not email or not password:
        return "Please fill all fields", ""
    
    client = APIClient()
    result = client.register(username, email, password)
    
    if "error" in result:
        detail = result.get("detail", "Registration failed")
        if isinstance(detail, dict):
            detail = detail.get("message", "Registration failed")
        return str(detail), ""
    
    return "", "Registration successful! You can now login."


# Logout callback
@callback(
    Output('auth-token', 'data', allow_duplicate=True),
    Output('user-data', 'data', allow_duplicate=True),
    Output('url', 'pathname', allow_duplicate=True),
    Input('logout-button', 'n_clicks'),
    prevent_initial_call=True
)
def handle_logout(n_clicks):
    if n_clicks:
        return None, None, '/login'
    return no_update, no_update, no_update


# User display callback
@callback(
    Output('user-display', 'children'),
    Input('user-data', 'data')
)
def update_user_display(user_data):
    if user_data:
        return f"Welcome, {user_data.get('username', 'User')}"
    return ""


# Chart update callbacks
@callback(
    Output('workout-pie-chart', 'figure'),
    Output('calories-line-chart', 'figure'),
    Output('steps-bar-chart', 'figure'),
    Output('weight-line-chart', 'figure'),
    Output('sleep-water-chart', 'figure'),
    Input('refresh-button', 'n_clicks'),
    Input('refresh-interval', 'n_intervals'),
    Input('auth-token', 'data'),
    State('date-filter', 'start_date'),
    State('date-filter', 'end_date'),
    State('workout-type-filter', 'value')
)
def update_charts(n_clicks, n_intervals, token, start_date, end_date, workout_type):
    """Update all charts with current data."""
    empty_fig = go.Figure()
    empty_fig.update_layout(
        annotations=[{"text": "No data available", "showarrow": False, "font": {"size": 16}}]
    )
    
    if not token:
        return empty_fig, empty_fig, empty_fig, empty_fig, empty_fig
    
    client = APIClient(token)
    
    # Fetch data
    fitness_records = client.get_fitness_records(start_date, end_date, workout_type if workout_type else None)
    health_metrics = client.get_health_metrics(start_date, end_date)
    
    # Workout distribution pie chart
    if fitness_records:
        df_fitness = pd.DataFrame(fitness_records)
        workout_counts = df_fitness['workout_type'].value_counts()
        pie_fig = px.pie(
            values=workout_counts.values,
            names=workout_counts.index,
            title="Workout Types",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
    else:
        pie_fig = empty_fig

    
    # Calories line chart
    if fitness_records:
        df_fitness = pd.DataFrame(fitness_records)
        df_fitness['date'] = pd.to_datetime(df_fitness['date'])
        calories_by_date = df_fitness.groupby('date')['calories_burned'].sum().reset_index()
        calories_fig = px.line(
            calories_by_date,
            x='date',
            y='calories_burned',
            title="Calories Burned",
            markers=True
        )
        calories_fig.update_traces(line_color='#FF6B6B')
    else:
        calories_fig = empty_fig
    
    # Steps bar chart
    if health_metrics:
        df_health = pd.DataFrame(health_metrics)
        df_health['date'] = pd.to_datetime(df_health['date'])
        df_health = df_health.sort_values('date')
        steps_fig = px.bar(
            df_health,
            x='date',
            y='steps',
            title="Daily Steps",
            color='steps',
            color_continuous_scale='Greens'
        )
        steps_fig.add_hline(y=10000, line_dash="dash", line_color="red", annotation_text="Goal: 10,000")
    else:
        steps_fig = empty_fig
    
    # Weight trend line chart
    if health_metrics:
        df_health = pd.DataFrame(health_metrics)
        df_health['date'] = pd.to_datetime(df_health['date'])
        df_health = df_health.sort_values('date')
        weight_fig = px.line(
            df_health,
            x='date',
            y='weight_kg',
            title="Weight Trend",
            markers=True
        )
        weight_fig.update_traces(line_color='#4ECDC4')
    else:
        weight_fig = empty_fig
    
    # Sleep & Water area chart
    if health_metrics:
        df_health = pd.DataFrame(health_metrics)
        df_health['date'] = pd.to_datetime(df_health['date'])
        df_health = df_health.sort_values('date')
        
        sleep_water_fig = go.Figure()
        sleep_water_fig.add_trace(go.Scatter(
            x=df_health['date'],
            y=df_health['sleep_hours'],
            name='Sleep (hours)',
            fill='tozeroy',
            line=dict(color='#9B59B6')
        ))
        sleep_water_fig.add_trace(go.Scatter(
            x=df_health['date'],
            y=df_health['water_intake_liters'],
            name='Water (liters)',
            fill='tozeroy',
            line=dict(color='#3498DB')
        ))
        sleep_water_fig.update_layout(title="Sleep & Water Intake")
    else:
        sleep_water_fig = empty_fig
    
    return pie_fig, calories_fig, steps_fig, weight_fig, sleep_water_fig


# Add fitness record callback
@callback(
    Output('fitness-form-message', 'children'),
    Output('fitness-date', 'date'),
    Output('fitness-workout-type', 'value'),
    Output('fitness-duration', 'value'),
    Output('fitness-calories', 'value'),
    Output('fitness-distance', 'value'),
    Output('fitness-notes', 'value'),
    Input('add-fitness-button', 'n_clicks'),
    State('auth-token', 'data'),
    State('fitness-date', 'date'),
    State('fitness-workout-type', 'value'),
    State('fitness-duration', 'value'),
    State('fitness-calories', 'value'),
    State('fitness-distance', 'value'),
    State('fitness-notes', 'value'),
    prevent_initial_call=True
)
def add_fitness_record(n_clicks, token, rec_date, workout_type, duration, calories, distance, notes):
    if not n_clicks or not token:
        return no_update, no_update, no_update, no_update, no_update, no_update, no_update
    
    if not rec_date or not workout_type or not duration:
        return html.Span("Please fill required fields", className="text-danger"), no_update, no_update, no_update, no_update, no_update, no_update
    
    client = APIClient(token)
    data = {
        "date": rec_date,
        "workout_type": workout_type,
        "duration_minutes": int(duration),
        "calories_burned": int(calories) if calories else 0,
        "distance_km": float(distance) if distance else None,
        "notes": notes if notes else None
    }
    
    result = client.create_fitness_record(data)
    
    if "error" in result:
        detail = result.get("detail", "Failed to add record")
        if isinstance(detail, dict):
            detail = detail.get("message", "Failed to add record")
        return html.Span(str(detail), className="text-danger"), no_update, no_update, no_update, no_update, no_update, no_update
    
    return html.Span("Record added successfully!", className="text-success"), None, None, None, None, None, None


# Add health metric callback
@callback(
    Output('health-form-message', 'children'),
    Output('health-date', 'date'),
    Output('health-weight', 'value'),
    Output('health-steps', 'value'),
    Output('health-water', 'value'),
    Output('health-sleep', 'value'),
    Output('health-heartrate', 'value'),
    Input('add-health-button', 'n_clicks'),
    State('auth-token', 'data'),
    State('health-date', 'date'),
    State('health-weight', 'value'),
    State('health-steps', 'value'),
    State('health-water', 'value'),
    State('health-sleep', 'value'),
    State('health-heartrate', 'value'),
    prevent_initial_call=True
)
def add_health_metric(n_clicks, token, metric_date, weight, steps, water, sleep, heartrate):
    if not n_clicks or not token:
        return no_update, no_update, no_update, no_update, no_update, no_update, no_update
    
    if not metric_date:
        return html.Span("Please select a date", className="text-danger"), no_update, no_update, no_update, no_update, no_update, no_update
    
    client = APIClient(token)
    data = {
        "date": metric_date,
        "weight_kg": float(weight) if weight else None,
        "steps": int(steps) if steps else None,
        "water_intake_liters": float(water) if water else None,
        "sleep_hours": float(sleep) if sleep else None,
        "heart_rate_bpm": int(heartrate) if heartrate else None
    }
    
    result = client.create_health_metric(data)
    
    if "error" in result:
        detail = result.get("detail", "Failed to add metric")
        if isinstance(detail, dict):
            detail = detail.get("message", "Failed to add metric")
        return html.Span(str(detail), className="text-danger"), no_update, no_update, no_update, no_update, no_update, no_update
    
    return html.Span("Metric added successfully!", className="text-success"), None, None, None, None, None, None


# Data tables callbacks
@callback(
    Output('fitness-records-table', 'children'),
    Input('refresh-button', 'n_clicks'),
    Input('refresh-interval', 'n_intervals'),
    Input('auth-token', 'data'),
    State('date-filter', 'start_date'),
    State('date-filter', 'end_date')
)
def update_fitness_table(n_clicks, n_intervals, token, start_date, end_date):
    if not token:
        return html.P("Please login to view records")
    
    client = APIClient(token)
    records = client.get_fitness_records(start_date, end_date)
    
    if not records:
        return html.P("No fitness records found")
    
    # Show only recent 10 records
    records = records[:10]
    
    table_header = [
        html.Thead(html.Tr([
            html.Th("Date"),
            html.Th("Type"),
            html.Th("Duration"),
            html.Th("Calories"),
            html.Th("Action")
        ]))
    ]
    
    rows = []
    for record in records:
        rows.append(html.Tr([
            html.Td(record['date']),
            html.Td(record['workout_type']),
            html.Td(f"{record['duration_minutes']} min"),
            html.Td(record['calories_burned']),
            html.Td(dbc.Button("Delete", id={"type": "delete-fitness", "index": record['id']}, 
                              color="danger", size="sm"))
        ]))
    
    table_body = [html.Tbody(rows)]
    
    return dbc.Table(table_header + table_body, bordered=True, hover=True, size="sm")


@callback(
    Output('health-metrics-table', 'children'),
    Input('refresh-button', 'n_clicks'),
    Input('refresh-interval', 'n_intervals'),
    Input('auth-token', 'data'),
    State('date-filter', 'start_date'),
    State('date-filter', 'end_date')
)
def update_health_table(n_clicks, n_intervals, token, start_date, end_date):
    if not token:
        return html.P("Please login to view metrics")
    
    client = APIClient(token)
    metrics = client.get_health_metrics(start_date, end_date)
    
    if not metrics:
        return html.P("No health metrics found")
    
    # Show only recent 10 metrics
    metrics = metrics[:10]
    
    table_header = [
        html.Thead(html.Tr([
            html.Th("Date"),
            html.Th("Weight"),
            html.Th("Steps"),
            html.Th("Sleep"),
            html.Th("Action")
        ]))
    ]
    
    rows = []
    for metric in metrics:
        rows.append(html.Tr([
            html.Td(metric['date']),
            html.Td(f"{metric.get('weight_kg', '-')} kg" if metric.get('weight_kg') else "-"),
            html.Td(metric.get('steps', '-')),
            html.Td(f"{metric.get('sleep_hours', '-')} hrs" if metric.get('sleep_hours') else "-"),
            html.Td(dbc.Button("Delete", id={"type": "delete-health", "index": metric['id']},
                              color="danger", size="sm"))
        ]))
    
    table_body = [html.Tbody(rows)]
    
    return dbc.Table(table_header + table_body, bordered=True, hover=True, size="sm")
