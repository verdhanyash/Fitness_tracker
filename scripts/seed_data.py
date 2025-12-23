"""Seed database with sample data (50+ records)."""
import sys
import os
from datetime import date, timedelta
import random

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models import User, FitnessRecord, HealthMetric
from app.security import hash_password


# Sample data
WORKOUT_TYPES = ["running", "cycling", "swimming", "weightlifting", "yoga", "hiit", "walking"]

WORKOUT_NOTES = [
    "Great session today!",
    "Felt a bit tired but pushed through",
    "Personal best!",
    "Recovery workout",
    "Morning session",
    "Evening workout",
    "Outdoor activity",
    None
]


def create_demo_user(db):
    """Create a demo user for testing."""
    existing = db.query(User).filter(User.username == "demo").first()
    if existing:
        print("Demo user already exists")
        return existing
    
    demo_user = User(
        username="demo",
        email="demo@example.com",
        password_hash=hash_password("demo123")
    )
    db.add(demo_user)
    db.commit()
    db.refresh(demo_user)
    print(f"Created demo user: username='demo', password='demo123'")
    return demo_user


def generate_fitness_records(user_id, num_records=30):
    """Generate sample fitness records."""
    records = []
    base_date = date.today() - timedelta(days=60)
    
    for i in range(num_records):
        record_date = base_date + timedelta(days=random.randint(0, 60))
        workout_type = random.choice(WORKOUT_TYPES)
        
        # Generate realistic values based on workout type
        if workout_type == "running":
            duration = random.randint(20, 60)
            calories = duration * random.randint(10, 14)
            distance = round(random.uniform(3, 12), 2)
        elif workout_type == "cycling":
            duration = random.randint(30, 90)
            calories = duration * random.randint(8, 12)
            distance = round(random.uniform(10, 40), 2)
        elif workout_type == "swimming":
            duration = random.randint(20, 45)
            calories = duration * random.randint(9, 13)
            distance = round(random.uniform(0.5, 2), 2)
        elif workout_type == "weightlifting":
            duration = random.randint(30, 75)
            calories = duration * random.randint(5, 8)
            distance = None
        elif workout_type == "yoga":
            duration = random.randint(30, 60)
            calories = duration * random.randint(3, 5)
            distance = None
        elif workout_type == "hiit":
            duration = random.randint(15, 35)
            calories = duration * random.randint(12, 18)
            distance = None
        else:  # walking
            duration = random.randint(20, 60)
            calories = duration * random.randint(4, 6)
            distance = round(random.uniform(2, 6), 2)
        
        records.append(FitnessRecord(
            user_id=user_id,
            date=record_date,
            workout_type=workout_type,
            duration_minutes=duration,
            calories_burned=calories,
            distance_km=distance,
            intensity_level=random.choice(["low", "medium", "high"]),
            notes=random.choice(WORKOUT_NOTES)
        ))
    
    return records


def generate_health_metrics(user_id, num_days=30):
    """Generate sample health metrics (one per day)."""
    metrics = []
    base_date = date.today() - timedelta(days=num_days)
    base_weight = random.uniform(65, 85)
    
    for i in range(num_days):
        metric_date = base_date + timedelta(days=i)
        # Simulate gradual weight change
        weight = round(base_weight + random.uniform(-0.5, 0.3) * (i / 10), 1)
        
        metrics.append(HealthMetric(
            user_id=user_id,
            date=metric_date,
            weight_kg=weight,
            steps=random.randint(3000, 15000),
            water_intake_liters=round(random.uniform(1.5, 3.5), 1),
            sleep_hours=round(random.uniform(5.5, 9), 1),
            heart_rate_bpm=random.randint(55, 85)
        ))
    
    return metrics


def seed_database():
    """Seed the database with sample data."""
    db = SessionLocal()
    
    try:
        # Create demo user
        demo_user = create_demo_user(db)
        
        # Check if data already exists
        existing_fitness = db.query(FitnessRecord).filter(
            FitnessRecord.user_id == demo_user.id
        ).count()
        
        existing_health = db.query(HealthMetric).filter(
            HealthMetric.user_id == demo_user.id
        ).count()
        
        if existing_fitness > 0 or existing_health > 0:
            print(f"Data already exists: {existing_fitness} fitness records, {existing_health} health metrics")
            print("Skipping seed to avoid duplicates. Delete existing data to re-seed.")
            return
        
        # Generate and insert fitness records (30 records)
        print("Generating fitness records...")
        fitness_records = generate_fitness_records(demo_user.id, num_records=30)
        db.add_all(fitness_records)
        db.commit()
        print(f"Created {len(fitness_records)} fitness records")
        
        # Generate and insert health metrics (30 days)
        print("Generating health metrics...")
        health_metrics = generate_health_metrics(demo_user.id, num_days=30)
        db.add_all(health_metrics)
        db.commit()
        print(f"Created {len(health_metrics)} health metrics")
        
        total = len(fitness_records) + len(health_metrics)
        print(f"\nTotal records created: {total}")
        print("Seed completed successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
