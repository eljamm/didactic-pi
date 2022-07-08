from django.shortcuts import render


def index(request):
    return render(request, 'sensor/index.html')


def read_value(request, sensor_name):
    return render(request, 'sensor/read.html', {
        'sensor_name': sensor_name,
        'sensors': ['temperature', 'ultrasound']
    })
