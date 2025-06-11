import asyncio
import random
from datetime import datetime, timezone
from app.models import SensorData

async def generate_sensor_data(queue: asyncio.Queue):
    sensor_ids = ["sensor-1", "sensor-2", "sensor-3"]
    while True:
        data = SensorData(
            timestamp=datetime.now(timezone.utc),
            sensor_id=random.choice(sensor_ids),
            value=round(random.uniform(10, 100), 2)
        )
        await queue.put(data)
        await asyncio.sleep(0.01)
