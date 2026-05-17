import numpy as np
from sklearn.cluster import DBSCAN
from django.contrib.gis.geos import Point
from reports.models import Report
from .models import Incident

# Convert meters to degrees for epsilon calculation in DBSCAN (very rough approximation)
# 1 degree of latitude is approx 111,320 meters
METERS_PER_DEGREE = 111320
RADIUS_IN_METERS = 5.0
EPSILON_DEGREES = RADIUS_IN_METERS / METERS_PER_DEGREE

def run_dbscan_clustering():
    """
    Fetches all unassigned or pending reports, runs DBSCAN based on location (5 meters),
    and creates/updates Master Incidents in the database.
    """
    reports = Report.objects.filter(status__in=['REPORTED', 'VERIFIED'])
    if not reports.exists():
        return

    # Extract coordinates
    coords = []
    report_list = list(reports)
    for r in report_list:
        coords.append([r.location.y, r.location.x])  # [lat, lon]

    coords_array = np.array(coords)

    # Run DBSCAN
    db = DBSCAN(eps=EPSILON_DEGREES, min_samples=1, metric='euclidean').fit(coords_array)
    labels = db.labels_

    # Group reports by cluster label
    clusters = {}
    for idx, label in enumerate(labels):
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(report_list[idx])

    # Create or update Incidents for each cluster
    for label, cluster_reports in clusters.items():
        if label == -1:
            # Noise (though with min_samples=1, this shouldn't happen)
            continue

        # Calculate center point
        lats = [r.location.y for r in cluster_reports]
        lons = [r.location.x for r in cluster_reports]
        center_lat = sum(lats) / len(lats)
        center_lon = sum(lons) / len(lons)
        center_point = Point(center_lon, center_lat, srid=4326)

        # Determine aggregated severity (take the maximum severity)
        severity_weights = {'UNVERIFIED': 0, 'LOW': 1, 'MEDIUM': 2, 'CRITICAL': 3}
        max_severity = 'LOW'
        max_weight = 1

        for r in cluster_reports:
            w = severity_weights.get(r.severity, 0)
            if w > max_weight:
                max_weight = w
                max_severity = r.severity

        # Find existing incident or create new
        # For simplicity, we just create a new incident if reports aren't already attached to one
        incident, created = Incident.objects.get_or_create(
            center_location=center_point,
            defaults={'aggregated_severity': max_severity}
        )

        if not created and severity_weights.get(incident.aggregated_severity, 0) < max_weight:
             incident.aggregated_severity = max_severity
             incident.save()

        for r in cluster_reports:
            incident.reports.add(r)

    return len(clusters)
