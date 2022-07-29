import json
import logging

from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import AddRaspi
from .models import Raspi, Sensor


def index(request):
    raspi = Raspi.objects.all().order_by('name')
    return render(request, 'sensor/index.html', {
        'raspi': raspi,
    })


def add_pi(request):
    if request.method == "POST":
        form = AddRaspi(request.POST)

        if form.is_valid():
            logging.debug("Raspi is valid")
            name = form.cleaned_data["name"]
            address = form.cleaned_data["address"]
            raspi = Raspi(name=name, address=address)
            raspi.save()

            sensors = ["dht11", "ultrasonic", "8x8matrix", "buzzer",
                       "relay", "lcd", "7segment", "ledarray", "joystick"]

            for sensor_name in sensors:
                raspi.sensor_set.create(name=sensor_name)
            raspi.save()

        return HttpResponseRedirect("/")

    else:
        form = AddRaspi()

    return render(request, 'sensor/raspberry/add-pi.html', {
        'form': form
    })


def modify_pi(request):
    raspi = Raspi.objects.all().order_by('name')
    form = AddRaspi()

    if request.method == "POST":
        body = json.loads(request.body)

        raspi_id = body["raspi_id"]
        raspi_name = body["raspi_name"]
        raspi_address = body["raspi_address"]

        pi = Raspi.objects.get(id=raspi_id)

        pi.name = raspi_name
        pi.address = raspi_address

        pi.save()

    return render(request, 'sensor/raspberry/modify-pi.html', {
        'form': form,
        'raspi': raspi,
    })


def remove_pi(request):
    raspi = Raspi.objects.all().order_by('name')

    if request.method == "POST":
        body = json.loads(request.body)
        raspi_name = body["raspi_name"]
        raspi_id = body["raspi_id"]

        pi = Raspi.objects.get(id=raspi_id, name=raspi_name)
        pi.delete()

    return render(request, 'sensor/raspberry/remove-pi.html', {
        'raspi': raspi,
    })


def pinout(request):
    return render(request, 'sensor/base/pinout.html')


def pi_name(request, pi_name):
    raspi = Raspi.objects.all().order_by('name')
    pi_list = [x.name for x in raspi]
    sensors = ["dht11", "ultrasonic", "8x8matrix", "buzzer",
               "relay", "lcd", "7segment", "ledarray", "joystick"]

    return render(request, 'sensor/raspberry/raspi.html', {
        'pi_name': pi_name,
        'pi_list': pi_list,
        'sensors': sensors
    })


def sensor_name(request, pi_name, sensor_name):
    debug = settings.DEBUG
    sensors = ["dht11", "ultrasonic", "8x8matrix", "buzzer",
               "relay", "lcd", "7segment", "ledarray", "joystick"]

    return render(request, 'sensor/sensor.html', {
        'debug': debug,
        'pi_name': pi_name,
        'sensor_name': sensor_name,
        'sensors': sensors,
        'url': f'sensor/sensors/{sensor_name}.html',
    })


def sensor_extra(request, pi_name, sensor_name, extra):
    debug = settings.DEBUG
    return render(request, 'sensor/extra.html', {
        'debug': debug,
        'pi_name': pi_name,
        'sensor_name': sensor_name,
        'extra': extra,
        'url': f'sensor/sensors/{sensor_name}/{extra}.html',
    })
