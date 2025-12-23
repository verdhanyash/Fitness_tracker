"""SQLAlchemy database models."""
import uuid
from datetime import datetime

from sqlalchemy import (
    Column, String, Integer, Float, Text, Date, DateTime,
    ForeignKey, Index, UniqueConstraint, CheckConstraint
)
from sqlalchemy.orm import relationship

from app.database import Base


def generate_uuid():
    return str(uuid.uuid4())


class User(Base):
    """User model for authentication."""
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    fitness_records = relationship(
        "FitnessRecord",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    health_metrics = relationship(
        "HealthMetric",
        back_populates="user",
        cascade="all, delete-orphan"
    )


class FitnessRecord(Base):
    """Fitness record model for workout tracking."""
    __tablename__ = "fitness_records"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    date = Column(Date, nullable=False)
    workout_type = Column(String(50), nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    calories_burned = Column(Integer, nullable=False)
    distance_km = Column(Float, nullable=True)
    intensity_level = Column(String(20), nullable=False, default="medium")
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="fitness_records")

    # Indexes
    __table_args__ = (
        Index('idx_fitness_user_date', 'user_id', 'date'),
        Index('idx_fitness_workout_type', 'workout_type'),
    )


class HealthMetric(Base):
    """Health metric model for daily wellness tracking."""
    __tablename__ = "health_metrics"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    date = Column(Date, nullable=False)
    weight_kg = Column(Float, nullable=True)
    steps = Column(Integer, nullable=True)
    water_intake_liters = Column(Float, nullable=True)
    sleep_hours = Column(Float, nullable=True)
    heart_rate_bpm = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="health_metrics")

    # Indexes
    __table_args__ = (
        Index('idx_health_user_date', 'user_id', 'date'),
        UniqueConstraint('user_id', 'date', name='unique_user_date'),
    )
