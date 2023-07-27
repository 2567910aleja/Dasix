from django.urls import path
from core.erp.views.categoria.views import *
from core.erp.views.dashboard.views import *

app_name = 'erp'

urlpatterns = [
    #Categoria
  path('categoria/list/', CategoriaListView.as_view(), name='categoria_list'),
  path('categoria/add/', CategoriaCreateView.as_view(), name='categoria_create'),
  path('categoria/update/<int:pk>/', CategoriaUpdateView.as_view(), name='categoria_update'),
  path('categoria/delete/<int:pk>/', CategoriaDeleteView.as_view(), name='categoria_delete'),
  path('categoria/form/', CategoriaFormView.as_view(), name='categoria_form'),

  #Home
  path('dashboard/', DashboardView.as_view(), name='dashboard'),
]        