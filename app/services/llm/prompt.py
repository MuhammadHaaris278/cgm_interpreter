from typing import Dict, Any

def build_prompt(summary: Dict[str, Any], recommendations: list[str]) -> str:
    """
    Builds a structured prompt for GPT-4.1 given CGM summary + recs.
    """
    metrics = summary.get("metrics", {})
    patterns = summary.get("patterns", {})
    
    prompt = f"""
You are an expert endocrinologist interpreting Continuous Glucose Monitoring (CGM) data.
Given the following summary metrics and patterns, generate a concise and clinically accurate interpretation.

Metrics:
- Mean Glucose: {metrics.get('mean_glucose')} mg/dL
- Standard Deviation: {metrics.get('std_glucose')} mg/dL
- Coefficient of Variation (CV): {metrics.get('cv')}%
- GMI: {metrics.get('gmi')}
- Time in Range (70–180 mg/dL): {metrics.get('tir_percent')}%
- Time Below Range (<70): {metrics.get('below_70_percent')}%
- Time Above Range (>180): {metrics.get('above_180_percent')}%

Patterns Detected:
- Dawn Phenomenon: {patterns.get('dawn_phenomenon')}
- No. of Hypoglycemia Events: {len(patterns.get('hypoglycemia_events', []))}
- No. of Nocturnal Hypo Events: {len(patterns.get('nocturnal_hypoglycemia_events', []))}
- No. of Hyperglycemia Events: {len(patterns.get('hyperglycemia_events', []))}
- Postprandial Spikes: {len(patterns.get('postprandial_spikes', []))}

Recommendations (if needed):
- {chr(10).join(f"- {rec}" for rec in recommendations)}

Your interpretation must include:
1. A one-paragraph summary of the patient’s glucose control.
2. Identification of any abnormal patterns (e.g., nocturnal hypoglycemia, postprandial spikes).
3. Clinical guidance or action suggestions based on the findings.

Use clinical, concise language appropriate for an EHR. Avoid fluff.
"""

    return prompt.strip()
