import random

def analyze_photo(photo_path):
    """
    Mock implementation of a YOLO vision model.
    In a real-world scenario, this function would load a custom trained YOLO model,
    run inference on the photo_path, and return detected bounding boxes, severity, and confidence.
    For this MVP, it randomly simulates analyzing a pothole image.
    """
    # Simulate processing time or model loading
    severity_choices = ['LOW', 'MEDIUM', 'CRITICAL']

    # 90% chance of successfully detecting a pothole
    is_pothole = random.random() < 0.90

    if is_pothole:
        severity = random.choice(severity_choices)
        confidence = random.uniform(0.65, 0.98) # Random confidence between 65% and 98%
        return {
            'detected': True,
            'severity': severity,
            'confidence': confidence
        }
    else:
        return {
            'detected': False,
            'severity': 'UNVERIFIED',
            'confidence': 0.0
        }
