# main.py

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from src.infrastructure.request_id_middleware import RequestIDMiddleware
from src.infrastructure.logging.logging_middleware import LoggingMiddleware
from src.infrastructure.response_interceptor import ResponseFormatMiddleware
from contextlib import asynccontextmanager
from src.infrastructure.di_container import Container
from src.infrastructure.logging.logging_config import setup_logging
from src.interfaces.api.v1.user_controller import router as user_router
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

# Setup logging configuration
setup_logging()

# Initialize the logger
logger = logging.getLogger(__name__)

# Create the FastAPI app
app = FastAPI(
    title="User Management API",
    description="API for managing users in the application",
    version="1.0.0"
)

app.add_middleware(LoggingMiddleware)
# Register the middleware to intercept all responses
app.add_middleware(ResponseFormatMiddleware)

# Initialize the DI container
container = Container()

# Set configuration values using environment variables
container.config.db_uri.from_env("MONGO_URI")  # MongoDB URI (e.g., "mongodb://localhost:27017")
container.config.db_name.from_env("DB_NAME")   # Database name (e.g., "mydatabase")
container.config.db_collection.from_env("DB_COLLECTION")  # Collection name (e.g., "users")

# Initialize resources to ensure configuration values are fully propagated
container.init_resources()

# Wire the container to the modules that use the dependencies
container.wire(modules=["src.interfaces.api.v1.user_controller"])  # Wire the user controller

# Set the DI container to the app's state (optional if needed for accessing container)
app.container = container

# Include the user router with dependency injection configured
app.include_router(user_router, prefix="/api/v1", tags=["users"])

# Use an async context manager for lifespan events instead of on_event
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event manager to handle startup and shutdown events."""
    # Startup event to connect to MongoDB when the application starts
    mongo_client = container.mongo_client()
    await mongo_client.connect()
    logger.info("MongoDB client connected during startup.")

    # Verify that the collection is set correctly
    assert mongo_client.collection is not None, "MongoDB collection is not set during startup"

    # Yield control to allow handling requests
    yield

    # Shutdown event to disconnect from MongoDB when the application shuts down
    await mongo_client.disconnect()
    logger.info("MongoDB client disconnected during shutdown.")

# Set lifespan event handler for the FastAPI application
app.router.lifespan_context = lifespan

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
