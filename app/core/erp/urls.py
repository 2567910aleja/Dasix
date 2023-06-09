from django.urls import path
from core.erp.views.categoria.views import *

app_name = 'erp'

urlpatterns = [
  path('categoria/list/', CategoriaListView.as_view(), name='categoria_list'),
  path('categoria/list2/', categoria_list, name='categoria_list2'),
  path('categoria/add/', CategoriaCreateView.as_view(), name='categoria_create'),
]        