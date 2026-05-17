from django.db import models
from django.contrib.gis.db import models as gis_models
from reports.models import Report

class Incident(models.Model):
    # An incident is a cluster of one or more reports
    SEVERITY_CHOICES = (
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('CRITICAL', 'Critical'),
    )

    STATUS_CHOICES = (
        ('PENDING', 'Pending Repair'),
        ('IN_PROGRESS', 'Repair In Progress'),
        ('RESOLVED', 'Resolved'),
    )

    center_location = gis_models.PointField(srid=4326)
    aggregated_severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='LOW')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    reports = models.ManyToManyField(Report, related_name='incidents')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Incident {self.id} ({self.aggregated_severity})"
