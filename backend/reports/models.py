from django.db import models
from django.contrib.gis.db import models as gis_models
from django.conf import settings

class Report(models.Model):
    SEVERITY_CHOICES = (
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('CRITICAL', 'Critical'),
        ('UNVERIFIED', 'Unverified')
    )

    STATUS_CHOICES = (
        ('REPORTED', 'Reported'),
        ('VERIFIED', 'Verified'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
    )

    citizen = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='reports')
    photo = models.ImageField(upload_to='report_photos/')
    location = gis_models.PointField(srid=4326) # WGS84
    description = models.TextField(blank=True, null=True)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='UNVERIFIED')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='REPORTED')

    # Optional fields for AI analysis results
    ai_confidence = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Report {self.id} at {self.location} - {self.severity}"
