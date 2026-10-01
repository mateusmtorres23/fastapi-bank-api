# FastAPI Bank API

A banking API developed as a learning project to practice backend development with FastAPI and a more structured application architecture.

The project focuses on separation of responsibilities, asynchronous database operations, authentication, and automated testing.

## Features

- User registration and authentication
- JWT-based authentication
- Bank account management
- Deposits
- Withdrawals
- Transfers between accounts

## Technologies

- Python
- FastAPI
- SQLAlchemy
- SQLite / aiosqlite
- JWT
- Pytest
- HTTPX

## Architecture

The application is organized into separate modules for:

- `models` — database entities
- `schemas` — request and response models
- `routers` — API endpoints
- `services` — business logic
- `security` — authentication and JWT handling
- `db` — database configuration

## Tests

The project includes automated tests covering different parts of the application, including authentication, models, schemas, routers, and services.
