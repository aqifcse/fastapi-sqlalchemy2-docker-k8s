import asyncio
from fastapi import FastAPI
from app.routers import router  # Import router instead of app
from app.database import engine, Base

# Define FastAPI app here
app = FastAPI()

# Include your routers
app.include_router(router)

async def create_db():
    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)

async def main():
    await create_db()

@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    asyncio.run(main())

