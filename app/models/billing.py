from pydantic import BaseModel
from datetime import datetime

class BillingEvent(BaseModel):
    timestamp: datetime
    patient_id: str
    provider_id: str
    cpt_code: str = "95251"
    duration_days: int