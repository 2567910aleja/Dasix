from django.urls import path
from core.erp.views.categoria.views import *

urlpatterns = [
  path('categoria/list/', CategoriaListView.as_view(), name='categoria_list'),
]        