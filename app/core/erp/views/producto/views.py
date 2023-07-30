from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.erp.forms import ProductoForm
from core.erp.models import Producto


class ProductoListView(ListView):
    model = Producto
    template_name = 'producto/list.html'

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
                for i in Producto.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] ='Ha ocurrido un error'
        except Exception as e:
            data['error']=str (e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Productos'
        context['create_url'] = reverse_lazy('erp:producto_create')
        context['list_url'] = reverse_lazy('erp:producto_list')
        context['entity'] = 'Productos'
        return context


class ProductoCreateView(CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'producto/create.html'
    success_url = reverse_lazy('erp:producto_list')

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
         data = {}
         try:
             action = request.POST['action']
             if action == 'add':
                 form = self.get_form()
                 data = form.save()
             else:
                 data['error'] = 'No ha ingresado a ninguna opción'
         except Exception as e:
             data['error'] = str(e)
         return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de un Producto'
        context['entity'] = 'Productos'
        context['list_url'] = reverse_lazy('erp:producto_list')
        context['action'] = 'add'
        return context


class ProductoUpdateView(UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'producto/create.html'
    success_url = reverse_lazy('erp:producto_list')

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de un Producto'
        context['entity'] = 'Productos'
        context['list_url'] = reverse_lazy('erp:producto_list')
        context['action'] = 'edit'
        return context


class ProductoDeleteView(DeleteView):
    model = Producto
    template_name = 'producto/delete.html'
    success_url = reverse_lazy('erp:producto_list')

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de un Producto'
        context['entity'] = 'Productos'
        context['list_url'] = reverse_lazy('erp:producto_list')
        return context