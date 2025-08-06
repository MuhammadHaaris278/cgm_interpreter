from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.summary import CGMSummary

class Interpretation(BaseModel):
    interpretation_id: str
    timestamp: datetime
    patient_id: str
    provider_id: str
    editable: bool
    finalized: bool
    summary: CGMSummary
    interpretation_text: str