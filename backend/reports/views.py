from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Report
from .serializers import ReportSerializer
from .ai_vision import analyze_photo

class ReportListCreateView(generics.ListCreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.AllowAny] # Allow anonymous reporting for citizens

    def perform_create(self, serializer):
        citizen = self.request.user if self.request.user.is_authenticated else None

        # Save the report initially to get the photo saved on disk
        report = serializer.save(citizen=citizen)

        # Call the mock AI vision model to analyze the photo
        analysis = analyze_photo(report.photo.path)

        if analysis['detected']:
            report.severity = analysis['severity']
            report.ai_confidence = analysis['confidence']
            report.status = 'VERIFIED'
        else:
            report.status = 'REPORTED' # Remains unverified by AI

        report.save()

class ReportDetailView(generics.RetrieveUpdateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]
