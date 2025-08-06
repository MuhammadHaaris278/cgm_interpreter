from pydantic import BaseModel
from datetime import datetime

class CGMPoint(BaseModel):
    timestamp: datetime
    glucose: float