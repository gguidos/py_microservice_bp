from fastapi import Depends
from src.services.user_service import UserService
from src.infrastructure.di_container import Container
from src.dependencies.request_id_dependency import get_request_id

async def get_user_service(
    request_id: str = Depends(get_request_id),  # First, get the request ID
    container: Container = Depends(lambda: Container())  # Get an instance of the DI container
) -> UserService:
    """Create a UserService instance with the provided request_id."""
    # Use the container to create a UserService instance with request_id
    return container.user_service(request_id=request_id)
