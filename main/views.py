from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.utils import timezone
from .models import Sensor
from .forms import AddSensor, AddData
import logging


def index(response):
    return render(response, "main/index.html", {})


def sensor_id(response, id):
    sensor = Sensor.objects.get(id=id)
    return render(response, "main/list.html", {"sensor": sensor})


def add_sensor(response):
    if response.method == "POST":
        form = AddSensor(response.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            datetime = timezone.now()

            sensor = Sensor(name=name)
            sensor.save()

            logging.debug(f"({sensor_id}) {sensor.name} - {datetime}")

        return HttpResponseRedirect(f"/{sensor.id}")

    else:
        form = AddSensor()
    return render(response, "main/sensor.html", {"form": form, "action": "/add_sensor/"})


def add_data(response):
    if response.method == "POST":
        form = AddData(response.POST)
        if form.is_valid():
            sensor_id = form.cleaned_data["sensor_id"]
            data = form.cleaned_data["data"]
            datetime = timezone.now()

            sensor = Sensor.objects.get(id=sensor_id)
            sensor.item_set.create(datetime=datetime, data=data)
            sensor.save()

            logging.debug(
                f"({sensor.id}) {sensor.name} - {datetime} - {data}", )

        return HttpResponseRedirect(f"/{sensor.id}")

    else:
        form = AddData()
    return render(response, "main/data.html", {"form": form, "action": "/add_data/"})
