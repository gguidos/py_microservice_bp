from typing import List, Optional
from src.core.entities.user import User
from src.core.repositories.user_repository import UserRepository
from src.core.use_cases.create_user import CreateUser
from src.core.use_cases.get_all_users import GetAllUsers
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)

# Conversion functions between Pydantic models and MongoDB documents
def user_to_mongo_dict(user: User) -> dict:
    """Convert a Pydantic User model to a MongoDB dictionary format."""
    return user.dict(by_alias=True, exclude_none=True)

def mongo_dict_to_user(mongo_dict: dict) -> User:
    """Convert a MongoDB dictionary to a Pydantic User model."""
    # Convert ObjectId to string for the _id field
    if "_id" in mongo_dict and isinstance(mongo_dict["_id"], ObjectId):
        mongo_dict["_id"] = str(mongo_dict["_id"])
    return User(**mongo_dict)

class UserService:
    """Service layer for managing users."""

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        self.create_user_use_case = CreateUser(user_repository)
        self.get_all_users_use_case = GetAllUsers(user_repository)

    async def create_user(self, name: str, email: str, age: int) -> User:
        """Create a new user using the create_user use-case."""
        logger.info(f"Creating user with email: {email}")
        # Check if a user with the same email already exists.
        existing_users = await self.find_user_by_email(email=email)
        if existing_users:
            logger.error(f"User with email: {email} already exists")
            raise ValueError(f"User with email {email} already exists.")
        try:
            logger.info(f"User with email {email} created successfully")
            return await self.create_user_use_case.execute(name=name, email=email, age=age)
        except Exception as e:
            logger.error(f"Failed to create user with email {email}: {e}")

    async def get_all_users(self) -> List[User]:
        """Get all users using the get_all_users use-case."""
        return await self.get_all_users_use_case.execute()

    async def find_user_by_id(self, user_id: str) -> Optional[User]:
        """Find a user by ID."""
        users = await self.user_repository.find(query={"_id": ObjectId(user_id)})
        if users:
            return User(**users[0])
        return None

    async def find_user_by_email(self, email: str) -> Optional[User]:
        """Find a user by email."""
        users = await self.user_repository.find(query={"email": email})
        if users:
            return User(**users[0])
        return None

    async def find_users_by_age(self, age: int) -> List[User]:
        """Find all users by age."""
        user_data_list = await self.user_repository.find(query={"age": age})
        return [User(**data) for data in user_data_list]

