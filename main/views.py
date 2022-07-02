from django.shortcuts import render
from django.http import HttpResponse
from .models import Sensor, Item

def index(response):
    return HttpResponse("<h1>Index</h1>")

def sensor_id(response, id):
    se = Sensor.objects.get(id=id)
    return HttpResponse("<h1>%s</h1>" % se.name)