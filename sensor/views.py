import logging

from django.shortcuts import render

from .models import Raspi, Sensor


def index(request):
    raspi = Raspi.objects.all()
    return render(request, 'sensor/index.html', {
        'raspi': raspi,
    })


def pi_name(request, pi_name):
    raspi = Raspi.objects.all()
    raspberry = [ x.name for x in raspi ]
    return render(request, 'sensor/raspi.html', {
        'pi_name': pi_name,
        'raspberry': raspberry,
    })


def sensor_name(request, sensor_name, pi_name):
    raspi = Raspi.objects.get(name=pi_name)
    sen = raspi.sensor_set.all()
    sensors = [ x.name for x in sen ]
    logging.debug(sensors)
    return render(request, 'sensor/sensor.html', {
        'pi_name': pi_name,
        'sensor_name': sensor_name,
    })
