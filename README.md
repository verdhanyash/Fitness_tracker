# Fitness & Health Tracker

A full-stack fitness and health tracking application with FastAPI backend, PostgreSQL database, JWT authentication, and interactive Plotly/Dash dashboard.

## Features

- **JWT Authentication**: Secure user registration and login
- **Fitness Records**: Track workouts with type, duration, calories, and distance
- **Health Metrics**: Monitor weight, steps, water intake, sleep, and heart rate
- **Interactive Dashboard**: 5+ visualization types with real-time updates
- **CRUD Forms**: Add and delete records directly from the dashboard
- **Date Filtering**: Filter data by date range and workout type

## Technology Stack

- **Backend**: FastAPI, SQLAlchemy, PostgreSQL
- **Authentication**: JWT (python-jose), bcrypt
- **Dashboard**: Plotly, Dash, Dash Bootstrap Components
- **Database**: PostgreSQL with SQLAlchemy ORM

## Setup Instructions

### Prerequisites

- Python 3.9+
- PostgreSQL database

### Installation

1. Clone the repository and navigate to the project directory

2. Create a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file from the example:
```bash
copy .env.example .env
```

5. Update `.env` with your PostgreSQL credentials:
```
DATABASE_URL=postgresql://username:password@localhost:5432/fitness_tracker
JWT_SECRET_KEY=your-secure-secret-key
```

6. Create the database:
```sql
CREATE DATABASE fitness_tracker;
```

7. Initialize and seed the database:
```bash
python scripts/init_db.py
python scripts/seed_data.py
```

### Running the Application

1. Start the FastAPI backend:
```bash
python -m uvicorn app.main:app --reload --port 8000
```

2. In a new terminal, start the Dash dashboard:
```bash
python dashboard/app.py
```

3. Access the application:
   - Dashboard: http://localhost:8050
   - API Docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Demo Credentials

After running the seed script:
- Username: `demo`
- Password: `demo123`

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get JWT token
- `GET /auth/me` - Get current user info

### Fitness Records
- `GET /fitness-records` - List records (with filters)
- `POST /fitness-records` - Create record
- `GET /fitness-records/{id}` - Get record
- `PUT /fitness-records/{id}` - Update record
- `DELETE /fitness-records/{id}` - Delete record

### Health Metrics
- `GET /health-metrics` - List metrics (with filters)
- `POST /health-metrics` - Create metric
- `GET /health-metrics/{id}` - Get metric
- `PUT /health-metrics/{id}` - Update metric
- `DELETE /health-metrics/{id}` - Delete metric

## Dashboard Visualizations

1. **Workout Distribution Pie Chart** - Shows breakdown of workout types
2. **Calories Burned Line Chart** - Tracks calories over time
3. **Daily Steps Bar Chart** - Displays daily step counts with goal line
4. **Weight Trend Line Chart** - Monitors weight changes
5. **Sleep & Water Area Chart** - Visualizes sleep and hydration patterns

## Project Structure

```
├── app/
│   ├── __init__.py
│   ├── config.py          # Configuration settings
│   ├── database.py        # Database connection
│   ├── main.py            # FastAPI application
│   ├── models.py          # SQLAlchemy models
│   ├── schemas.py         # Pydantic schemas
│   ├── security.py        # JWT and password utilities
│   └── routers/
│       ├── auth.py        # Authentication routes
│       ├── fitness.py     # Fitness records routes
│       └── health.py      # Health metrics routes
├── dashboard/
│   ├── __init__.py
│   ├── app.py             # Dash application
│   ├── api_client.py      # API client
│   ├── callbacks.py       # Dash callbacks
│   └── layouts.py         # Page layouts
├── scripts/
│   ├── init_db.py         # Database initialization
│   └── seed_data.py       # Sample data seeding
├── tests/
├── .env.example
├── requirements.txt
└── README.md
```

## License

MIT License
