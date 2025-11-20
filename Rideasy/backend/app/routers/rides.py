from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from datetime import datetime, timedelta
from typing import List
import math

from app.database import get_db
from app.models import User, Ride, Location, RideStatus
from app.schemas import (
    RideCreate, RideResponse, RideUpdate, UserResponse
)
from app.dependencies import get_current_active_user
from app.routers.websocket import manager

router = APIRouter()

# Simple fare calculation based on distance
def calculate_fare(pickup_lat: float, pickup_lon: float, dest_lat: float, dest_lon: float) -> float:
    # Haversine formula for distance calculation
    R = 6371  # Earth radius in km
    lat1, lon1 = math.radians(pickup_lat), math.radians(pickup_lon)
    lat2, lon2 = math.radians(dest_lat), math.radians(dest_lon)
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    distance = R * c
    
    # Base fare + per km rate
    base_fare = 2.50
    per_km_rate = 1.50
    fare = base_fare + (distance * per_km_rate)
    
    return round(fare, 2)


@router.post("", response_model=RideResponse, status_code=status.HTTP_201_CREATED)
async def create_ride(
    ride_data: RideCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    # Check if user has an active ride
    result = await db.execute(
        select(Ride).where(
            and_(
                Ride.rider_id == current_user.id,
                Ride.status.in_([RideStatus.SEARCHING, RideStatus.MATCHED, RideStatus.DRIVER_ARRIVING, RideStatus.IN_PROGRESS])
            )
        )
    )
    active_ride = result.scalar_one_or_none()
    if active_ride:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already have an active ride"
        )
    
    # Create pickup location
    pickup_location = Location(
        name=ride_data.pickup_location.name,
        latitude=ride_data.pickup_location.latitude,
        longitude=ride_data.pickup_location.longitude
    )
    db.add(pickup_location)
    await db.flush()
    
    # Create destination location
    destination_location = Location(
        name=ride_data.destination_location.name,
        latitude=ride_data.destination_location.latitude,
        longitude=ride_data.destination_location.longitude
    )
    db.add(destination_location)
    await db.flush()
    
    # Calculate fare
    fare = calculate_fare(
        pickup_location.latitude,
        pickup_location.longitude,
        destination_location.latitude,
        destination_location.longitude
    )
    
    # Create ride
    new_ride = Ride(
        rider_id=current_user.id,
        pickup_location_id=pickup_location.id,
        destination_location_id=destination_location.id,
        status=RideStatus.SEARCHING,
        fare=fare
    )
    
    db.add(new_ride)
    await db.commit()
    await db.refresh(new_ride)
    await db.refresh(new_ride.pickup_location)
    await db.refresh(new_ride.destination_location)
    
    # Try to find available driver
    await match_driver(new_ride.id, db)
    
    # Refresh ride to get updated data
    await db.refresh(new_ride)
    await db.refresh(new_ride.rider)
    if new_ride.driver_id:
        await db.refresh(new_ride.driver)
    
    ride_response = await ride_to_response(new_ride, db)
    
    # Notify rider via WebSocket
    await manager.send_ride_update(current_user.id, ride_response)
    
    return ride_response


async def match_driver(ride_id: str, db: AsyncSession):
    """Match a ride with an available driver"""
    ride = await db.get(Ride, ride_id)
    if not ride or ride.status != RideStatus.SEARCHING:
        return
    
    # Find available drivers near pickup location
    result = await db.execute(
        select(User).where(
            and_(
                User.user_mode == "driver",
                User.is_online == True,
                User.id.notin_(
                    select(Ride.driver_id).where(
                        Ride.status.in_([RideStatus.MATCHED, RideStatus.DRIVER_ARRIVING, RideStatus.IN_PROGRESS])
                    )
                )
            )
        )
    )
    available_drivers = result.scalars().all()
    
    if not available_drivers:
        return
    
    # Simple matching: pick first available driver
    # In production, you'd want to match based on proximity
    driver = available_drivers[0]
    
    ride.driver_id = driver.id
    ride.status = RideStatus.MATCHED
    ride.estimated_arrival = datetime.utcnow() + timedelta(minutes=5)
    
    await db.commit()
    
    # Notify driver via WebSocket
    ride_response = await ride_to_response(ride, db)
    await manager.send_ride_update(driver.id, ride_response)


async def ride_to_response(ride: Ride, db: AsyncSession) -> RideResponse:
    """Convert Ride model to RideResponse schema"""
    await db.refresh(ride.pickup_location)
    await db.refresh(ride.destination_location)
    await db.refresh(ride.rider)
    
    response_data = {
        "id": ride.id,
        "rider_id": ride.rider_id,
        "driver_id": ride.driver_id,
        "pickup_location": {
            "id": ride.pickup_location.id,
            "name": ride.pickup_location.name,
            "latitude": ride.pickup_location.latitude,
            "longitude": ride.pickup_location.longitude,
            "created_at": ride.pickup_location.created_at
        },
        "destination_location": {
            "id": ride.destination_location.id,
            "name": ride.destination_location.name,
            "latitude": ride.destination_location.latitude,
            "longitude": ride.destination_location.longitude,
            "created_at": ride.destination_location.created_at
        },
        "status": ride.status,
        "fare": ride.fare,
        "estimated_arrival": ride.estimated_arrival,
        "started_at": ride.started_at,
        "completed_at": ride.completed_at,
        "created_at": ride.created_at,
        "updated_at": ride.updated_at,
        "rider_name": ride.rider.full_name or ride.rider.username,
        "driver_name": None,
        "rider_rating": ride.rider.rating,
        "driver_rating": None
    }
    
    if ride.driver_id:
        await db.refresh(ride.driver)
        response_data["driver_name"] = ride.driver.full_name or ride.driver.username
        response_data["driver_rating"] = ride.driver.rating
    
    return RideResponse(**response_data)


