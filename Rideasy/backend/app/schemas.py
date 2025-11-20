from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from app.models import UserMode, RideStatus


# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    user_mode: UserMode = UserMode.RIDER


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(UserBase):
    id: str
    rating: float
    is_online: bool
    current_latitude: Optional[float] = None
    current_longitude: Optional[float] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse


# Location Schemas
class LocationBase(BaseModel):
    name: str
    latitude: float
    longitude: float


class LocationCreate(LocationBase):
    pass


class LocationResponse(LocationBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True


# Ride Schemas
class RideBase(BaseModel):
    pickup_location: LocationCreate
    destination_location: LocationCreate


class RideCreate(RideBase):
    pass


class RideResponse(BaseModel):
    id: str
    rider_id: str
    driver_id: Optional[str] = None
    pickup_location: LocationResponse
    destination_location: LocationResponse
    status: RideStatus
    fare: Optional[float] = None
    estimated_arrival: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    rider_name: Optional[str] = None
    driver_name: Optional[str] = None
    rider_rating: Optional[float] = None
    driver_rating: Optional[float] = None

    class Config:
        from_attributes = True


class RideUpdate(BaseModel):
    status: Optional[RideStatus] = None
    driver_id: Optional[str] = None
    fare: Optional[float] = None
    estimated_arrival: Optional[datetime] = None


class DriverAvailabilityUpdate(BaseModel):
    is_online: bool
    latitude: Optional[float] = None
    longitude: Optional[float] = None


# WebSocket Message Schemas
class WebSocketMessage(BaseModel):
    type: str
    data: dict


class RideStatusUpdate(BaseModel):
    ride_id: str
    status: RideStatus
    driver_id: Optional[str] = None
    estimated_arrival: Optional[datetime] = None

