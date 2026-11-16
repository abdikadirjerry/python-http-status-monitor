import json
from pathlib import Path

DATA_FILE = Path("data/services.json")

def load_services() -> list[dict]:
    if not DATA_FILE.exists():
        return []
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))

def save_services(services: list[dict]) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(json.dumps(services, indent=2), encoding="utf-8")