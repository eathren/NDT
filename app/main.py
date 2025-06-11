from fastapi import FastAPI, Query
from typing import Optional
from datetime import datetime
from app.store import results
from app.ingest import generate_sensor_data
from app.processor import analyze, data_buffer
import asyncio

app = FastAPI()
data_queue = asyncio.Queue()

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(generate_sensor_data(data_queue))
    asyncio.create_task(ingestion_loop())


async def ingestion_loop():
    while True:
        batch = []
        while not data_queue.empty():
            batch.append(await data_queue.get())
        if batch:
            data_buffer.extend(batch)
            analyze(list(data_buffer)[-20:])
        await asyncio.sleep(0.2)


@app.get("/results/latest")
async def get_latest():
    latest = results.get("latest")
    # Debugging output
    print("/results/latest called, returning:", latest)
    if latest is None:
        return {"message": "No data yet"}
    return latest

@app.get("/health")
async def health():
    """Health/sanity check."""
    return {"status": "ok"}

@app.post("/trigger")
async def trigger_data_load():
    """Manually trigger a single data ingestion and processing cycle."""
    batch = []
    while not data_queue.empty():
        batch.append(await data_queue.get())
    if batch:
        data_buffer.extend(batch)
        analyze(list(data_buffer)[-50:])
        return {"status": "triggered", "batch_size": len(batch)}
    return {"status": "no_data"}

@app.get("/results/query")
async def query_results(
    start: Optional[datetime] = Query(None, description="Start timestamp (ISO format)"),
    end: Optional[datetime] = Query(None, description="End timestamp (ISO format)"),
    sensor_id: Optional[str] = Query(None, description="Sensor ID to filter")
):
    data = results.get("latest", [])
    filtered = []
    for row in data:
        ts = row.get("timestamp")
        if isinstance(ts, str):
            ts = datetime.fromisoformat(ts)
        if start and ts < start:
            continue
        if end and ts > end:
            continue
        if sensor_id and row.get("sensor_id") != sensor_id:
            continue
        filtered.append(row)
    return filtered