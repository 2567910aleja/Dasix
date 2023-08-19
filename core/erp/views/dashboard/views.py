from datetime import datetime

from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from core.erp.models import Venta, Producto, DetalleVenta

from random import randint

class DashboardView(TemplateView):
    template_name= 'dashboard.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'get_grafico_venta_mes':
                data = {
                    'name': 'Porcentaje de venta',
                    'showInLegend': False,
                    'colorByPoint': True,
                    'data': self.get_grafico_venta_mes()
                }
            elif action == 'get_grafico_producto_venta_mes':
                data = {
                    'name': 'Porcentaje',
                    'colorByPoint': True,
                    'data': self.get_grafico_producto_venta_mes(),
                }
            elif action == 'get_grafico_online':
                data = {'y': randint(1, 100)}
                print(data)
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_grafico_venta_mes(self):
        data=[]
        try:
            year=datetime.now().year
            for m in range(1,13):
                Total=Venta.objects.filter(Date_joined__year=year, Date_joined__mes=m).aget(r=Coalesce(Sum('Total'),0)).get('r')
                data.append(float(Total))
        except:
            pass
        return data
    
    def get_grafico_producto_venta_mes(self):
        data = []
        year = datetime.now().year
        mes = datetime.now().month
        try:
            for p in Producto.objects.all():
                total = DetalleVenta.objects.filter(Venta__Date_joined__year=year, Venta__Date_joined__mes=mes, Produ_id=p.id).aggregate(r=Coalesce(Sum('Subtotal'), 0)).get('r')
                if total > 0:
                    data.append({
                        'name': p.Nombre,
                        'y': float(total)
                    })
        except:
            pass
        return data

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['panel']='Panel de administrador'
        context['grafico_venta_mes']=self.get_grafico_venta_mes()
        return context