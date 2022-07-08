from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:id>", views.sensor_id, name="sensors"),
    path("add_data/", views.add_data, name="add_data"),
    path("add_sensor/", views.add_sensor, name="add_sensor"),
]
