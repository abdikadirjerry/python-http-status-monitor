def calculate_metrics(services: list[dict]) -> dict:
    total = len(services)
    if total == 0:
        return {"total": 0, "up": 0, "degraded": 0, "down": 0, "avg_latency": 0, "uptime_pct": 100.0}

    up = sum(1 for s in services if s["status"] == "UP")
    degraded = sum(1 for s in services if s["status"] == "DEGRADED")
    down = sum(1 for s in services if s["status"] == "DOWN")

    active_latencies = [s["latency_ms"] for s in services if s["latency_ms"] > 0]
    avg_latency = int(sum(active_latencies) / len(active_latencies)) if active_latencies else 0
    uptime_pct = round(((up + degraded) / total) * 100, 1)

    return {
        "total": total,
        "up": up,
        "degraded": degraded,
        "down": down,
        "avg_latency": avg_latency,
        "uptime_pct": uptime_pct
    }