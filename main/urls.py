from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:id>", views.sensor_id, name="sensors"),
    path("data/", views.add_data, name="add_data"),
    path("sensor/", views.add_sensor, name="add_sensor"),
]
