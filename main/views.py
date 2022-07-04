from django.shortcuts import render
from django.http import HttpResponse
from .models import Sensor, Item

def index(response):
    return render(response, "main/index.html", {})


def sensor_id(response, id):
    sensor = Sensor.objects.get(id=id)
    return render(response, "main/list.html", {"sensor": sensor})


