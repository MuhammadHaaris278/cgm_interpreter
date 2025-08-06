from typing import List, Dict, Any
from datetime import datetime, timedelta
from app.models.cgm_point import CGMPoint

HYPO_THRESHOLD = 70
SEVERE_HYPO = 54
HYPER_THRESHOLD = 250
SPIKE_DELTA = 30
DAWN_WINDOW = (2, 8)  # 2am–8am
NOCTURNAL_WINDOW = (22, 6)

def detect_hypo_events(readings: List[CGMPoint]) -> List[Dict[str, Any]]:
    events = []
    current_event = []

    for point in readings:
        if point.glucose < HYPO_THRESHOLD:
            current_event.append(point)
        else:
            if len(current_event) >= 3:  # ≥15 min = 3 readings
                events.append({
                    "start": current_event[0].timestamp.isoformat(),
                    "end": current_event[-1].timestamp.isoformat(),
                    "min_glucose": min(p.glucose for p in current_event),
                    "count": len(current_event)
                })
            current_event = []

    # Handle trailing event
    if len(current_event) >= 3:
        events.append({
            "start": current_event[0].timestamp.isoformat(),
            "end": current_event[-1].timestamp.isoformat(),
            "min_glucose": min(p.glucose for p in current_event),
            "count": len(current_event)
        })

    return events

def detect_nocturnal_hypoglycemia(events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    nocturnal_events = []
    for e in events:
        start_time = datetime.fromisoformat(e["start"])
        if (start_time.hour >= NOCTURNAL_WINDOW[0]) or (start_time.hour < NOCTURNAL_WINDOW[1]):
            nocturnal_events.append(e)
    return nocturnal_events

def detect_hyper_events(readings: List[CGMPoint]) -> List[Dict[str, Any]]:
    events = []
    current_event = []

    for point in readings:
        if point.glucose > HYPER_THRESHOLD:
            current_event.append(point)
        else:
            if len(current_event) >= 3:
                events.append({
                    "start": current_event[0].timestamp.isoformat(),
                    "end": current_event[-1].timestamp.isoformat(),
                    "max_glucose": max(p.glucose for p in current_event),
                    "count": len(current_event)
                })
            current_event = []

    if len(current_event) >= 3:
        events.append({
            "start": current_event[0].timestamp.isoformat(),
            "end": current_event[-1].timestamp.isoformat(),
            "max_glucose": max(p.glucose for p in current_event),
            "count": len(current_event)
        })

    return events

def detect_dawn_phenomenon(readings: List[CGMPoint]) -> bool:
    """
    Detects a rise of ≥20 mg/dL from nadir in 2–6am to peak in 6–8am window
    """
    nadir = None
    rise = None

    overnight = [r for r in readings if 2 <= r.timestamp.hour < 6]
    morning = [r for r in readings if 6 <= r.timestamp.hour < 8]

    if not overnight or not morning:
        return False

    nadir_val = min(r.glucose for r in overnight)
    peak_val = max(r.glucose for r in morning)

    if (peak_val - nadir_val) >= 20:
        return True
    return False

def detect_postprandial_spikes(readings: List[CGMPoint]) -> List[Dict[str, Any]]:
    """
    Identifies glucose rises of ≥30 mg/dL over any 60–90 min window
    """
    spikes = []
    for i in range(len(readings) - 6):  # 6 x 5min = 30min minimum window
        start = readings[i]
        for j in range(i+6, min(i+18, len(readings))):  # Up to 90 mins ahead
            end = readings[j]
            if (end.glucose - start.glucose) >= SPIKE_DELTA:
                spikes.append({
                    "start": start.timestamp.isoformat(),
                    "end": end.timestamp.isoformat(),
                    "delta": round(end.glucose - start.glucose, 2)
                })
                break  # Only count first spike in that window
    return spikes

def detect_all_patterns(readings: List[CGMPoint]) -> Dict[str, Any]:
    hypo_events = detect_hypo_events(readings)
    hyper_events = detect_hyper_events(readings)
    nocturnal_hypo = detect_nocturnal_hypoglycemia(hypo_events)
    dawn_present = detect_dawn_phenomenon(readings)
    spikes = detect_postprandial_spikes(readings)

    return {
        "hypoglycemia_events": hypo_events,
        "nocturnal_hypoglycemia_events": nocturnal_hypo,
        "hyperglycemia_events": hyper_events,
        "dawn_phenomenon": dawn_present,
        "postprandial_spikes": spikes
    }
