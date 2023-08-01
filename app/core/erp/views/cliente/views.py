from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from core.erp.models import Cliente
from core.erp.forms import ClienteForm 


class ClienteView(TemplateView):
    template_name = 'cliente/list.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Cliente.objects.all():
                    data.append(i.toJSON())
            elif action=='add':
                cli=Cliente()
                cli.Nombres=request.POST['Nombres']
                cli.Apellidos=request.POST['Apellidos']
                cli.Cedula=request.POST['Cedula']
                cli.Cumple=request.POST['Cumple']
                cli.Direccion=request.POST['Direccion']
                cli.Sexo=request.POST['Sexo']
                cli.save()
            elif action=='edit':
                cli=Cliente.objects.get(pk=request.POST['id'])
                cli.Nombres=request.POST['Nombres']
                cli.Apellidos=request.POST['Apellidos']
                cli.Cedula=request.POST['Cedula']
                cli.Cumple=request.POST['Cumple']
                cli.Direccion=request.POST['Direccion']
                cli.Sexo=request.POST['Sexo']
                cli.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Clientes'
        context['list_url'] = reverse_lazy('erp:cliente')
        context['entity'] = 'Clientes'
        context['form']=ClienteForm()
        return context