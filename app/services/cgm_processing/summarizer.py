from typing import List, Dict, Any
from app.models.cgm_point import CGMPoint
from app.services.cgm_processing.metrics import compute_cgm_metrics
from app.services.cgm_processing.patterns import detect_all_patterns


def generate_summary(readings: List[CGMPoint]) -> Dict[str, Any]:
    """
    Unifies metrics and event patterns into one structured summary
    ready for interpretation, review, billing, and audit.
    """
    metrics = compute_cgm_metrics(readings)
    patterns = detect_all_patterns(readings)

    summary = {
        "metrics": metrics,
        "patterns": patterns,
        "recommendation_context": {
            "high_cv": metrics["cv"] > 36,
            "low_tir": metrics["tir_percent"] < 70,
            "frequent_hypos": len(patterns.get("nocturnal_hypoglycemia_episodes", [])) >= 2,
            "frequent_spikes": len(patterns["postprandial_spikes"]) >= 3,
            "dawn_present": patterns["dawn_phenomenon"]
        }
    }

    return summary
