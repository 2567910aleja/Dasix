from config.wsgi import *
from core.erp.models import *
#from django.test import TestCase

#Insertar
valores=["Lacteos","Cereales","Carnes"]
for valor in valores:
  c=Categoria()
  #Porque estoy recorriendo el arreglo
  c.nombre=valor
  c.save()
  
#LISTAR
print(Categoria.objects.all())
for i in Categoria.objects.filter():
    print(i)


