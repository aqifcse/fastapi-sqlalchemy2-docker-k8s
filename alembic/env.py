import asyncio
from logging.config import fileConfig
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context
from app.database import Base

# Load Alembic configuration
config = context.config
fileConfig(config.config_file_name)

# Set up SQLAlchemy database URL
DATABASE_URL = "postgresql+asyncpg://aqif:p@db:5432/fastapi"

# Create SQLAlchemy engine
engine = create_async_engine(DATABASE_URL, echo=True)


# Async migration runner
async def async_run_migrations():
    async with engine.begin() as conn:
        # Apply migrations
        await conn.run_sync(Base.metadata.create_all)


# Run migrations
def run_migrations_online():
    asyncio.run(async_run_migrations())


# Call this function in your Alembic configuration
if context.is_offline_mode():
    context.configure(url=DATABASE_URL, target_metadata=Base.metadata)
else:
    run_migrations_online()
