from core.apiAndroid.views import InicioSesion
from django.urls import path

app_name = 'api'

urlpatterns = [
    path('iniciosesion/',InicioSesion.as_view(),name="iniciosesion")
]