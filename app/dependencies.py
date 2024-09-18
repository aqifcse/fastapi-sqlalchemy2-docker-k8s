from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://aqif:p@db:5432/fastapi"

# Async engine
engine = create_async_engine(DATABASE_URL, future=True, echo=True)

# Async session local
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


# Dependency injection to get database session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
