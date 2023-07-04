from config.wsgi import *
from core.erp.models import *
#from django.test import TestCase

#Insertar
#valores=["Lacteos","Cereales","Carnes"]
#for valor in valores:
  #c=Categoria()
  #Porque estoy recorriendo el arreglo
  #c.Nombre=valor
  #c.save()
  
#LISTAR
#print(Categoria.objects.all())
#for i in Categoria.objects.filter():
    #print(i)

valores=[["Yogurt",2],["Arroz",3],["Pechuga de pollo",4]]
for valor in valores: 
  p=Producto()
  #Porque estoy recorriendo el arreglo
  p.Nombre=valor[0]
  p.cate_id=valor[1]
  p.save()