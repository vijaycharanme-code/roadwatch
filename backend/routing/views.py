from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Incident
from rest_framework import serializers
from .clustering import run_dbscan_clustering

class IncidentSerializer(serializers.ModelSerializer):
    longitude = serializers.SerializerMethodField()
    latitude = serializers.SerializerMethodField()
    report_count = serializers.SerializerMethodField()

    class Meta:
        model = Incident
        fields = ('id', 'center_location', 'longitude', 'latitude', 'aggregated_severity', 'status', 'report_count', 'created_at')

    def get_longitude(self, obj):
        return obj.center_location.x

    def get_latitude(self, obj):
        return obj.center_location.y

    def get_report_count(self, obj):
        return obj.reports.count()


class IncidentListView(generics.ListAPIView):
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer
    permission_classes = [permissions.AllowAny]


class TriggerClusteringView(APIView):
    permission_classes = [permissions.AllowAny] # In production, restrict to Admin or run via Celery cron

    def post(self, request, *args, **kwargs):
        num_clusters = run_dbscan_clustering()
        return Response({"message": f"Clustering completed. {num_clusters} incidents processed or created."})

from .tsp import calculate_optimal_route
from rest_framework.decorators import api_view, permission_classes

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_optimized_route(request):
    # Fetch top pending incidents ordered by severity
    # CRITICAL -> MEDIUM -> LOW

    # Custom ordering using annotate is possible, but for MVP we will fetch and sort in python
    incidents = list(Incident.objects.filter(status='PENDING'))

    if not incidents:
        return Response({"route": []})

    severity_order = {'CRITICAL': 0, 'MEDIUM': 1, 'LOW': 2}

    # Get top 20 most critical/high severity pending incidents to route
    incidents.sort(key=lambda x: severity_order.get(x.aggregated_severity, 3))
    incidents_to_route = incidents[:20]

    route_ids = calculate_optimal_route(incidents_to_route)

    # Serialize the ordered incidents
    ordered_incidents = []
    for inc_id in route_ids:
        # Find the incident object
        inc_obj = next(i for i in incidents_to_route if i.id == inc_id)
        ordered_incidents.append(IncidentSerializer(inc_obj).data)

    return Response({"route": ordered_incidents})
