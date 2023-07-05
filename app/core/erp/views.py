from django.shortcuts import render
from core.erp.models import *

def PrimerVista(request):
    data={'name':'Ale',
          'Categorias':Categoria.objects.all()
          }
    return render(request,'home.html',data)

def SegundaVista(request):
    data={'name':'Ale',
          'Productos':Producto.objects.all()
          }
    return render(request,'segundo.html',data)