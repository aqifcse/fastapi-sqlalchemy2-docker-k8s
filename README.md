# fastapi-sqlalchemy2-docker-k8s
Here's an example of how you can build a FastAPI application with SQLAlchemy 2.x for One-to-Many and Many-to-Many relationships, integrating Pydantic for validation, Alembic for migrations, Docker, and Kubernetes support. The application also includes Dependency Injection, Security &amp; Authentication, Asynchronous Support, and Middlewares.

command to run

```
docker-compose up --build
```

In another terminal
```
docker-compose exec web alembic revision --autogenerate -m "Initial migration"
docker-compose exec web alembic upgrade head
```
