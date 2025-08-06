from pathlib import Path
from app.services.cgm_processing.loader import load_cgm_file
from app.services.cgm_processing.summarizer import generate_summary
from app.services.cgm_processing.recommender import generate_recommendations
from app.services.llm.generator import generate_interpretation
from app.services.workflow.editor import save_interpretation
from app.models.cgm_point import CGMPoint


def run_interpretation_workflow(
    patient_id: str,
    provider_id: str,
    file_path: Path
) -> dict:
    """
    Full pipeline:
    - Load CGM file
    - Calculate metrics and patterns
    - Generate recommendations
    - Call LLM for interpretation
    - Save editable version

    Returns:
        dict with summary, interpretation_text, interpretation_id
    """
    # Step 1: Load data
    readings: list[CGMPoint] = load_cgm_file(file_path)

    # Step 2: Summarize
    summary = generate_summary(readings)

    # Step 3: Get rule-based suggestions
    recommendations = generate_recommendations(summary["recommendation_context"])

    # Step 4: Call LLM
    interpretation_text = generate_interpretation(summary, recommendations)

    # Step 5: Save editable version
    interpretation_id = save_interpretation(
        patient_id=patient_id,
        summary=summary,
        interpretation_text=interpretation_text,
        provider_id=provider_id,
        editable=True,
        finalized=False
    )

    return {
        "interpretation_id": interpretation_id,
        "summary": summary,
        "recommendations": recommendations,
        "interpretation_text": interpretation_text
    }
