import pandas as pd
from collections import deque
from app.models import SensorData
from app.store import results
from concurrent.futures import ProcessPoolExecutor
import asyncio
import math

data_buffer = deque(maxlen=100)

def analyze(data: list[SensorData], use_process: bool = False):
    def _analyze_inner(data):
        df = pd.DataFrame([d.dict() for d in data])
        if df.empty:
            return []
        pivot = df.pivot_table(index="timestamp", columns="sensor_id", values="value")
        melted = pivot.reset_index().melt(id_vars=["timestamp"], var_name="sensor_id", value_name="value")
        melted["rolling_avg"] = melted.groupby("sensor_id")["value"].transform(
            lambda x: x.rolling(5, min_periods=1).mean()
        )
        # Replace inf, -inf, NaN with None for JSON serialization
        records = melted.tail(10).to_dict(orient="records")
        for row in records:
            for k, v in row.items():
                if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
                    row[k] = None
            # Ensure sensor_id is a string or None
            if 'sensor_id' in row and not (isinstance(row['sensor_id'], str) or row['sensor_id'] is None):
                row['sensor_id'] = str(row['sensor_id']) if row['sensor_id'] is not None else None
        return records

    if use_process:
        loop = asyncio.get_event_loop()
        with ProcessPoolExecutor() as pool:
            result = loop.run_in_executor(pool, _analyze_inner, data)
            results["latest"] = loop.run_until_complete(result)
    else:
        results["latest"] = _analyze_inner(data)
