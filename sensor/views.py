import json
import logging

from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import AddRaspi
from .models import Raspi, Sensor


def index(request):
    raspi = Raspi.objects.all()
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

    return render(request, 'sensor/add-pi.html', {'form': form})


def remove_pi(request):
    raspi = Raspi.objects.all()
    if request.method == "POST":
        body = json.loads(request.body)
        name = body["pi_name"]
        pi = Raspi.objects.get(name=name)
        pi.delete()

        return HttpResponseRedirect("/")

    return render(request, 'sensor/remove-pi.html', {
        'raspi': raspi,
    })


def pi_name(request, pi_name):
    raspi = Raspi.objects.all()
    pi_list = [x.name for x in raspi]
    sensors = ["dht11", "ultrasonic", "8x8matrix", "buzzer",
               "relay", "lcd", "7segment", "ledarray", "joystick"]

    return render(request, 'sensor/raspi.html', {
        'pi_name': pi_name,
        'pi_list': pi_list,
        'sensors': sensors
    })


def sensor_name(request, sensor_name, pi_name):
    sensors = ["dht11", "ultrasonic", "8x8matrix", "buzzer",
               "relay", "lcd", "7segment", "ledarray", "joystick"]
    return render(request, 'sensor/sensor.html', {
        'pi_name': pi_name,
        'sensor_name': sensor_name,
        'sensors': sensors,
        'url': f'sensor/sensors/{sensor_name}.html',
    })
