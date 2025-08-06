import json
from typing import List
from pathlib import Path
from datetime import datetime
from app.models.cgm_point import CGMPoint


def load_cgm_file(file_path: Path) -> List[CGMPoint]:
    """
    Loads and parses a JSON file with Dexcom-style CGM readings.
    Supports both mock files and Dexcom API-compatible schema.

    Args:
        file_path: path to a local .json file

    Returns:
        List[CGMPoint]
    """
    with open(file_path, "r") as f:
        raw_data = json.load(f)

    # Handle Dexcom official schema
    if isinstance(raw_data, dict) and "records" in raw_data:
        readings = raw_data["records"]
        return _parse_dexcom_records(readings)

    # Handle list of mock data records
    elif isinstance(raw_data, list):
        return _parse_mock_format(raw_data)

    else:
        raise ValueError("Unrecognized CGM file format")


def _parse_mock_format(data: List[dict]) -> List[CGMPoint]:
    parsed = []
    for item in data:
        timestamp = item.get("timestamp") or item.get("systemTime") or item.get("displayTime")
        value = item.get("glucose_mg_per_dl") or item.get("value") or item.get("smoothedValue")
        if timestamp and value:
            parsed.append(CGMPoint(
                timestamp=_parse_time(timestamp),
                glucose=float(value)
            ))
    return sorted(parsed, key=lambda x: x.timestamp)


def _parse_dexcom_records(records: List[dict]) -> List[CGMPoint]:
    parsed = []
    for r in records:
        if not r.get("value"):
            continue
        parsed.append(CGMPoint(
            timestamp=_parse_time(r["systemTime"]),
            glucose=float(r["value"])
        ))
    return sorted(parsed, key=lambda x: x.timestamp)


def _parse_time(t: str) -> datetime:
    # ISO 8601 UTC or offset timestamps
    try:
        return datetime.fromisoformat(t.replace("Z", "+00:00"))
    except Exception:
        raise ValueError(f"Invalid timestamp format: {t}")
