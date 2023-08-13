from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.erp.mixins import ValidatePermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from core.erp.models import Venta, Producto, DetalleVenta
from core.erp.forms import VentaForm
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json

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
                    det.venta_id=venta_id
                    det.produ_id=i['id']
                    det.cant=int(i['cant'])
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
