from django.db import models


class Sensor(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Item(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    data = models.CharField(max_length=300)

    def __str__(self):
        return self.data
