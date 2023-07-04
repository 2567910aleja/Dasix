'''
from config.wsgi import *
from core.erp.models import Type
#from django.test import TestCase

#Listar
query=Type.objects.all()
print(query)

#Insertar
t=Type()
t.Nombre="prueba"
t.save()
'''