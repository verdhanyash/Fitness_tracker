# Implementation Plan: Fitness & Health Tracker

## Overview

Implementation of a full-stack fitness tracking application with FastAPI backend, PostgreSQL database, JWT authentication, and Plotly/Dash dashboard with CRUD forms and real-time updates.

## Tasks

- [x] 1. Set up project structure and dependencies
  - Create directory structure: `app/`, `dashboard/`, `tests/`, `scripts/`
  - Create `requirements.txt` with FastAPI, SQLAlchemy, psycopg2, python-jose, passlib, dash, plotly, hypothesis
  - Create `app/__init__.py`, `app/config.py` for environment configuration
  - Create `.env.example` with database URL and JWT secret templates
  - _Requirements: 7.1, 8.1_

- [x] 2. Implement database models and connection
  - [x] 2.1 Create database connection module
    - Create `app/database.py` with SQLAlchemy engine and session management
    - Configure connection pooling and session lifecycle
    - _Requirements: 7.1_

  - [x] 2.2 Create SQLAlchemy models
    - Create `app/models.py` with User, FitnessRecord, HealthMetric models
    - Implement relationships, indexes, and constraints as per design
    - _Requirements: 7.2, 7.3_

  - [x] 2.3 Create Pydantic schemas
    - Create `app/schemas.py` with request/response models
    - Implement validation rules (date not in future, value ranges)
    - _Requirements: 2.2, 3.2, 8.4_

- [x] 3. Implement authentication system
  - [x] 3.1 Create security utilities
    - Create `app/security.py` with password hashing (bcrypt)
    - Implement JWT token creation and verification
    - Create `get_current_user` dependency for protected routes
    - _Requirements: 1.1, 1.3, 1.5, 1.6_

  - [x] 3.2 Create authentication routes
    - Create `app/routers/auth.py` with POST /auth/register
    - Implement POST /auth/login returning JWT token
    - Add duplicate username/email checking
    - _Requirements: 1.1, 1.2, 1.3, 1.4_

  - [ ]* 3.3 Write property test for registration round-trip
    - **Property 1: User Registration Round-Trip**
    - **Validates: Requirements 1.1, 1.3**

  - [ ]* 3.4 Write property test for duplicate rejection
    - **Property 2: Duplicate Registration Rejection**
    - **Validates: Requirements 1.2**

  - [ ]* 3.5 Write property test for invalid credentials
    - **Property 3: Invalid Credentials Rejection**
    - **Validates: Requirements 1.4**

  - [ ]* 3.6 Write property test for JWT validation
    - **Property 4: JWT Token Authentication**
    - **Validates: Requirements 1.5, 1.6**

- [x] 4. Checkpoint - Authentication complete
  - Ensure all auth tests pass, ask the user if questions arise.

- [x] 5. Implement fitness records CRUD
  - [x] 5.1 Create fitness records routes
    - Create `app/routers/fitness.py` with GET /fitness-records (list with filters)
    - Implement POST /fitness-records with validation
    - Implement GET /fitness-records/{id} with ownership check
    - Implement PUT /fitness-records/{id} with ownership check
    - Implement DELETE /fitness-records/{id} with ownership check
    - _Requirements: 2.1, 2.3, 2.4, 2.5, 2.6_

  - [ ]* 5.2 Write property test for fitness record creation
    - **Property 5: Fitness Record Creation Round-Trip**
    - **Validates: Requirements 2.1**

  - [ ]* 5.3 Write property test for fitness record validation
    - **Property 6: Fitness Record Validation**
    - **Validates: Requirements 2.2, 8.4**

  - [ ]* 5.4 Write property test for data isolation
    - **Property 7: Fitness Record Data Isolation**
    - **Validates: Requirements 2.3**

  - [ ]* 5.5 Write property test for update operation
    - **Property 8: Fitness Record Update**
    - **Validates: Requirements 2.4**

  - [ ]* 5.6 Write property test for deletion
    - **Property 9: Fitness Record Deletion**
    - **Validates: Requirements 2.5**

  - [ ]* 5.7 Write property test for access control
    - **Property 10: Fitness Record Access Control**
    - **Validates: Requirements 2.6**

- [-] 6. Implement health metrics CRUD
  - [x] 6.1 Create health metrics routes
    - Create `app/routers/health.py` with GET /health-metrics (list with filters)
    - Implement POST /health-metrics with validation and unique date check
    - Implement GET /health-metrics/{id} with ownership check
    - Implement PUT /health-metrics/{id} with ownership check
    - Implement DELETE /health-metrics/{id} with ownership check
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6_

  - [ ]* 6.2 Write property test for health metric creation
    - **Property 11: Health Metric Creation Round-Trip**
    - **Validates: Requirements 3.1**

  - [ ]* 6.3 Write property test for health metric validation
    - **Property 12: Health Metric Validation**
    - **Validates: Requirements 3.2, 8.4**

  - [ ]* 6.4 Write property test for data isolation
    - **Property 13: Health Metric Data Isolation**
    - **Validates: Requirements 3.3**

  - [ ]* 6.5 Write property test for update operation
    - **Property 14: Health Metric Update**
    - **Validates: Requirements 3.4**

  - [ ]* 6.6 Write property test for deletion
    - **Property 15: Health Metric Deletion**
    - **Validates: Requirements 3.5**

  - [ ]* 6.7 Write property test for unique date constraint
    - **Property 16: Health Metric Unique Date Constraint**
    - **Validates: Requirements 3.6**

