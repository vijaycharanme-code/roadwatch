from rest_framework import serializers
from .models import Report
from django.contrib.gis.geos import Point

class ReportSerializer(serializers.ModelSerializer):
    longitude = serializers.FloatField(write_only=True)
    latitude = serializers.FloatField(write_only=True)

    class Meta:
        model = Report
        fields = ('id', 'citizen', 'photo', 'description', 'severity', 'status', 'ai_confidence', 'created_at', 'longitude', 'latitude', 'location')
        read_only_fields = ('id', 'severity', 'status', 'ai_confidence', 'created_at', 'location', 'citizen')

    def create(self, validated_data):
        longitude = validated_data.pop('longitude')
        latitude = validated_data.pop('latitude')

        # Create Point object from coordinates
        location = Point(longitude, latitude, srid=4326)
        validated_data['location'] = location

        # We will assign the citizen in the view
        return super().create(validated_data)
