import os
from django.db import models
from datetime import datetime
from django.forms import model_to_dict
from config.settings import MEDIA_URL, STATIC_URL
from core.models import BaseModel
from crum import get_current_user

AZURE_STATIC="https://contenedordasix.blob.core.windows.net/django-dasix"+STATIC_URL

gender_choices = (
    ('male','Masculino'),
    ('female','Femenino'),
)
    
class Categoria(BaseModel):
    Nombre=models.CharField(max_length=150, unique=True)
    Descripcion=models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.Nombre
    
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        user=get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation=user
        else:
            self.user_update=user
        super(Categoria, self).save()
    
    def toJSON(self):
        item= model_to_dict(self,exclude=['user_creation', 'user_update'])
        return item
    
    class Meta:
        verbose_name="Categoria"
        verbose_name_plural="Categorias"
        ordering=['id']

class Producto(models.Model):
    Nombre=models.CharField(max_length=150,unique=True)
    cate=models.ForeignKey(Categoria, on_delete=models.CASCADE, verbose_name='Categoria')
    if "WEBSITE_HOSTNAME" in os.environ:
        image=models.ImageField(upload_to=f'{MEDIA_URL}producto/%y/%m/%d',null=True, blank=True, verbose_name='Imagen')
    else:
        image=models.ImageField(upload_to='producto/%y/%m/%d',null=True, blank=True, verbose_name='Imagen')
    Stock=models.IntegerField(default=0, verbose_name='Stock')
    pvp=models.DecimalField(default=0.00, max_digits=9,decimal_places=2, verbose_name='Precio de venta')

    def __str__(self):
        return self.Nombre
    
    def get_image(self):
        if self.image:
            return self.image.url
        AZURE_STATIC
        if "WEBSITE_HOSTNAME" in os.environ:
            return '{}{}'.format(AZURE_STATIC, 'img/empty.webp')
        else:
            return '{}{}'.format(STATIC_URL, 'img/empty.webp')
    class Meta:
        verbose_name='Producto'
        verbose_name_plural='Productos'
        ordering=['id']
    
    def toJSON(self):
        item = model_to_dict(self)
        item['full_nombre']='{} / {}'.format(self.Nombre, self.cate.Nombre)
        item['cate']={"id":self.cate.id,"Nombre":self.cate.Nombre}
        item['image']=self.get_image()
        item['pvp']=format(self.pvp, '.2f')
        return item

class Cliente(models.Model):
    Nombres=models.CharField(max_length=150)
    Apellidos=models.CharField(max_length=150)
    Cedula=models.CharField(max_length=10, unique=True)
    Cumple=models.DateField(default=datetime.now, verbose_name='Fecha de Nacimiento')
    Direccion=models.CharField(max_length=150, null=True, blank=True)
    Sexo=models.CharField(max_length=10, choices=gender_choices,default='male')

    def __str__(self):
        return self.Nombres
    
    def get_nombre(self):
        return self.Nombres + " " + self.Apellidos

    def toJSON(self):
        item = model_to_dict(self)
        item['Sexo'] = {'id':self.Sexo,'name':self.get_Sexo_display()} 
        item['Cumple'] = self.Cumple.strftime('%Y-%m-%d')
        return item
    
    class Meta:
        verbose_name='Cliente'
        verbose_name_plural='Clientes'
        ordering=['id']

class Proveedor(models.Model):
  Nombres=models.CharField(max_length=150)
  Identificacion=models.CharField(max_length=10, unique=True)
  Direccion=models.CharField(max_length=150, null=True, blank=True)
  Telefono=models.CharField(max_length=10, null=False, blank=False)
  Correo=models.EmailField(null=False, blank=False)

  def __str__(self):
      return self.Nombres
  
  def toJSON(self):
      return model_to_dict(self)
  
  class Meta:
      verbose_name='Proveedor'
      verbose_name_plural='Proveedores'
      ordering=['id']

class Venta(models.Model):
    Cli=models.ForeignKey(Cliente, on_delete=models.CASCADE)
    Date_joined=models.DateField(default=datetime.now)
    Subtotal=models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    Iva=models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    Total=models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.Cli.Nombres
    
    class Meta:
        verbose_name='Venta'
        verbose_name_plural='Ventas'
        ordering=['id']

    def toJSON(self):
        item=model_to_dict(self)
        #item['Cli']={"id": self.Cli.id, "Nombres": self.Cli.Nombres}
        item['Cli']=self.Cli.toJSON()
        item['Date_joined']=self.Date_joined.strftime('%Y-%m-%d')
        item['Subtotal']=format(self.Subtotal, '.2f')
        item['Iva']=format(self.Iva, '.2f')
        item['Total']=format(self.Total, '.2f')
        item['det']=[i.toJSON() for i in self.detalleventa_set.all()]
        return item
    
    def delete(self, usign=None, keep_parents=False):
        for det in self.detalleventa_set.all():
            det.Produ.Stock += det.Cantidad
            det.Produ.save()
        super(Venta, self).delete()

class DetalleVenta(models.Model):
    Venta=models.ForeignKey(Venta, on_delete=models.CASCADE)
    Produ=models.ForeignKey(Producto, on_delete=models.CASCADE)
    Precio=models.DecimalField(default=0.00, max_digits=9,decimal_places=2)
    Cantidad=models.IntegerField(default=0)
    Subtotal=models.DecimalField(default=0.00, max_digits=9,decimal_places=2)

    def __str__(self):
        return self.Produ.Nombre
    
    class Meta:
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalle de Ventas'
        ordering = ['id']

    def toJSON(self):
        item=model_to_dict(self, exclude=['Venta'])
        item['Produ']=self.Produ.toJSON()
        item['Precio']=format(self.Precio, '2f')
        item['Subtotal']=format(self.Subtotal, '2f')
        return item