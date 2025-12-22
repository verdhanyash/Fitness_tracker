# Design Document: Fitness & Health Tracker

## Overview

A full-stack fitness and health tracking application built with FastAPI backend, PostgreSQL database, and Plotly/Dash frontend. The system enables users to track workouts and health metrics through a RESTful API with JWT authentication, visualized through an interactive dashboard with real-time updates and integrated CRUD forms.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Client Layer                              │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Plotly/Dash Dashboard                       │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────────┐   │   │
│  │  │ Charts  │ │ Forms   │ │ Tables  │ │ Auth Forms  │   │   │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────────┘   │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        API Layer (FastAPI)                       │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐   │
│  │ Auth Routes │ │ Fitness     │ │ Health Metrics Routes   │   │
│  │ /auth/*     │ │ Routes      │ │ /health-metrics/*       │   │
│  └─────────────┘ └─────────────┘ └─────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              JWT Authentication Middleware               │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Data Layer                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                 SQLAlchemy ORM                           │   │
│  └─────────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                 PostgreSQL Database                      │   │
│  │  ┌─────────┐ ┌─────────────────┐ ┌─────────────────┐   │   │
│  │  │ Users   │ │ Fitness Records │ │ Health Metrics  │   │   │
│  │  └─────────┘ └─────────────────┘ └─────────────────┘   │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## Components and Interfaces

### 1. Authentication Module

**Purpose:** Handle user registration, login, and JWT token management.

**Interfaces:**

```python
# POST /auth/register
class UserCreate(BaseModel):
    username: str  # 3-50 chars, alphanumeric
    email: EmailStr
    password: str  # min 8 chars

class UserResponse(BaseModel):
    id: UUID
    username: str
    email: str
    created_at: datetime

# POST /auth/login
class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# JWT Payload
class TokenPayload(BaseModel):
    sub: UUID  # user_id
    exp: datetime
    iat: datetime
```

**Security Functions:**
```python
def hash_password(password: str) -> str:
    """Hash password using bcrypt."""
    
def verify_password(plain: str, hashed: str) -> bool:
    """Verify password against hash."""
    
def create_access_token(user_id: UUID) -> str:
    """Create JWT token with 24h expiry."""
    
def get_current_user(token: str) -> User:
    """Decode JWT and return authenticated user."""
```

### 2. Fitness Records Module

**Purpose:** CRUD operations for workout/exercise records.

**Interfaces:**

```python
# POST /fitness-records
class FitnessRecordCreate(BaseModel):
    date: date  # not in future
    workout_type: Literal["cardio", "strength", "yoga", "cycling", "running", "swimming"]
    duration_minutes: int  # > 0
    calories_burned: int  # >= 0
    distance_km: Optional[float]  # >= 0 if provided
    intensity_level: Literal["low", "medium", "high"]
    notes: Optional[str]

# PUT /fitness-records/{id}
class FitnessRecordUpdate(BaseModel):
    date: Optional[date]
    workout_type: Optional[str]
    duration_minutes: Optional[int]
    calories_burned: Optional[int]
    distance_km: Optional[float]
    intensity_level: Optional[str]
    notes: Optional[str]

# Response
class FitnessRecordResponse(BaseModel):
    id: UUID
    user_id: UUID
    date: date
    workout_type: str
    duration_minutes: int
    calories_burned: int
    distance_km: Optional[float]
    intensity_level: str
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime
```

**Endpoints:**
- `GET /fitness-records` - List user's records (with optional filters)
- `POST /fitness-records` - Create new record
- `GET /fitness-records/{id}` - Get specific record
- `PUT /fitness-records/{id}` - Update record
- `DELETE /fitness-records/{id}` - Delete record
- `GET /fitness-records/range` - Get records by date range

### 3. Health Metrics Module

**Purpose:** CRUD operations for daily health measurements.

**Interfaces:**

```python
# POST /health-metrics
class HealthMetricCreate(BaseModel):
    date: date  # not in future, unique per user
    weight_kg: float  # 20-500
    steps: int  # 0-200000
    water_intake_liters: float  # 0-20
    sleep_hours: float  # 0-24
    heart_rate_bpm: Optional[int]  # 30-300 if provided

# PUT /health-metrics/{id}
class HealthMetricUpdate(BaseModel):
    weight_kg: Optional[float]
    steps: Optional[int]
    water_intake_liters: Optional[float]
    sleep_hours: Optional[float]
    heart_rate_bpm: Optional[int]

# Response
class HealthMetricResponse(BaseModel):
    id: UUID
    user_id: UUID
    date: date
    weight_kg: float
    steps: int
    water_intake_liters: float
    sleep_hours: float
    heart_rate_bpm: Optional[int]
    created_at: datetime
    updated_at: datetime
```

**Endpoints:**
- `GET /health-metrics` - List user's metrics (with optional filters)
- `POST /health-metrics` - Create new metric
- `GET /health-metrics/{id}` - Get specific metric
- `PUT /health-metrics/{id}` - Update metric
- `DELETE /health-metrics/{id}` - Delete metric

### 4. Dashboard Module

**Purpose:** Interactive visualization and CRUD forms using Plotly/Dash.

**Components:**

```python
# Layout Structure
app.layout = html.Div([
    # Authentication Section
    dcc.Store(id='auth-token'),
    html.Div(id='auth-container'),  # Login/Register forms
    
    # Main Dashboard (shown when authenticated)
    html.Div(id='dashboard-container', children=[
        # Header with logout
        html.Div(id='header'),
        
        # Date Range Filter
        dcc.DatePickerRange(id='date-filter'),
        
        # Visualizations Row 1
        html.Div([
            dcc.Graph(id='workout-pie-chart'),      # Workout distribution
            dcc.Graph(id='calories-line-chart'),    # Calories over time
        ]),
        
        # Visualizations Row 2
        html.Div([
            dcc.Graph(id='steps-bar-chart'),        # Daily steps
            dcc.Graph(id='weight-trend-chart'),     # Weight trend line
        ]),
        
        # Bonus: Sleep & Water Area Chart
        dcc.Graph(id='sleep-water-area-chart'),
        
        # CRUD Forms Section
        html.Div([
            # Add Fitness Record Form
            html.Div(id='fitness-form'),
            # Add Health Metric Form
            html.Div(id='health-form'),
        ]),
        
        # Data Tables with Delete
        dash_table.DataTable(id='fitness-table'),
        dash_table.DataTable(id='health-table'),
        
        # Auto-refresh interval
        dcc.Interval(id='refresh-interval', interval=5000),
    ])
])
```

**Callbacks:**
- `update_charts()` - Refresh all visualizations on data change
- `handle_login()` - Process login form submission
- `handle_register()` - Process registration form
- `add_fitness_record()` - Submit new fitness record
- `add_health_metric()` - Submit new health metric
- `delete_record()` - Handle record deletion

## Data Models

### Database Schema

**Users Table:**
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
```

**Fitness Records Table:**
```sql
CREATE TABLE fitness_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    workout_type VARCHAR(50) NOT NULL,
    duration_minutes INTEGER NOT NULL CHECK (duration_minutes > 0),
    calories_burned INTEGER NOT NULL CHECK (calories_burned >= 0),
    distance_km FLOAT CHECK (distance_km >= 0),
    intensity_level VARCHAR(20) NOT NULL CHECK (intensity_level IN ('low', 'medium', 'high')),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_fitness_user_date ON fitness_records(user_id, date);
CREATE INDEX idx_fitness_workout_type ON fitness_records(workout_type);
```

**Health Metrics Table:**
```sql
CREATE TABLE health_metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    weight_kg FLOAT NOT NULL CHECK (weight_kg > 0 AND weight_kg <= 500),
    steps INTEGER NOT NULL CHECK (steps >= 0 AND steps <= 200000),
    water_intake_liters FLOAT NOT NULL CHECK (water_intake_liters >= 0 AND water_intake_liters <= 20),
    sleep_hours FLOAT NOT NULL CHECK (sleep_hours >= 0 AND sleep_hours <= 24),
    heart_rate_bpm INTEGER CHECK (heart_rate_bpm > 0 AND heart_rate_bpm <= 300),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (user_id, date)
);

CREATE INDEX idx_health_user_date ON health_metrics(user_id, date);
```

### SQLAlchemy Models

```python
class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    fitness_records = relationship("FitnessRecord", back_populates="user", cascade="all, delete-orphan")
    health_metrics = relationship("HealthMetric", back_populates="user", cascade="all, delete-orphan")

class FitnessRecord(Base):
    __tablename__ = "fitness_records"
    
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, nullable=False)
    workout_type = Column(String(50), nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    calories_burned = Column(Integer, nullable=False)
    distance_km = Column(Float, nullable=True)
    intensity_level = Column(String(20), nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="fitness_records")

class HealthMetric(Base):
    __tablename__ = "health_metrics"
    
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, nullable=False)
    weight_kg = Column(Float, nullable=False)
    steps = Column(Integer, nullable=False)
    water_intake_liters = Column(Float, nullable=False)
    sleep_hours = Column(Float, nullable=False)
    heart_rate_bpm = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="health_metrics")
    
    __table_args__ = (
        UniqueConstraint('user_id', 'date', name='unique_user_date'),
    )
```

### Data Relationships

- One User has many Fitness Records (1:N)
- One User has many Health Metrics (1:N)
- Health Metrics have unique constraint on (user_id, date)
- Cascade delete: When user is deleted, all associated records are deleted

### Data Validation Rules

**Fitness Records:**
- workout_type: Must be one of ['cardio', 'strength', 'yoga', 'cycling', 'running', 'swimming']
- duration_minutes: Must be positive integer (> 0)
- calories_burned: Must be non-negative integer (>= 0)
- distance_km: Optional, must be non-negative if provided (>= 0)
- intensity_level: Must be one of ['low', 'medium', 'high']
- date: Must be valid date, not in future

**Health Metrics:**
- weight_kg: Must be positive float (20-500 kg)
- steps: Must be non-negative integer (0-200000)
- water_intake_liters: Must be non-negative float (0-20 liters)
- sleep_hours: Must be between 0 and 24
- heart_rate_bpm: Optional, must be positive if provided (30-300)
- date: Must be valid date, not in future, unique per user



## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: User Registration Round-Trip

*For any* valid registration data (username, email, password), submitting registration should create a user account where the password is stored as a hash (not plaintext) and the user can subsequently login with the original password.

**Validates: Requirements 1.1, 1.3**

### Property 2: Duplicate Registration Rejection

*For any* existing user, attempting to register with the same username OR the same email should be rejected with an appropriate error response.

**Validates: Requirements 1.2**

### Property 3: Invalid Credentials Rejection

*For any* login attempt with non-existent username OR incorrect password, the system should return 401 Unauthorized status.

**Validates: Requirements 1.4**

### Property 4: JWT Token Authentication

*For any* valid JWT token, requests to protected endpoints should succeed. *For any* invalid, malformed, or expired JWT token, requests should be rejected with 401 status.

**Validates: Requirements 1.5, 1.6**

### Property 5: Fitness Record Creation Round-Trip

*For any* valid fitness record data and authenticated user, creating a record should return the same data with a generated ID and user association, and the record should be retrievable via GET.

**Validates: Requirements 2.1**

### Property 6: Fitness Record Validation

*For any* fitness record with invalid data (invalid workout_type, non-positive duration, negative calories, negative distance, invalid intensity, future date), the system should reject creation with validation errors.

**Validates: Requirements 2.2, 8.4**

### Property 7: Fitness Record Data Isolation

*For any* user, querying fitness records should return ONLY records where user_id matches the authenticated user. No records from other users should be visible.

**Validates: Requirements 2.3**

### Property 8: Fitness Record Update

*For any* fitness record owned by the authenticated user and valid update data, updating should modify the specified fields and update the updated_at timestamp.

**Validates: Requirements 2.4**

### Property 9: Fitness Record Deletion

*For any* fitness record owned by the authenticated user, deleting should remove the record such that subsequent GET returns 404.

**Validates: Requirements 2.5**

### Property 10: Fitness Record Access Control

*For any* fitness record owned by a different user, attempting to read, update, or delete should return 403 Forbidden.

**Validates: Requirements 2.6**

### Property 11: Health Metric Creation Round-Trip

*For any* valid health metric data and authenticated user, creating a metric should return the same data with a generated ID and user association.

**Validates: Requirements 3.1**

### Property 12: Health Metric Validation

*For any* health metric with invalid data (weight outside 20-500, steps outside 0-200000, water outside 0-20, sleep outside 0-24, heart_rate outside 30-300, future date), the system should reject creation with validation errors.

**Validates: Requirements 3.2, 8.4**

### Property 13: Health Metric Data Isolation

*For any* user, querying health metrics should return ONLY metrics where user_id matches the authenticated user.

**Validates: Requirements 3.3**

### Property 14: Health Metric Update

*For any* health metric owned by the authenticated user and valid update data, updating should modify the specified fields and update the updated_at timestamp.

**Validates: Requirements 3.4**

### Property 15: Health Metric Deletion

*For any* health metric owned by the authenticated user, deleting should remove the metric such that subsequent GET returns 404.

**Validates: Requirements 3.5**

### Property 16: Health Metric Unique Date Constraint

*For any* user who already has a health metric for a specific date, attempting to create another metric for the same date should be rejected with a conflict error.

**Validates: Requirements 3.6**

### Property 17: Date Range Filtering - Fitness Records

*For any* date range query on fitness records, ALL returned records should have dates within the specified range (inclusive).

**Validates: Requirements 4.1**

### Property 18: Date Range Filtering - Health Metrics

*For any* date range query on health metrics, ALL returned records should have dates within the specified range (inclusive).

**Validates: Requirements 4.2**

### Property 19: Workout Type Filtering

*For any* workout type filter on fitness records, ALL returned records should have the specified workout_type.

**Validates: Requirements 4.3**

### Property 20: Pagination Correctness

*For any* pagination parameters (limit, offset), the returned records should be a correct subset of the total records, with count not exceeding limit.

**Validates: Requirements 4.4**

### Property 21: Error Response Format Consistency

*For any* error response from the API, the response body should contain a consistent structure with error details.

**Validates: Requirements 8.3**

## Error Handling

### HTTP Status Codes

| Status Code | Usage |
|-------------|-------|
| 200 OK | Successful GET, PUT requests |
| 201 Created | Successful POST (resource created) |
| 204 No Content | Successful DELETE |
| 400 Bad Request | Validation errors, malformed request |
| 401 Unauthorized | Missing/invalid/expired JWT token |
| 403 Forbidden | Access to resource not owned by user |
| 404 Not Found | Resource does not exist |
| 409 Conflict | Duplicate resource (username, email, date) |
| 422 Unprocessable Entity | Request validation failed |
| 500 Internal Server Error | Unexpected server error |

### Error Response Format

```python
class ErrorResponse(BaseModel):
    detail: Union[str, dict]
    
# Validation Error Format (422)
{
    "detail": [
        {
            "loc": ["body", "field_name"],
            "msg": "error message",
            "type": "error_type"
        }
    ]
}

# Business Error Format (400, 401, 403, 404, 409)
{
    "detail": {
        "code": "ERROR_CODE",
        "message": "Human readable message"
    }
}
```

### Error Codes

- `DUPLICATE_USERNAME` - Username already exists
- `DUPLICATE_EMAIL` - Email already registered
- `INVALID_CREDENTIALS` - Wrong username or password
- `TOKEN_EXPIRED` - JWT token has expired
- `TOKEN_INVALID` - JWT token is malformed or invalid
- `RESOURCE_NOT_FOUND` - Requested resource does not exist
- `ACCESS_DENIED` - User does not own the resource
- `DUPLICATE_DATE` - Health metric already exists for this date

## Testing Strategy

### Dual Testing Approach

The application uses both unit tests and property-based tests for comprehensive coverage:

1. **Unit Tests**: Verify specific examples, edge cases, and error conditions
2. **Property-Based Tests**: Verify universal properties across randomly generated inputs

### Property-Based Testing Configuration

- **Framework**: Hypothesis (Python)
- **Minimum iterations**: 100 per property test
- **Tag format**: `**Feature: fitness-health-tracker, Property {number}: {property_text}**`

### Test Categories

**Authentication Tests:**
- Property tests for registration round-trip (Property 1)
- Property tests for duplicate rejection (Property 2)
- Property tests for invalid credentials (Property 3)
- Property tests for JWT validation (Property 4)

**Fitness Records Tests:**
- Property tests for CRUD operations (Properties 5, 8, 9)
- Property tests for validation (Property 6)
- Property tests for data isolation (Property 7)
- Property tests for access control (Property 10)
- Property tests for filtering (Properties 17, 19)

**Health Metrics Tests:**
- Property tests for CRUD operations (Properties 11, 14, 15)
- Property tests for validation (Property 12)
- Property tests for data isolation (Property 13)
- Property tests for unique date constraint (Property 16)
- Property tests for filtering (Property 18)

**API Tests:**
- Property tests for pagination (Property 20)
- Property tests for error format (Property 21)
- Unit tests for OpenAPI documentation endpoint

**Dashboard Tests:**
- Unit tests for component rendering
- Integration tests for form submissions
- Unit tests for chart data transformation

### Test Data Generators

```python
# Hypothesis strategies for generating test data
from hypothesis import strategies as st

# Valid username: 3-50 alphanumeric characters
valid_usernames = st.text(
    alphabet=st.characters(whitelist_categories=('Ll', 'Lu', 'Nd')),
    min_size=3, max_size=50
)

# Valid email
valid_emails = st.emails()

# Valid password: 8+ characters
valid_passwords = st.text(min_size=8, max_size=100)

# Valid workout types
valid_workout_types = st.sampled_from(['cardio', 'strength', 'yoga', 'cycling', 'running', 'swimming'])

# Valid intensity levels
valid_intensity_levels = st.sampled_from(['low', 'medium', 'high'])

# Valid dates (not in future)
valid_dates = st.dates(max_value=date.today())

# Valid fitness record
valid_fitness_records = st.fixed_dictionaries({
    'date': valid_dates,
    'workout_type': valid_workout_types,
    'duration_minutes': st.integers(min_value=1, max_value=1000),
    'calories_burned': st.integers(min_value=0, max_value=10000),
    'distance_km': st.one_of(st.none(), st.floats(min_value=0, max_value=1000)),
    'intensity_level': valid_intensity_levels,
    'notes': st.one_of(st.none(), st.text(max_size=500))
})

# Valid health metric
valid_health_metrics = st.fixed_dictionaries({
    'date': valid_dates,
    'weight_kg': st.floats(min_value=20, max_value=500),
    'steps': st.integers(min_value=0, max_value=200000),
    'water_intake_liters': st.floats(min_value=0, max_value=20),
    'sleep_hours': st.floats(min_value=0, max_value=24),
    'heart_rate_bpm': st.one_of(st.none(), st.integers(min_value=30, max_value=300))
})
```

## Visualization Specifications

### 1. Workout Distribution Pie Chart
- **Data**: Count of fitness records grouped by workout_type
- **Colors**: Distinct color per workout type
- **Features**: Hover tooltips with count and percentage

### 2. Calories Burned Line Chart
- **Data**: Sum of calories_burned per date
- **X-axis**: Date
- **Y-axis**: Total calories
- **Features**: Date range filter, hover tooltips

### 3. Daily Steps Bar Chart
- **Data**: Steps from health_metrics per date
- **X-axis**: Date
- **Y-axis**: Steps count
- **Features**: Color gradient based on step count, goal line at 10,000

### 4. Weight Trend Line Chart
- **Data**: weight_kg from health_metrics over time
- **X-axis**: Date
- **Y-axis**: Weight (kg)
- **Features**: Trend line, moving average

### 5. Sleep & Water Area Chart (Bonus)
- **Data**: sleep_hours and water_intake_liters over time
- **Dual Y-axis**: Sleep (hours) and Water (liters)
- **Features**: Stacked area with transparency
