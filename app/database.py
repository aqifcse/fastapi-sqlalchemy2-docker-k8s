from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Define the base
Base = declarative_base()

# Create an asynchronous engine
engine = create_async_engine(
    "postgresql+asyncpg://aqif:p@db:5432/fastapi", echo=True
)

# Create an asynchronous session
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# Create all tables in the database (should be used cautiously in production)
async def init_db():
    # Import models to ensure they are registered with Base
    async with engine.begin() as conn:
        # Create tables
        await conn.run_sync(Base.metadata.create_all)


# Utility function to get a session
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
