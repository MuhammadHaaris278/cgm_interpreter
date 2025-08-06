from typing import List, Dict


def generate_recommendations(context: Dict[str, bool]) -> List[str]:
    """
    Based on rule-triggered flags from CGM summary,
    generate treatment-focused recommendation bullet points.
    """

    recs = []

    if context.get("low_tir", False):
        recs.append("Consider intensifying glucose control to increase time in range.")

    if context.get("frequent_hypos", False):
        recs.append("Evaluate overnight basal insulin to reduce hypoglycemia events.")
        recs.append("Review patient's hypoglycemia awareness and carbohydrate intake.")

    if context.get("high_cv", False):
        recs.append("Glycemic variability is elevated; consider smoothing basal-bolus dosing or adjusting meal timing.")

    if context.get("frequent_spikes", False):
        recs.append("Postprandial spikes suggest possible missed boluses or carbohydrate misestimation.")

    if context.get("dawn_present", False):
        recs.append("Dawn phenomenon detected; evaluate basal rate or consider split dose timing.")

    if not recs:
        recs.append("Maintain current therapy; no concerning patterns identified.")

    return recs