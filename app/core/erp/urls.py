from django.urls import path
from core.erp.views.categoria.views import *

urlpatterns = [
  path('categoria/list/', categoria_list, name='categoria_list'),
]        