@router.get("", response_model=List[RideResponse])
async def get_rides(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
    status_filter: RideStatus = None
):
    if current_user.user_mode.value == "rider":
        query = select(Ride).where(Ride.rider_id == current_user.id)
    else:
        query = select(Ride).where(Ride.driver_id == current_user.id)
    
    if status_filter:
        query = query.where(Ride.status == status_filter)
    
    query = query.order_by(Ride.created_at.desc())
    result = await db.execute(query)
    rides = result.scalars().all()
    
    return [await ride_to_response(ride, db) for ride in rides]


@router.get("/available", response_model=List[RideResponse])
async def get_available_rides(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    if current_user.user_mode.value != "driver":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only drivers can view available rides"
        )
    
    if not current_user.is_online:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Driver must be online to view available rides"
        )
    
    # Get rides that are searching for a driver
    result = await db.execute(
        select(Ride).where(Ride.status == RideStatus.SEARCHING)
    )
    rides = result.scalars().all()
    
    return [await ride_to_response(ride, db) for ride in rides]


@router.get("/{ride_id}", response_model=RideResponse)
async def get_ride(
    ride_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    ride = await db.get(Ride, ride_id)
    if not ride:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ride not found"
        )
    
    # Check if user has access to this ride
    if ride.rider_id != current_user.id and ride.driver_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this ride"
        )
    
    return await ride_to_response(ride, db)


@router.put("/{ride_id}", response_model=RideResponse)
async def update_ride(
    ride_id: str,
    ride_update: RideUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    ride = await db.get(Ride, ride_id)
    if not ride:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ride not found"
        )
    
    # Check permissions
    if ride.rider_id != current_user.id and ride.driver_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this ride"
        )
    
    # Update ride
    if ride_update.status:
        ride.status = ride_update.status
        if ride_update.status == RideStatus.IN_PROGRESS and not ride.started_at:
            ride.started_at = datetime.utcnow()
        elif ride_update.status == RideStatus.COMPLETED and not ride.completed_at:
            ride.completed_at = datetime.utcnow()
    
    if ride_update.driver_id:
        ride.driver_id = ride_update.driver_id
    if ride_update.fare is not None:
        ride.fare = ride_update.fare
    if ride_update.estimated_arrival:
        ride.estimated_arrival = ride_update.estimated_arrival
    
    await db.commit()
    await db.refresh(ride)
    
    ride_response = await ride_to_response(ride, db)
    
    # Notify both rider and driver via WebSocket
    await manager.send_ride_update(ride.rider_id, ride_response)
    if ride.driver_id:
        await manager.send_ride_update(ride.driver_id, ride_response)
    
    return ride_response


@router.post("/{ride_id}/accept", response_model=RideResponse)
async def accept_ride(
    ride_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    if current_user.user_mode.value != "driver":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only drivers can accept rides"
        )
    
    if not current_user.is_online:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Driver must be online to accept rides"
        )
    
    ride = await db.get(Ride, ride_id)
    if not ride:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ride not found"
        )
    
    if ride.status != RideStatus.SEARCHING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ride is not available for acceptance"
        )
    
    # Check if driver already has an active ride
    result = await db.execute(
        select(Ride).where(
            and_(
                Ride.driver_id == current_user.id,
                Ride.status.in_([RideStatus.MATCHED, RideStatus.DRIVER_ARRIVING, RideStatus.IN_PROGRESS])
            )
        )
    )
    active_ride = result.scalar_one_or_none()
    if active_ride:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already have an active ride"
        )
    
    ride.driver_id = current_user.id
    ride.status = RideStatus.MATCHED
    ride.estimated_arrival = datetime.utcnow() + timedelta(minutes=5)
    
    await db.commit()
    await db.refresh(ride)
    
    ride_response = await ride_to_response(ride, db)
    
    # Notify both rider and driver via WebSocket
    await manager.send_ride_update(ride.rider_id, ride_response)
    await manager.send_ride_update(current_user.id, ride_response)
    
    return ride_response


@router.post("/{ride_id}/cancel", response_model=RideResponse)
async def cancel_ride(
    ride_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    ride = await db.get(Ride, ride_id)
    if not ride:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ride not found"
        )
    
    # Check permissions
    if ride.rider_id != current_user.id and ride.driver_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to cancel this ride"
        )
    
    if ride.status in [RideStatus.COMPLETED, RideStatus.CANCELLED]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot cancel a completed or already cancelled ride"
        )
    
    ride.status = RideStatus.CANCELLED
    
    await db.commit()
    await db.refresh(ride)
    
    ride_response = await ride_to_response(ride, db)
    
    # Notify both rider and driver via WebSocket
    await manager.send_ride_update(ride.rider_id, ride_response)
    if ride.driver_id:
        await manager.send_ride_update(ride.driver_id, ride_response)
    
    return ride_response

