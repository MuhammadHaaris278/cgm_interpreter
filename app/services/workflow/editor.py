import json
import uuid
from datetime import datetime
from pathlib import Path
from app.config.loader import Config

config = Config()
SAVE_DIR = config.output_dir

def save_interpretation(
    patient_id: str,
    summary: dict,
    interpretation_text: str,
    provider_id: str,
    editable: bool = True,
    finalized: bool = False
) -> str:
    """
    Saves an editable or finalized interpretation to disk.
    Returns the unique interpretation ID.
    """
    interpretation_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat()

    output = {
        "interpretation_id": interpretation_id,
        "timestamp": timestamp,
        "patient_id": patient_id,
        "provider_id": provider_id,
        "editable": editable,
        "finalized": finalized,
        "summary": summary,
        "interpretation_text": interpretation_text
    }

    path = SAVE_DIR / f"{interpretation_id}.json"
    with open(path, "w") as f:
        json.dump(output, f, indent=2)

    return interpretation_id


def load_interpretation(interpretation_id: str) -> dict:
    path = SAVE_DIR / f"{interpretation_id}.json"
    if not path.exists():
        raise FileNotFoundError(f"Interpretation not found: {interpretation_id}")

    with open(path, "r") as f:
        return json.load(f)


def update_interpretation(interpretation_id: str, new_text: str, provider_id: str) -> None:
    data = load_interpretation(interpretation_id)

    if data.get("finalized", False):
        raise ValueError("Interpretation has been finalized and cannot be edited.")

    data["interpretation_text"] = new_text
    data["timestamp"] = datetime.utcnow().isoformat()
    data["provider_id"] = provider_id

    path = SAVE_DIR / f"{interpretation_id}.json"
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def finalize_interpretation(interpretation_id: str) -> dict:
    data = load_interpretation(interpretation_id)
    data["finalized"] = True
    data["editable"] = False
    data["timestamp"] = datetime.utcnow().isoformat()

    path = SAVE_DIR / f"{interpretation_id}.json"
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

    return data  # for billing
