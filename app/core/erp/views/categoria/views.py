from django.contrib.auth.decorators import *
from django.shortcuts import render, redirect
from core.erp.models import *
from django.views.generic import *
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import *

def categoria_list(request):
    data={
        'title':'Listado de categorias',
        'categorias':Categoria.objects.all()
    }
    return render(request,'categoria/list.html',data)

class CategoriaListView(ListView):
    model=Categoria
    template_name='categoria/list.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, *args, **kwargs):
        data={'name':'Ale'}
        return JsonResponse(data)
    

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['title']='Listado de categorias'
        #context['object_list']=Producto.objects.all()
        return context