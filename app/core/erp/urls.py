from django.urls import path
from core.erp.views import *


urlpatterns = [
  path('uno/',PrimerVista, name='Vista1'),
  path('dos/',SegundaVista, name='Vista2'),
]        