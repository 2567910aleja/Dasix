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
            action=request.POST['action']
            if action =='searchdata':
                data=[]
                for i in Categoria.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] ='Ha ocurrido un error'
        except Exception as e:
            data['error']=str (e)
        return JsonResponse(data, safe=False)
    

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

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data={}
        try:
            action=request.POST['action']
            if action == 'add':
                form=self.get_form()
                data=form.save()
            else:
                data['error']='No ha ingresado a ninguna opcion'
        except Exception as e:
            data['error']=str (e)
        return JsonResponse(data)

    #     print(request.POST)
    #     form = CategoriaForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return HttpResponseRedirect(self.success_url)
    #     self.object = None
    #     context = self.get_context_data(**kwargs)
    #     context['form'] = form
    #     return render(request, self.template_name, context

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['title']='Creacion de categorias'
        context['entity']='Categorias'
        context['list_url']=reverse_lazy('erp:categoria_list')
        context['action']='add'
        return context 

class CategoriaUpdateView(UpdateView):
    model=Categoria
    form_class=CategoriaForm
    template_name='Categoria/create.html'
    success_url=reverse_lazy('erp:categoria_list')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object=self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data={}
        try:
            action=request.POST['action']
            if action == 'edit':
                form=self.get_form()
                data=form.save()
            else:
                data['error']='No ha ingresado a ninguna opcion'
        except Exception as e:
            data['error']=str (e)

        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['title']='Edicion de categorias'
        context['entity']='Categorias'
        context['list_url']=reverse_lazy('erp:categoria_list')
        context['action']='edit'
        return context 
    
class CategoriaDeleteView(DeleteView):
    model=Categoria
    template_name='Categoria/delete.html'
    success_url=reverse_lazy('erp:categoria_list')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object=self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data={}
        try:
            self.object.delete()
        except Exception as e:
            data['error']=str(e)
        return JsonResponse(data)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminacion de una Categoria'
        context['entity'] = 'Categorias'
        context['list_url'] = reverse_lazy('erp:categoria_list')
        return context