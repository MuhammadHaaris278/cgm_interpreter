from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pathlib import Path
import shutil
import tempfile
from app.services.controller import run_interpretation_workflow
from app.services.workflow.editor import update_interpretation, finalize_interpretation
from app.services.workflow.billing import trigger_cpt_95251
from app.config.loader import Config

router = APIRouter()
config = Config()

@router.post("/interpret")
async def interpret_cgm_data(
    patient_id: str = Form(...),
    provider_id: str = Form(...),
    file: UploadFile = File(...)
):
    """
    Uploads a CGM JSON file, runs the full interpretation pipeline,
    and returns the editable report with interpretation_id.
    """
    if not file.filename.endswith(".json"):
        raise HTTPException(status_code=400, detail="Only .json files are supported.")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = Path(tmp.name)

    try:
        result = run_interpretation_workflow(
            patient_id=patient_id,
            provider_id=provider_id,
            file_path=tmp_path
        )
        return result
    finally:
        tmp_path.unlink(missing_ok=True)


@router.post("/edit/{interpretation_id}")
async def edit_interpretation(
    interpretation_id: str,
    new_text: str = Form(...),
    provider_id: str = Form(...)
):
    """
    Updates the interpretation text if it hasn't been finalized.
    """
    try:
        update_interpretation(interpretation_id, new_text, provider_id)
        return {"message": "Interpretation updated successfully."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/finalize/{interpretation_id}")
async def finalize_report(
    interpretation_id: str,
    patient_id: str = Form(...),
    provider_id: str = Form(...),
    duration_days: int = Form(...)
):
    """
    Locks the report and triggers CPT 95251 billing event if valid.
    """
    try:
        finalized_data = finalize_interpretation(interpretation_id)
        if duration_days >= 3:
            billing_id = trigger_cpt_95251(
                patient_id=patient_id,
                provider_id=provider_id,
                duration_days=duration_days
            )
            return {
                "message": "Report finalized and CPT 95251 triggered.",
                "billing_id": billing_id
            }
        else:
            return {"message": "Report finalized (CPT not triggered due to short duration)."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
