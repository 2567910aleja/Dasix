from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View
from django.views.decorators.csrf import *
from django.utils.decorators import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.sessions.models import Session
from core.erp.models import Cliente
from core.user.models import User

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
    
class Registrar(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data={}
        #Obtengo los valores
        nombre=request.POST.get('usuario', "")
        password=request.POST.get('password', "")
        confiPassword=request.POST.get('passwordConfirmacion', "")
        # Valido si alguno esta vacio
        if nombre=="":
            data['error']=['El nombre no puede estar vacio']
            return JsonResponse(data)
        # valido que el usuario no exista
        if User.objects.filter(username__iexact=nombre).exists():
            data['error']="El usuario ya existe"
            return JsonResponse(data)
        if password=="":
            data['error']=['La contraseña no puede estar vacia']
            return JsonResponse(data)
        if confiPassword=="":
            data['error']=['La confirmacion de contraseña no coincide']
            return JsonResponse(data)
        #Valido que la contraseña tenga más de 8 caracteres y que el password sea igual al confiPassword
        if len(password)<8:
            data['error']=['La contraseña es menor a 8 caracteres']
            return JsonResponse(data)
        if password!=confiPassword:
            data['error']=['Las contraseñas no coinciden']
            return JsonResponse(data)
        
        #Si todo esta bien creo o registro el usuario
        #La funcion set_password encripta la contraseña y se la asigna al usuario
        try:
            usuarioCrear=User()
            usuarioCrear.username=nombre
            usuarioCrear.set_password(password)
            usuarioCrear.save()
            data['respuesta']="creado"
        except Exception as e:
            data['error']=[str(e)]
        
        return JsonResponse(data)

class cargaDatos(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data={}
        # verificar el session_id
        session_id=request.POST.get("session_id","")
        if session_id=="" or verificar_session_id(session_id) is None:
            data['error']=['session invalida']
            return JsonResponse(data)

        accion = request.POST.get("accion")
        # Aleja
        if accion=="tiposUsuarios":
            data['tiposUsuarios']=['cliente','usuario']
        elif accion=="cargarUsuarios":
            usuarios=User.objects.all()
            data['usuarios']=[]
            for user in usuarios:
                data['usuarios'].append(user.toJSON())              
        elif accion=="cargarClientes":
            clientes=Cliente.objects.all()
            data['clientes']=[]
            for client in clientes:
                data['clientes'].append(client.toJSON())
        else:
            data['error']=['No se envio una accion']
        return JsonResponse(data)