- [x] 7. Checkpoint - CRUD operations complete
  - Ensure all CRUD tests pass, ask the user if questions arise.

- [x] 8. Implement filtering and pagination
  - [x] 8.1 Add date range filtering
    - Add start_date and end_date query parameters to fitness records endpoint
    - Add start_date and end_date query parameters to health metrics endpoint
    - _Requirements: 4.1, 4.2_

  - [x] 8.2 Add workout type filtering
    - Add workout_type query parameter to fitness records endpoint
    - _Requirements: 4.3_

  - [x] 8.3 Add pagination support
    - Add limit and offset query parameters to list endpoints
    - Return total count in response headers or body
    - _Requirements: 4.4_

  - [ ]* 8.4 Write property test for date range filtering
    - **Property 17: Date Range Filtering - Fitness Records**
    - **Property 18: Date Range Filtering - Health Metrics**
    - **Validates: Requirements 4.1, 4.2**

  - [ ]* 8.5 Write property test for workout type filtering
    - **Property 19: Workout Type Filtering**
    - **Validates: Requirements 4.3**

  - [ ]* 8.6 Write property test for pagination
    - **Property 20: Pagination Correctness**
    - **Validates: Requirements 4.4**

- [x] 9. Create main FastAPI application
  - [x] 9.1 Create main application entry point
    - Create `app/main.py` with FastAPI app instance
    - Include all routers (auth, fitness, health)
    - Configure CORS for dashboard access
    - Add OpenAPI documentation configuration
    - _Requirements: 8.1, 8.2_

  - [ ]* 9.2 Write property test for error response format
    - **Property 21: Error Response Format Consistency**
    - **Validates: Requirements 8.3**

- [x] 10. Create database initialization script
  - [x] 10.1 Create seed data script
    - Create `scripts/init_db.py` to create tables
    - Create `scripts/seed_data.py` with 50+ sample records
    - Include demo user for testing
    - _Requirements: 7.4, 7.5_

- [x] 11. Checkpoint - Backend complete
  - Ensure all backend tests pass, verify API via Swagger UI, ask the user if questions arise.

- [x] 12. Implement Dash dashboard layout
  - [x] 12.1 Create dashboard application structure
    - Create `dashboard/app.py` with Dash app instance
    - Create `dashboard/layouts.py` with page layouts
    - Create `dashboard/components.py` with reusable components
    - _Requirements: 5.1_

  - [x] 12.2 Create authentication UI
    - Create login form component with username/password fields
    - Create registration form component
    - Implement token storage in dcc.Store
    - Add logout functionality
    - _Requirements: 1.7, 1.8_

  - [x] 12.3 Create main dashboard layout
    - Create header with user info and logout button
    - Create date range filter component
    - Create responsive grid layout for charts
    - _Requirements: 5.5, 5.7_

- [x] 13. Implement dashboard visualizations
  - [x] 13.1 Create workout distribution pie chart
    - Fetch fitness records from API
    - Group by workout_type and count
    - Create Plotly pie chart with colors and tooltips
    - _Requirements: 5.2_

  - [x] 13.2 Create calories burned line chart
    - Aggregate calories by date
    - Create Plotly line chart with date x-axis
    - Add hover tooltips
    - _Requirements: 5.3_

  - [x] 13.3 Create daily steps bar chart
    - Fetch health metrics from API
    - Create Plotly bar chart with color gradient
    - Add 10,000 step goal line
    - _Requirements: 5.4_

  - [x] 13.4 Create weight trend line chart
    - Plot weight_kg over time
    - Add trend line or moving average
    - _Requirements: 5.1_

  - [x] 13.5 Create sleep & water area chart
    - Create dual y-axis area chart
    - Plot sleep_hours and water_intake_liters
    - Add transparency for stacked view
    - _Requirements: 5.1_

- [x] 14. Implement dashboard CRUD forms
  - [x] 14.1 Create fitness record form
    - Create form with all fitness record fields
    - Add validation feedback
    - Submit to API on form submission
    - _Requirements: 6.1, 6.3, 6.4_

  - [x] 14.2 Create health metric form
    - Create form with all health metric fields
    - Add validation feedback
    - Submit to API on form submission
    - _Requirements: 6.2, 6.3, 6.4_

  - [x] 14.3 Create data tables with delete
    - Create DataTable for fitness records with delete button
    - Create DataTable for health metrics with delete button
    - Handle delete confirmation and API call
    - _Requirements: 6.5, 6.6_

- [x] 15. Implement real-time updates
  - [x] 15.1 Add auto-refresh mechanism
    - Add dcc.Interval component for periodic refresh
    - Create callbacks to update all charts on interval
    - Refresh after form submissions
    - _Requirements: 5.6_

- [x] 16. Checkpoint - Dashboard complete
  - Test all visualizations update correctly, test CRUD forms work, ask the user if questions arise.

- [x] 17. Create documentation and setup
  - [x] 17.1 Create README.md
    - Write project description and features
    - Document technology stack
    - Write setup and installation instructions
    - Document API endpoints
    - Add screenshots of dashboard
    - _Requirements: 8.1_

  - [x] 17.2 Create run scripts
    - Create script to start FastAPI server
    - Create script to start Dash dashboard
    - Create combined startup script
    - _Requirements: 7.1_

- [x] 18. Final checkpoint
  - Run all tests, verify full application flow, ensure documentation is complete.

## Notes

- Tasks marked with `*` are optional property-based tests that can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties
- Unit tests validate specific examples and edge cases
