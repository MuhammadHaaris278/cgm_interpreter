from app.services.cgm_processing.patterns import detect_all_patterns
from app.models.cgm_point import CGMPoint
from datetime import datetime, timedelta

def test_pattern_detection_dawn():
    base = datetime(2025, 8, 1, 2, 0)
    readings = [CGMPoint(timestamp=base + timedelta(minutes=i*5), glucose=70 + i) for i in range(72)]
    result = detect_all_patterns(readings)
    assert isinstance(result["dawn_phenomenon"], bool)
