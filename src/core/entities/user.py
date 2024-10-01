# src/core/entities/user.py

from src.core.entities.base_entity import BaseEntity
from pydantic import BaseModel, Field, field_validator, model_validator
from bson import ObjectId
from typing import Optional

class ObjectIdStr(str):
    """Custom data type for handling ObjectId as a string."""

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value, field=None):
        """Validate that the value is an ObjectId and return it as a string."""
        if not isinstance(value, ObjectId):
            raise TypeError(f"Expected ObjectId, but got {type(value)} instead.")
        return str(value)

    @classmethod
    def __get_pydantic_json_schema__(cls, schema):
        """Modify the JSON schema to represent ObjectIdStr as a string."""
        schema.update(type="string")
        return schema

class User(BaseEntity):
    id: Optional[ObjectIdStr] = Field(None, alias="_id")
    name: str
    email: str
    age: int

    class Config:
        allow_population_by_field_name = True  # Allow alias fields to be populated
        arbitrary_types_allowed = True  # Allow custom types like ObjectIdStr

    @model_validator(mode='before')
    @classmethod
    def convert_object_id(cls, values):
        """Convert ObjectId to string if needed."""
        if "_id" in values and isinstance(values["_id"], ObjectId):
            values["id"] = str(values["_id"])
        return values
