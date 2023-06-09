from typing import Any
from django.contrib.auth.decorators import *
from django.shortcuts import render, redirect
from core.erp.models import *
from django.views.generic import *
from django.utils.decorators import method_decorator
from django.http import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import *
from core.erp.forms import *
from django.urls import *

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

    def post(self, request, *args, **kwargs):
        data={}
        try:
            data= Categoria.objects.get(pk=request.POST['id']).toJSON()
        except Exception as e:
            data['error']=str (e)

        return JsonResponse(data)
    

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['title']='Listado de categorias'
        context['create_url']=reverse_lazy('erp:categoria_create')
        context['list_url']=reverse_lazy('erp:categoria_list')
        context['entity']='Categorias'
        #context['object_list']=Producto.objects.all()
        return context
    
class CategoriaCreateView(CreateView):
    model=Categoria
    form_class=CategoriaForm
    template_name='Categoria/create.html'
    success_url=reverse_lazy('erp:categoria_list')

    def post(self, request, *args, **kwargs):
        data={}
        try:
            action=request.POST['action']
            if action == 'add':
                form=self.get_form()
                if form.is_valid():
                    form.save()
                else:
                    data['error']=form.errors
            else:
                data['error']='No ha ingresado a ninguna opcion'
            data= Categoria.objects.get(pk=request.POST['id']).toJSON()
        except Exception as e:
            data['error']=str (e)

        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['title']='Creacion de categorias'
        context['entity']='Categorias'
        context['list_url']=reverse_lazy('erp:categoria_list')
        context['action']='add'
        return context 