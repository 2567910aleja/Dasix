from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View
from django.views.decorators.csrf import *
from django.utils.decorators import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.sessions.models import Session

# funciones
def verificar_session_id(session_id):
    try:
        session=Session.objects.get(session_key=session_id)
        data=session.get_decoded()
        user_id=data.get('_auth_user_id',None)
        return user_id
    except Session.DoesNotExist:
        return None

# vistas
class InicioSesion(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data={}
        accion=request.POST.get("accion")
        if accion=="iniciarsesion":
            try:
                usuario=request.POST.get('usuario')
                password=request.POST.get('password')

                if usuario and password:
                    if User.objects.filter(username=usuario).exists():
                        user=authenticate(request, username=usuario, password=password)
                        if user is not None:
                            login(request, user)
                            data['sessionid']=request.session.session_key
                        else:
                            data['error']=["Contraseña incorrecta"]
                    else:
                        data['error']=["El usuario no existe"]
                else:
                    data['error']=[]
                    if not usuario:
                        data['error'].append("No se envio un nombre de usuario")
                    if not password:
                        data['error'].append("No se envio la contraseña")
            except Exception as e:
                data['error']=["Ocurrio un error: "+str(e)]
        elif accion=="verificarsession":
            session_id=request.POST.get("session_id")
            user_id = verificar_session_id(session_id)
            if user_id is not None:
                data['respuesta']="valido"
            else:
                data['respuesta']='invalido'
        return JsonResponse(data)


class CerrarSesion(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data={}
        session_id=request.POST.get("session_id")
        user_id=verificar_session_id(session_id)
        if user_id is not None:
            Session.objects.get(session_key=session_id).delete()
            data['respuesta']="valido"
        else:
            data['respuesta']="sesion invalida"
        return JsonResponse(data)