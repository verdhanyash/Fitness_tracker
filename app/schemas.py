"""Pydantic schemas for request/response validation."""
from datetime import date, datetime
from typing import Optional, List, Any

from pydantic import BaseModel, EmailStr, Field, field_validator


# ============== User Schemas ==============

class UserCreate(BaseModel):
    """Schema for user registration."""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100)


class UserResponse(BaseModel):
    """Schema for user response."""
    id: str
    username: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    """Schema for login request."""
    username: str
    password: str


class TokenResponse(BaseModel):
    """Schema for JWT token response."""
    access_token: str
    token_type: str = "bearer"


# ============== Fitness Record Schemas ==============

class FitnessRecordCreate(BaseModel):
    """Schema for creating a fitness record."""
    date: date
    workout_type: str
    duration_minutes: int = Field(..., gt=0, le=1440)
    calories_burned: int = Field(..., ge=0, le=10000)
    distance_km: Optional[float] = Field(None, ge=0, le=1000)
    intensity_level: str = Field(default="medium")
    notes: Optional[str] = Field(None, max_length=1000)

    @field_validator('date')
    @classmethod
    def date_not_in_future(cls, v):
        if v > date.today():
            raise ValueError('Date cannot be in the future')
        return v


class FitnessRecordUpdate(BaseModel):
    """Schema for updating a fitness record."""
    date: Optional[date] = None
    workout_type: Optional[str] = None
    duration_minutes: Optional[int] = Field(None, gt=0, le=1440)
    calories_burned: Optional[int] = Field(None, ge=0, le=10000)
    distance_km: Optional[float] = Field(None, ge=0, le=1000)
    intensity_level: Optional[str] = None
    notes: Optional[str] = Field(None, max_length=1000)


class FitnessRecordResponse(BaseModel):
    """Schema for fitness record response."""
    id: str
    user_id: str
    date: date
    workout_type: str
    duration_minutes: int
    calories_burned: int
    distance_km: Optional[float]
    intensity_level: str
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============== Health Metric Schemas ==============

class HealthMetricCreate(BaseModel):
    """Schema for creating a health metric."""
    date: date
    weight_kg: Optional[float] = Field(None, gt=0, le=500)
    steps: Optional[int] = Field(None, ge=0, le=200000)
    water_intake_liters: Optional[float] = Field(None, ge=0, le=20)
    sleep_hours: Optional[float] = Field(None, ge=0, le=24)
    heart_rate_bpm: Optional[int] = Field(None, gt=0, le=300)


class HealthMetricUpdate(BaseModel):
    """Schema for updating a health metric."""
    weight_kg: Optional[float] = Field(None, gt=0, le=500)
    steps: Optional[int] = Field(None, ge=0, le=200000)
    water_intake_liters: Optional[float] = Field(None, ge=0, le=20)
    sleep_hours: Optional[float] = Field(None, ge=0, le=24)
    heart_rate_bpm: Optional[int] = Field(None, gt=0, le=300)


class HealthMetricResponse(BaseModel):
    """Schema for health metric response."""
    id: str
    user_id: str
    date: date
    weight_kg: Optional[float]
    steps: Optional[int]
    water_intake_liters: Optional[float]
    sleep_hours: Optional[float]
    heart_rate_bpm: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============== Common Schemas ==============

class ErrorDetail(BaseModel):
    """Schema for error detail."""
    code: str
    message: str
