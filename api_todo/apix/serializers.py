from apix.models import SensorData
from rest_framework import serializers

class SensorDataSerial(serializers.ModelSerializer):
    class Meta:
        model = SensorData
        fields = ['id', 'equipment_id', 'done', 'timestamp', 'value']