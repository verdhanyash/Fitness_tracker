"""Main FastAPI application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import API_HOST, API_PORT
from app.database import engine, Base
from app.routers import auth, fitness, health

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="Fitness & Health Tracker API",
    description="A comprehensive fitness and health tracking API with JWT authentication",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS for dashboard access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8050", "http://127.0.0.1:8050"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(fitness.router)
app.include_router(health.router)


@app.get("/", tags=["Root"])
def root():
    """Root endpoint with API information."""
    return {
        "message": "Fitness & Health Tracker API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health", tags=["Health Check"])
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=API_HOST, port=API_PORT, reload=True)
