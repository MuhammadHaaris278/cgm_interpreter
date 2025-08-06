import json
import uuid
from pathlib import Path
from datetime import datetime

def generate_id(prefix: str = "") -> str:
    return f"{prefix}_{uuid.uuid4()}"

def save_json(data: dict, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def load_json(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def timestamp_now() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
