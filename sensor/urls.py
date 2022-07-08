from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('read/<str:sensor_name>/', views.read_value, name='read_value'),
]
