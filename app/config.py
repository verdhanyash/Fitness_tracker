"""Application configuration settings."""
import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration - Use SQLite for easy local development
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./fitness_tracker.db")

# JWT configuration
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24

# API configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))

# Dashboard configuration
DASHBOARD_HOST = os.getenv("DASHBOARD_HOST", "0.0.0.0")
DASHBOARD_PORT = int(os.getenv("DASHBOARD_PORT", "8050"))
