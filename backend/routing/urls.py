from django.urls import path
from .views import IncidentListView, TriggerClusteringView, get_optimized_route

urlpatterns = [
    path('incidents/', IncidentListView.as_view(), name='incident-list'),
    path('incidents/cluster/', TriggerClusteringView.as_view(), name='trigger-clustering'),
    path('incidents/route/', get_optimized_route, name='get-optimized-route'),
]
