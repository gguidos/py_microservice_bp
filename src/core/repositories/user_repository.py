from datetime import datetime
from typing import Dict, Any, List
from src.infrastructure.db.mongo_client import MongoDBClient
from bson import ObjectId

class UserRepository:
    """Repository for performing CRUD operations on the users collection."""

    def __init__(self, client: MongoDBClient):
        self.client = client

    async def create(self, user_data: Dict[str, Any]) -> str:
        """Create a new user."""
        # Remove _id if it is None or not set
        if "_id" in user_data and user_data["_id"] is None:
            del user_data["_id"]
        user_data["created"] = user_data.get("created", datetime.utcnow())
        user_data["modified"] = user_data.get("modified", datetime.utcnow())
        user_id = await self.client.insert_one(user_data)
        return str(user_id)

    async def find_all(self) -> List[Dict[str, Any]]:
        """Retrieve all users."""
        return await self.client.find({})

    async def find(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Retrieve users that match the specified query.

        Args:
            query (Dict[str, Any]): A dictionary representing the query to be executed.

        Returns:
            List[Dict[str, Any]]: A list of user documents that match the query.
        """
        return await self.client.find(query)

    async def update(self, user_id: str, user_data: Dict[str, Any]) -> bool:
        """Update a user by ID."""
        query = {"_id": ObjectId(user_id)}
        updated_data = {"$set": user_data}
        updated_data["modified"] = datetime.utcnow()  
        result = await self.client.update_one(query, updated_data)
        return result.modified_count > 0

    async def delete(self, user_id: str) -> bool:
        """Delete a user by ID."""
        query = {"_id": ObjectId(user_id)}
        result = await self.client.delete_one(query)
        return result.deleted_count > 0
