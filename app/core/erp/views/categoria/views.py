from typing import Any, Dict
from django.shortcuts import render
from core.erp.models import *
from django.views.generic import *

def categoria_list(request):
    data={
        'title':'Listado de categorias',
        'categorias':Categoria.objects.all()
    }
    return render(request,'categoria/list.html',data)

class CategoriaListView(ListView):
    model=Categoria
    template_name='categoria/list.html'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['title']='Listado de categorias'
        #context['object_list']=Producto.objects.all()
        return context