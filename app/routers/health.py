"""Health metrics routes."""
from datetime import date
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.models import User, HealthMetric
from app.schemas import (
    HealthMetricCreate,
    HealthMetricUpdate,
    HealthMetricResponse
)
from app.security import get_current_user

router = APIRouter(prefix="/health-metrics", tags=["Health Metrics"])


@router.get("", response_model=List[HealthMetricResponse])
def list_health_metrics(
    start_date: Optional[date] = Query(None, description="Filter by start date"),
    end_date: Optional[date] = Query(None, description="Filter by end date"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum records to return"),
    offset: int = Query(0, ge=0, description="Number of records to skip"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List health metrics for the current user with optional filters."""
    query = db.query(HealthMetric).filter(HealthMetric.user_id == current_user.id)
    
    # Apply date filters
    if start_date:
        query = query.filter(HealthMetric.date >= start_date)
    if end_date:
        query = query.filter(HealthMetric.date <= end_date)
    
    # Order by date descending and apply pagination
    metrics = query.order_by(HealthMetric.date.desc()).offset(offset).limit(limit).all()
    
    return metrics


@router.post("", response_model=HealthMetricResponse, status_code=status.HTTP_201_CREATED)
def create_health_metric(
    metric_data: HealthMetricCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new health metric."""
    # Check for existing metric on same date
    existing = db.query(HealthMetric).filter(
        HealthMetric.user_id == current_user.id,
        HealthMetric.date == metric_data.date
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"code": "DUPLICATE_DATE", "message": "Health metric already exists for this date"}
        )
    
    new_metric = HealthMetric(
        user_id=current_user.id,
        date=metric_data.date,
        weight_kg=metric_data.weight_kg,
        steps=metric_data.steps,
        water_intake_liters=metric_data.water_intake_liters,
        sleep_hours=metric_data.sleep_hours,
        heart_rate_bpm=metric_data.heart_rate_bpm
    )
    
    try:
        db.add(new_metric)
        db.commit()
        db.refresh(new_metric)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"code": "DUPLICATE_DATE", "message": "Health metric already exists for this date"}
        )
    
    return new_metric


@router.get("/{metric_id}", response_model=HealthMetricResponse)
def get_health_metric(
    metric_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific health metric by ID."""
    metric = db.query(HealthMetric).filter(HealthMetric.id == metric_id).first()
    
    if not metric:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "RESOURCE_NOT_FOUND", "message": "Health metric not found"}
        )
    
    # Check ownership
    if metric.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"code": "ACCESS_DENIED", "message": "You do not have access to this metric"}
        )
    
    return metric


@router.put("/{metric_id}", response_model=HealthMetricResponse)
def update_health_metric(
    metric_id: str,
    update_data: HealthMetricUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a health metric."""
    metric = db.query(HealthMetric).filter(HealthMetric.id == metric_id).first()
    
    if not metric:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "RESOURCE_NOT_FOUND", "message": "Health metric not found"}
        )
    
    # Check ownership
    if metric.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"code": "ACCESS_DENIED", "message": "You do not have access to this metric"}
        )
    
    # Update fields
    update_dict = update_data.model_dump(exclude_unset=True)
    for field, value in update_dict.items():
        setattr(metric, field, value)
    
    db.commit()
    db.refresh(metric)
    
    return metric


@router.delete("/{metric_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_health_metric(
    metric_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a health metric."""
    metric = db.query(HealthMetric).filter(HealthMetric.id == metric_id).first()
    
    if not metric:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "RESOURCE_NOT_FOUND", "message": "Health metric not found"}
        )
    
    # Check ownership
    if metric.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"code": "ACCESS_DENIED", "message": "You do not have access to this metric"}
        )
    
    db.delete(metric)
    db.commit()
    
    return None
