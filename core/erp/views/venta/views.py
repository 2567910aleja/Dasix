from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.erp.mixins import ValidatePermissionRequiredMixin
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from core.erp.models import Venta, Producto, DetalleVenta
from core.erp.forms import VentaForm
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json

class VentaListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Venta
    template_name = 'venta/list.html'
    permission_required = 'erp.view_venta'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Venta.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data={}
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Ventas'
        context['create_url'] = reverse_lazy('erp:venta_create')
        context['list_url'] = reverse_lazy('erp:venta_list')
        context['entity'] = 'Ventas'
        return context

class VentaCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model= Venta
    form_class= VentaForm
    template_name='venta/create.html'
    success_url=reverse_lazy('index')
    permission_required='erp.add_venta'
    url_redirect=success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
         return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search-productos':
                data=[]
                produ=Producto.objects.filter(Nombre__icontains=request.POST['term'])[0:10]
                for i in produ:
                    item=i.toJSON()
                    item['value']=i.Nombre
                    data.append(item)
            elif action=='add':
                # El transaction.atomic sirve para cuando hay un error no se guarde solo una parte, la funcion
                # devuelve la accion hasta el principio y no se guarda nada
                with transaction.atomic():
                    ventas=json.loads(request.POST['ventas'])

                    venta=Venta()
                    venta.Date_joined=ventas['Date_joined']
                    venta.Cli_id=ventas['Cli']
                    venta.Subtotal=float(ventas['Subtotal'])
                    venta.Iva=float(ventas['Iva'])
                    venta.Total=float(ventas['Total'])
                    venta.save()

                    for i in ventas['productos']:
                        det=DetalleVenta()
                        det.Venta_id=venta.id
                        det.Produ_id=i['id']
                        det.Cantidad=int(i['cant'])
                        det.Precio=float(i['pvp'])
                        det.Subtotal=float(i['Subtotal'])
                        det.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data={}
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de una Venta'
        context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context

class VentaDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Venta
    template_name = 'venta/delete.html'
    success_url = reverse_lazy('erp:venta_list')
    permission_required = 'erp.delete_venta'
    url_redirect = success_url

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
        context['title'] = 'Eliminación de una Venta'
        context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        return context