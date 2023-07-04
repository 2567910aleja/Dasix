from django.shortcuts import render
from core.erp.models import *

def PrimerVista(request):
    data={'name':'Ale',
          'Categorias':Categoria.objects.all()
          }
    return render(request,'index.html',data)