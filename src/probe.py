import time
import urllib.request
import urllib.error
from datetime import datetime

def check_endpoint(url: str, timeout: int = 4) -> dict:
    start = time.perf_counter()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "PulseMonitor/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as response:
            code = response.getcode()
            latency = int((time.perf_counter() - start) * 1000)
            status = "DEGRADED" if latency > 800 else "UP"
            return {
                "status": status,
                "http_code": code,
                "latency_ms": latency,
                "last_checked": timestamp
            }
    except urllib.error.HTTPError as e:
        latency = int((time.perf_counter() - start) * 1000)
        return {
            "status": "DOWN",
            "http_code": e.code,
            "latency_ms": latency,
            "last_checked": timestamp
        }
    except Exception:
        return {
            "status": "DOWN",
            "http_code": 0,
            "latency_ms": 0,
            "last_checked": timestamp
        }