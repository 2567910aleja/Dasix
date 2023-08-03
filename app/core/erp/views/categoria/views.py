from core.erp.models import *
from django.views.generic import *
from django.utils.decorators import *
from django.http import *
from django.views.decorators.csrf import *
from core.erp.forms import *
from django.urls import *
from django.contrib.auth.decorators import * 
from core.erp.mixins import IsSuperuserMixin 


class CategoriaListView(IsSuperuserMixin,ListView):

    model=Categoria
    template_name='categoria/list.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
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
    @method_decorator(login_required)
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
    @method_decorator(login_required)
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
    @method_decorator(login_required)
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

class CategoriaFormView(FormView):
    form_class=CategoriaForm
    template_name='categoria/create.html'
    success_url=reverse_lazy('erp:categoria_list')

    def form_valid(self, form):
        print(form.is_valid())
        print(form)
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.is_valid())
        print(form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['title']='Form categorias'
        context['entity']='Categorias'
        context['list_url']=reverse_lazy('erp:categoria_list')
        context['action']='add'
        return context 