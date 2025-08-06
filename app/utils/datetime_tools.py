from datetime import datetime, time

def is_nocturnal(dt: datetime) -> bool:
    """
    Returns True if time is between 10:00 PM and 6:00 AM
    """
    return dt.hour >= 22 or dt.hour < 6

def is_dawn_window(dt: datetime) -> bool:
    """
    Returns True if time is between 2:00 AM and 8:00 AM
    """
    return 2 <= dt.hour < 8

def iso8601(dt: datetime) -> str:
    """
    Returns a UTC ISO 8601 string with Z suffix
    """
    return dt.replace(microsecond=0).isoformat() + "Z"

def parse_iso8601(s: str) -> datetime:
    """
    Parses ISO string into datetime with fallback for 'Z' suffix
    """
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except Exception as e:
        raise ValueError(f"Invalid datetime format: {s}") from e
