# ND Real-Time Sensor Data Pipeline

This project is a minimal real-time data processing pipeline and API using FastAPI, asyncio, and pandas.

## Features

- Simulates real-time sensor data streams
- Processes and analyzes data in real time
- Exposes a FastAPI web API for results and health checks
- Includes basic automated tests

## Requirements

- Python 3.10+
- (Recommended) Use a virtual environment

## Setup

1. **Install dependencies:**

   If using `uv` (recommended):

   ```bash
   uv pip install -r pyproject.toml
   ```

   Or, with pip (NOTE: I used UV. Results might vary here):

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install .
   ```

2. **Run the app:**

   ```bash
   uv run uvicorn app.main:app --reload
   ```

   The API will be available at http://localhost:8000

3. **API Docs:**

   - Swagger UI: http://localhost:8000/docs
   - OpenAPI JSON: http://localhost:8000/openapi.json

4. **Run tests:**

   ```bash
   pytest
   ```

## Endpoints

- `GET /health` — Health check
- `GET /results/latest` — Latest processed sensor data
- `POST /trigger` — Manually trigger data processing
- `GET /results/query` — Query results by time or sensor ID

---

For more details, see the code in the `app/` and `tests/` directories.

---

## Improvements for the future

- Database Integration: Store sensor data in a real database (SQLite, PostgreSQL, etc.) for persistence and scalability.
- Allow historical queries, not just the latest buffer.
- Better error handling: Add try/catch blocks around data ingestion, processing, and API endpoints for graceful failures.
- Input validation for all incoming data.
- More comprehensive tests: Add tests for edge cases, error conditions, and data validation.
- Logging: Use Python's logging module instead of print statements for better log management.
- Dockerization: Add a Dockerfile for easy deployment and reproducibility.
