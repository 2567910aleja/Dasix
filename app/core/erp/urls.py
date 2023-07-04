from django.urls import path
from core.erp.views import *

urlpatterns = [
  path('uno/',PrimerVista),
  path('dos/',PrimerVista),
]        