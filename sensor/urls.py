from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:pi_name>/', views.pi_name, name='pi_name'),
    path('<str:pi_name>/<str:sensor_name>', views.sensor_name, name='sensor_name'),
]
