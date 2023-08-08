from core.apiAndroid.views import InicioSesion, CerrarSesion, Registrar, cargaDatos
from django.urls import path

app_name = 'api'

urlpatterns = [
    path('iniciosesion/',InicioSesion.as_view(),name="iniciosesion"),
    path('cerrarsesion/',CerrarSesion.as_view(),name="cerrarsesion"),
    path('registrar/',Registrar.as_view(),name="registrar"),
    path("cargardatos/",cargaDatos.as_view(),name="cargardatos")
]