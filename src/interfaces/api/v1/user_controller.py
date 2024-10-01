# src/interfaces/api/v1/user_controller.py

from fastapi import APIRouter, Depends, HTTPException
from typing import List
from src.core.entities.user import User
from src.core.schemas.user_schema import UserCreateRequest, UserUpdateRequest
from src.services.user_service import UserService
from dependency_injector.wiring import inject, Provide
from src.infrastructure.di_container import Container
import logging
# Create a FastAPI router for user-related endpoints
router = APIRouter()

# Use @inject decorator to inject the UserService dependency
@router.post("/users/", response_model=User)
@inject
async def create_user(
    user_request: UserCreateRequest,
    service: UserService = Depends(Provide[Container.user_service])  # Use Provide to inject UserService from Container
):
    """Create a new user."""
    try:
        # Pass validated data to the service
        created_user = await service.create_user(
            name=user_request.name, 
            email=user_request.email, 
            age=user_request.age
        )
        return created_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/users/", response_model=List[User])
@inject
async def get_all_users(
    service: UserService = Depends(Provide[Container.user_service])  # Use Provide to inject UserService from Container
):
    """Get all users."""
    return await service.get_all_users()

@router.get("/users/id/{user_id}", response_model=User)
@inject
async def get_user_by_id(user_id: str, service: UserService = Depends(Provide[Container.user_service])):
    """Get a user by ID."""
    user = await service.find_user_by_id(user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/users/email/{email}", response_model=User)
@inject
async def get_user_by_email(email: str, service: UserService = Depends(Provide[Container.user_service])):
    """Get a user by email."""
    user = await service.find_user_by_email(email=email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user