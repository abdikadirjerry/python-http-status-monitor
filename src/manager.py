import uuid
from src.storage import load_services, save_services
from src.probe import check_endpoint

def add_service(name: str, url: str, category: str) -> dict:
    services = load_services()
    result = check_endpoint(url)
    new_service = {
        "id": f"srv-{uuid.uuid4().hex[:6]}",
        "name": name,
        "url": url,
        "category": category,
        "status": result["status"],
        "latency_ms": result["latency_ms"],
        "last_checked": result["last_checked"]
    }
    services.append(new_service)
    save_services(services)
    return new_service

def delete_service(service_id: str) -> bool:
    services = load_services()
    updated = [s for s in services if s["id"] != service_id]
    if len(updated) == len(services):
        return False
    save_services(updated)
    return True

def refresh_all_services() -> list[dict]:
    services = load_services()
    for srv in services:
        result = check_endpoint(srv["url"])
        srv["status"] = result["status"]
        srv["latency_ms"] = result["latency_ms"]
        srv["last_checked"] = result["last_checked"]
    save_services(services)
    return services