# Microservice Boilerplate with FastAPI, MongoDB, and Dependency Injection

Welcome to the Microservice Boilerplate repository! This project is a robust and modular backend service built using **FastAPI**, **MongoDB**, and **Dependency Injector**. It is designed to help you quickly get started with building microservices by providing a well-structured and extendable codebase.

## Table of Contents
- [Features](#features)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Setup](#environment-setup)
- [Running the Application](#running-the-application)
  - [Local Development](#local-development)
  - [Using Docker](#using-docker)
- [Endpoints](#endpoints)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Features

- **FastAPI** framework for creating performant APIs.
- **MongoDB** integration using `motor` for asynchronous operations.
- **Dependency Injection** with `dependency-injector` for modular and maintainable code.
- **Request/Response Validation** using Pydantic models.
- **Custom Middleware** for request tracking (e.g., Request ID).
- **Unified Logging** configuration with support for JSON and file-based logging.
- **Structured Project Layout** following the Clean Architecture principles.
- **Dynamic Configuration** using environment variables with `dotenv`.

## Project Structure

src/ ├── core/ # Core business logic and use-cases │ ├── entities/ # Entity definitions │ ├── repositories/ # Repository interfaces and implementations │ ├── use_cases/ # Use-cases implementing business rules ├── dependencies/ # FastAPI dependencies │ ├── request_id_dependency.py # Dependency to extract request ID ├── infrastructure/ # Infrastructure-related code and configurations │ ├── db/ # Database clients and configurations │ │ └── mongo_client.py # MongoDB client for async operations │ ├── logging_config.py # Centralized logging configuration │ ├── di_container.py # Dependency Injection container │ └── response_interceptor.py # Custom response interceptors ├── interfaces/ # Interface adapters │ ├── api/ # API layer with FastAPI routers │ │ └── v1/ │ │ └── user_controller.py # User-related API endpoints ├── middleware/ # Custom middleware (e.g., Request ID Middleware) ├── services/ # Service layer to coordinate use-cases and repositories │ └── user_service.py # User service with business logic coordination └── main.py # Entry point for the FastAPI application


## Getting Started

### Prerequisites

Make sure you have the following installed on your system:

- Python 3.8 or higher
- MongoDB 4.0 or higher
- Docker (optional, for running via Docker)

### Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2. **Create a virtual environment and activate it:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Install MongoDB locally** or ensure a remote instance is accessible.

### Environment Setup

1. **Create a `.env` file** in the root of the project and set up the following environment variables:

    ```ini
    MONGO_URI=mongodb://localhost:27017
    DB_NAME=mydatabase
    DB_COLLECTION=users
    LOG_LEVEL=DEBUG
    ```

2. **Modify the `.env` file** according to your local or production configurations.

## Running the Application

### Local Development

1. **Start MongoDB server** if running locally:

    ```bash
    mongod
    ```

2. **Run the application:**

    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    ```

3. The API will be available at `http://127.0.0.1:8000`.

### Using Docker

1. **Build the Docker image:**

    ```bash
    docker build -t my-microservice .
    ```

2. **Run the Docker container:**

    ```bash
    docker run -p 8000:8000 --env-file .env my-microservice
    ```

## Endpoints

Here are some key endpoints provided by this boilerplate:

- `GET /api/v1/users/`: Retrieve all users.
- `POST /api/v1/users/`: Create a new user.
- `GET /api/v1/users/id/{user_id}`: Retrieve a user by ID.
- `GET /api/v1/users/email/{email}`: Retrieve a user by email.

### Sample Request to Create a User

```json
POST /api/v1/users/
{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "age": 30
}
```

### Response Format
```json
{
  "status": "success",
  "data": { ... },
  "message": "Operation completed successfully."
}
```

## Testing
To run the tests, make sure you have pytest installed:

```bash
pytest
```
