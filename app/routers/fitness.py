"""Fitness records routes."""
from datetime import date
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, FitnessRecord
from app.schemas import (
    FitnessRecordCreate,
    FitnessRecordUpdate,
    FitnessRecordResponse
)
from app.security import get_current_user

router = APIRouter(prefix="/fitness-records", tags=["Fitness Records"])


@router.get("", response_model=List[FitnessRecordResponse])
def list_fitness_records(
    start_date: Optional[date] = Query(None, description="Filter by start date"),
    end_date: Optional[date] = Query(None, description="Filter by end date"),
    workout_type: Optional[str] = Query(None, description="Filter by workout type"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum records to return"),
    offset: int = Query(0, ge=0, description="Number of records to skip"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List fitness records for the current user with optional filters."""
    query = db.query(FitnessRecord).filter(FitnessRecord.user_id == current_user.id)
    
    # Apply date filters
    if start_date:
        query = query.filter(FitnessRecord.date >= start_date)
    if end_date:
        query = query.filter(FitnessRecord.date <= end_date)
    
    # Apply workout type filter
    if workout_type:
        query = query.filter(FitnessRecord.workout_type == workout_type)
    
    # Order by date descending and apply pagination
    records = query.order_by(FitnessRecord.date.desc()).offset(offset).limit(limit).all()
    
    return records


@router.post("", response_model=FitnessRecordResponse, status_code=status.HTTP_201_CREATED)
def create_fitness_record(
    record_data: FitnessRecordCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new fitness record."""
    new_record = FitnessRecord(
        user_id=current_user.id,
        date=record_data.date,
        workout_type=record_data.workout_type,
        duration_minutes=record_data.duration_minutes,
        calories_burned=record_data.calories_burned,
        distance_km=record_data.distance_km,
        intensity_level=record_data.intensity_level,
        notes=record_data.notes
    )
    
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    
    return new_record


@router.get("/{record_id}", response_model=FitnessRecordResponse)
def get_fitness_record(
    record_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific fitness record by ID."""
    record = db.query(FitnessRecord).filter(FitnessRecord.id == record_id).first()
    
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "RESOURCE_NOT_FOUND", "message": "Fitness record not found"}
        )
    
    # Check ownership
    if record.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"code": "ACCESS_DENIED", "message": "You do not have access to this record"}
        )
    
    return record


@router.put("/{record_id}", response_model=FitnessRecordResponse)
def update_fitness_record(
    record_id: str,
    update_data: FitnessRecordUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a fitness record."""
    record = db.query(FitnessRecord).filter(FitnessRecord.id == record_id).first()
    
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "RESOURCE_NOT_FOUND", "message": "Fitness record not found"}
        )
    
    # Check ownership
    if record.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"code": "ACCESS_DENIED", "message": "You do not have access to this record"}
        )
    
    # Update fields
    update_dict = update_data.model_dump(exclude_unset=True)
    for field, value in update_dict.items():
        setattr(record, field, value)
    
    db.commit()
    db.refresh(record)
    
    return record


@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_fitness_record(
    record_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a fitness record."""
    record = db.query(FitnessRecord).filter(FitnessRecord.id == record_id).first()
    
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "RESOURCE_NOT_FOUND", "message": "Fitness record not found"}
        )
    
    # Check ownership
    if record.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"code": "ACCESS_DENIED", "message": "You do not have access to this record"}
        )
    
    db.delete(record)
    db.commit()
    
    return None
