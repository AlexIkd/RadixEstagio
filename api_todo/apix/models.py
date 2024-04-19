from django.db import models

class SensorData(models.Model):
    equipment_id = models.CharField(max_length=100)
    done = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=False)
    value = models.DecimalField(max_digits=10, decimal_places=2)