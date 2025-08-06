from typing import List, Dict, Any
from datetime import datetime
from app.models.cgm_point import CGMPoint
from app.utils.datetime_tools import is_nocturnal, is_dawn_window

def is_postprandial(dt: datetime) -> bool:
    """Postprandial window: 6 AM to 10 PM."""
    return 6 <= dt.hour <= 22


def _group_hypo_episodes(events: List[Dict], min_gap_minutes: int = 30) -> List[Dict]:
    """Group consecutive low-glucose readings into discrete episodes."""
    if not events:
        return []

    grouped = []
    current_group = [events[0]]

    for i in range(1, len(events)):
        prev = datetime.fromisoformat(events[i - 1]["timestamp"])
        curr = datetime.fromisoformat(events[i]["timestamp"])
        gap = (curr - prev).total_seconds() / 60.0

        if gap <= min_gap_minutes:
            current_group.append(events[i])
        else:
            grouped.append(current_group)
            current_group = [events[i]]

    grouped.append(current_group)

    episodes = []
    for group in grouped:
        times = [datetime.fromisoformat(r["timestamp"]) for r in group]
        values = [r["glucose"] for r in group]
        episodes.append({
            "start": min(times).isoformat(),
            "end": max(times).isoformat(),
            "min_glucose": min(values),
            "count": len(group)
        })

    return episodes


def detect_all_patterns(readings: List[CGMPoint]) -> Dict[str, Any]:
    readings = sorted(readings, key=lambda x: x.timestamp)

    hypo = []
    nocturnal_hypo = []
    hyper = []
    spikes = []
    spike_tracker = set()

    for r in readings:
        if r.glucose < 70:
            hypo.append({
                "timestamp": r.timestamp.isoformat(),
                "glucose": r.glucose
            })
            if is_nocturnal(r.timestamp):
                nocturnal_hypo.append({
                    "timestamp": r.timestamp.isoformat(),
                    "glucose": r.glucose
                })

        elif r.glucose > 180:
            hyper.append({
                "timestamp": r.timestamp.isoformat(),
                "glucose": r.glucose
            })

    # Improved postprandial spike detection
    for i in range(len(readings) - 12):  # ~60 minutes apart
        start = readings[i]
        end = readings[i + 12]
        delta = end.glucose - start.glucose

        if not is_postprandial(start.timestamp):
            continue

        if delta >= 40:  # tighter, more specific spike definition
            rounded_time = start.timestamp.replace(minute=0, second=0)
            if rounded_time in spike_tracker:
                continue
            spike_tracker.add(rounded_time)

            spikes.append({
                "start": start.timestamp.isoformat(),
                "end": end.timestamp.isoformat(),
                "delta": round(delta, 2)
            })

    # Dawn phenomenon detection: multiple rising events between 2–8 AM
    dawn_rise_count = 0
    for i in range(1, len(readings)):
        prev = readings[i - 1]
        curr = readings[i]
        if is_dawn_window(prev.timestamp) and is_dawn_window(curr.timestamp):
            if curr.glucose - prev.glucose >= 20:
                dawn_rise_count += 1
    dawn_present = dawn_rise_count >= 3

    return {
        "hypoglycemia_events": hypo,
        "nocturnal_hypoglycemia_events": nocturnal_hypo,
        "nocturnal_hypoglycemia_episodes": _group_hypo_episodes(nocturnal_hypo),
        "hyperglycemia_events": hyper,
        "postprandial_spikes": spikes,
        "dawn_phenomenon": dawn_present
    }
