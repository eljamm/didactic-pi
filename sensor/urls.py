from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add-pi/', views.add_pi, name='add_pi'),
    path('remove-pi/', views.remove_pi, name='remove_pi'),
    path('<str:pi_name>/', views.pi_name, name='pi_name'),
    path('<str:pi_name>/<str:sensor_name>/',
         views.sensor_name, name='sensor_name'),
    path('<str:pi_name>/<str:sensor_name>/<str:extra_function>/',
         views.sensor_extra, name='sensor_extra'),
]
