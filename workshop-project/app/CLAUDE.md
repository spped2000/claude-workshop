# App Layer — Component Context

- main.py: FastAPI entry point, middleware registration, health check
- routers/users.py: All user CRUD routes — new feature routes go here
- models.py: Pydantic v2 request/response models, use Field() for validation
- database.py: In-memory dict store — never import SQLAlchemy
