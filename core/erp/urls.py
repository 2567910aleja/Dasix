from django.urls import path
from core.erp.views.categoria.views import *
from core.erp.views.cliente.views import *
from core.erp.views.venta.views import *
from core.erp.views.dashboard.views import *
from core.erp.views.producto.views import *
from core.erp.views.tests.views import TestView

app_name = 'erp'

urlpatterns = [
    #Categoria
    path('categoria/list/', CategoriaListView.as_view(), name='categoria_list'),
    path('categoria/add/', CategoriaCreateView.as_view(), name='categoria_create'),
    path('categoria/update/<int:pk>/', CategoriaUpdateView.as_view(), name='categoria_update'),
    path('categoria/delete/<int:pk>/', CategoriaDeleteView.as_view(), name='categoria_delete'),

    # producto
    path('producto/list/', ProductoListView.as_view(), name='producto_list'),
    path('producto/add/', ProductoCreateView.as_view(), name='producto_create'),
    path('producto/update/<int:pk>/', ProductoUpdateView.as_view(), name='producto_update'),
    path('producto/delete/<int:pk>/', ProductoDeleteView.as_view(), name='producto_delete'),

    # cliente
    path('cliente/list/', ClienteListView.as_view(), name='cliente_list'),
    path('cliente/add/', ClienteCreateView.as_view(), name='cliente_create'),
    path('cliente/update/<int:pk>/', ClienteUpdateView.as_view(), name='cliente_update'),
    path('cliente/delete/<int:pk>/', ClienteDeleteView.as_view(), name='cliente_delete'),

    #Home
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    #test
    path('tests/', TestView.as_view(), name='tests'),

    #Venta
    path('venta/list/', VentaListView.as_view(), name='venta_list'),
    path('venta/add/', VentaCreateView.as_view(), name='venta_create'),
    path('venta/delete/<int:pk>/', VentaDeleteView.as_view(), name='venta_delete'),
]        