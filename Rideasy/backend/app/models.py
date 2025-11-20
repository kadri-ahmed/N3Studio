from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Enum as SQLEnum, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum

from app.database import Base


class UserMode(str, enum.Enum):
    RIDER = "rider"
    DRIVER = "driver"


class RideStatus(str, enum.Enum):
    SEARCHING = "searching"
    MATCHED = "matched"
    DRIVER_ARRIVING = "driverArriving"
    IN_PROGRESS = "inProgress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    user_mode = Column(SQLEnum(UserMode), default=UserMode.RIDER)
    rating = Column(Float, default=0.0)
    is_online = Column(Boolean, default=False)
    current_latitude = Column(Float, nullable=True)
    current_longitude = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    rides_as_rider = relationship("Ride", foreign_keys="Ride.rider_id", back_populates="rider")
    rides_as_driver = relationship("Ride", foreign_keys="Ride.driver_id", back_populates="driver")


class Location(Base):
    __tablename__ = "locations"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Ride(Base):
    __tablename__ = "rides"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    rider_id = Column(String, ForeignKey("users.id"), nullable=False)
    driver_id = Column(String, ForeignKey("users.id"), nullable=True)
    pickup_location_id = Column(String, ForeignKey("locations.id"), nullable=False)
    destination_location_id = Column(String, ForeignKey("locations.id"), nullable=False)
    status = Column(SQLEnum(RideStatus), default=RideStatus.SEARCHING)
    fare = Column(Float, nullable=True)
    estimated_arrival = Column(DateTime, nullable=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    rider = relationship("User", foreign_keys=[rider_id], back_populates="rides_as_rider")
    driver = relationship("User", foreign_keys=[driver_id], back_populates="rides_as_driver")
    pickup_location = relationship("Location", foreign_keys=[pickup_location_id])
    destination_location = relationship("Location", foreign_keys=[destination_location_id])

