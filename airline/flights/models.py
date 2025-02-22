from django.db import models

# Create your models here.
class airport(models.Model):
    icao_code = models.CharField(max_length=4)
    iata_code = models.CharField(max_length=3)
    name = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    lat_decimal = models.DecimalField(max_digits=10, decimal_places=5)
    lon_decimal = models.DecimalField(max_digits=10, decimal_places=5)

    def __str__(self):
        return f"{self.country}({self.icao_code})"

class passenger(models.Model):
    first = models.CharField(max_length=20)
    last = models.CharField(max_length=20)

class flight(models.Model):
    origin = models.ForeignKey(airport, on_delete=models.CASCADE, related_name="departures")
    destination = models.ForeignKey(airport, on_delete=models.CASCADE, related_name="arrivals")
    duration = models.IntegerField()
    passengers = models.ManyToManyField(passenger, blank=True, related_name="flights")
