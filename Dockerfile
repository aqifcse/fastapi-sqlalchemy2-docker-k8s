FROM python:3.10-slim

# Install dependencies
RUN pip install --no-cache-dir alembic asyncpg

# Copy Alembic configuration and migration scripts
COPY alembic.ini /app/alembic.ini
COPY alembic /app/alembic

WORKDIR /app

# Copy other dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Default command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
