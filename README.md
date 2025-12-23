<div align="center">

# 🏋️ Fitness & Health Tracker

A modern, full-stack fitness tracking application with real-time analytics dashboard.

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Dash](https://img.shields.io/badge/Dash-2.14-3F4F75?style=flat&logo=plotly&logoColor=white)](https://dash.plotly.com)

</div>

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔐 **JWT Authentication** | Secure user registration and login |
| 🏃 **Fitness Tracking** | Log workouts with type, duration, calories, distance |
| 📊 **Health Metrics** | Track weight, steps, water intake, sleep, heart rate |
| 📈 **5 Interactive Charts** | Real-time visualizations powered by Plotly |
| ✏️ **CRUD Operations** | Add, view, and delete records from dashboard |
| 🔄 **Auto-refresh** | Dashboard updates every 30 seconds |
| 🎨 **Minimalist UI** | Clean design with Geist Mono font |

---

## 🛠️ Tech Stack

```
Backend          Dashboard         Database
─────────        ─────────         ─────────
FastAPI          Plotly            SQLite (dev)
SQLAlchemy       Dash              PostgreSQL (prod)
Pydantic         Bootstrap
JWT + bcrypt     
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/fitness-health-tracker.git
cd fitness-health-tracker

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Initialize database with sample data
python scripts/init_db.py
python scripts/seed_data.py
```

### Running the Application

**Terminal 1 - Start API Server:**
```bash
python -m uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Start Dashboard:**
```bash
python dashboard/app.py
```

### Access Points

| Service | URL |
|---------|-----|
| 📊 Dashboard | http://localhost:8050 |
| 📚 API Docs | http://localhost:8000/docs |
| 📖 ReDoc | http://localhost:8000/redoc |

---

## 🔑 Demo Credentials

```
Username: demo
Password: demo123
```

---

## 📡 API Reference

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/auth/register` | Register new user |
| `POST` | `/auth/login` | Get JWT token |
| `GET` | `/auth/me` | Current user info |

### Fitness Records
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/fitness-records` | List all records |
| `POST` | `/fitness-records` | Create record |
| `GET` | `/fitness-records/{id}` | Get single record |
| `PUT` | `/fitness-records/{id}` | Update record |
| `DELETE` | `/fitness-records/{id}` | Delete record |

### Health Metrics
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health-metrics` | List all metrics |
| `POST` | `/health-metrics` | Create metric |
| `GET` | `/health-metrics/{id}` | Get single metric |
| `PUT` | `/health-metrics/{id}` | Update metric |
| `DELETE` | `/health-metrics/{id}` | Delete metric |

---

## 📊 Dashboard Visualizations

| Chart | Type | Description |
|-------|------|-------------|
| 🥧 Workout Distribution | Donut | Breakdown by workout type |
| 🔥 Calories Burned | Area | Daily calorie tracking |
| 👟 Daily Steps | Bar | Step count with 10K goal |
| ⚖️ Weight Trend | Line | Weight changes over time |
| 😴 Sleep & Hydration | Dual Area | Sleep hours + water intake |

---

## 📁 Project Structure

```
fitness-health-tracker/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI application
│   ├── config.py         # Configuration settings
│   ├── database.py       # Database connection
│   ├── models.py         # SQLAlchemy models
│   ├── schemas.py        # Pydantic schemas
│   ├── security.py       # JWT & password utils
│   └── routers/
│       ├── auth.py       # Auth endpoints
│       ├── fitness.py    # Fitness endpoints
│       └── health.py     # Health endpoints
├── dashboard/
│   ├── app.py            # Dash application
│   ├── layouts.py        # Page layouts
│   ├── callbacks.py      # Interactivity
│   ├── api_client.py     # API communication
│   └── assets/
│       └── style.css     # Custom styles
├── scripts/
│   ├── init_db.py        # Create tables
│   └── seed_data.py      # Sample data (60 records)
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Environment Variables

Create a `.env` file in the root directory:

```env
DATABASE_URL=sqlite:///./fitness_tracker.db
JWT_SECRET_KEY=your-super-secret-key
API_PORT=8000
DASHBOARD_PORT=8050
```

---

## 📋 Requirements

```
fastapi>=0.104.0
uvicorn>=0.24.0
sqlalchemy>=2.0.0
python-jose>=3.3.0
bcrypt>=4.0.0
pydantic>=2.5.0
dash>=2.14.0
plotly>=5.18.0
pandas>=2.0.0
requests>=2.31.0
python-dotenv>=1.0.0
```

---

## 🎯 Assignment Info

**Course:** CSR210 - Advanced Programming and Database Systems  
**Topic:** Fitness & Health Tracker  

### Covered Units:
- ✅ Unit 1: REST API Development with FastAPI
- ✅ Unit 3: Integrating databases with SQLAlchemy
- ✅ Unit 5: Building analytics dashboards using Plotly and Dash

---

<div align="center">

Made with ❤️ for CSR210

</div>
