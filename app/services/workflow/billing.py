import json
from pathlib import Path
from datetime import datetime
from app.config.loader import Config

config = Config()
BILLING_LOG_DIR = config.billing_log_dir

def trigger_cpt_95251(patient_id: str, provider_id: str, duration_days: int) -> str:
    """
    Logs a billing event if criteria are met.
    """
    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "patient_id": patient_id,
        "provider_id": provider_id,
        "cpt_code": "95251",
        "duration_days": duration_days
    }

    record_id = f"{patient_id}_{datetime.utcnow().timestamp()}"
    path = BILLING_LOG_DIR / f"{record_id}.json"

    with open(path, "w") as f:
        json.dump(record, f, indent=2)

    return record_id
