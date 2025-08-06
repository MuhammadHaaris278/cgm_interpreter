from pydantic import BaseModel
from typing import List, Dict, Any

class CGMSummary(BaseModel):
    metrics: Dict[str, float]
    patterns: Dict[str, Any]
    recommendation_context: Dict[str, bool]