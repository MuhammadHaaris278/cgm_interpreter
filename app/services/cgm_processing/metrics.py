from typing import List, Dict
from statistics import mean, stdev
from app.models.cgm_point import CGMPoint

# Glycemic thresholds in mg/dL (standard)
TIR_LOWER = 70
TIR_UPPER = 180
LOW_L1 = 54
HIGH_L1 = 250

def compute_cgm_metrics(readings: List[CGMPoint]) -> Dict[str, float]:
    """
    Computes standard CGM metrics from CGMPoint list:
    - Mean Glucose
    - Standard Deviation
    - Coefficient of Variation (CV)
    - GMI (Glucose Management Indicator)
    - Time In Range (70–180 mg/dL)
    - Time Below Range (Level 1 <70, Level 2 <54)
    - Time Above Range (Level 1 >180, Level 2 >250)
    Returns all metrics in percentages and absolute stats.
    """

    # Extract glucose values
    glucose_values = [r.glucose for r in readings if r.glucose is not None]
    total = len(glucose_values)

    if total == 0:
        raise ValueError("No valid CGM glucose data available.")

    # Core metrics
    avg = mean(glucose_values)
    std = stdev(glucose_values) if total > 1 else 0.0
    cv = (std / avg) * 100 if avg else 0.0
    gmi = 3.31 + (0.02392 * avg)

    # TIR metrics (percentage of time)
    tir = len([v for v in glucose_values if TIR_LOWER <= v <= TIR_UPPER])
    below_70 = len([v for v in glucose_values if v < TIR_LOWER])
    below_54 = len([v for v in glucose_values if v < LOW_L1])
    above_180 = len([v for v in glucose_values if v > TIR_UPPER])
    above_250 = len([v for v in glucose_values if v > HIGH_L1])

    return {
        "mean_glucose": round(avg, 2),
        "std_glucose": round(std, 2),
        "cv": round(cv, 2),
        "gmi": round(gmi, 2),

        "tir_percent": round((tir / total) * 100, 2),
        "below_70_percent": round((below_70 / total) * 100, 2),
        "below_54_percent": round((below_54 / total) * 100, 2),
        "above_180_percent": round((above_180 / total) * 100, 2),
        "above_250_percent": round((above_250 / total) * 100, 2),

        "tir_count": tir,
        "below_70_count": below_70,
        "below_54_count": below_54,
        "above_180_count": above_180,
        "above_250_count": above_250,
        "total_points": total
    }
