from app.services.cgm_processing.metrics import compute_cgm_metrics
from app.models.cgm_point import CGMPoint
from datetime import datetime, timedelta

def test_compute_metrics_basic_case():
    now = datetime.utcnow()
    points = [CGMPoint(timestamp=now + timedelta(minutes=i*5), glucose=100 + i) for i in range(12)]
    result = compute_cgm_metrics(points)
    assert "mean_glucose" in result
    assert result["tir_percent"] > 0
