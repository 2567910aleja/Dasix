from django.db import models
from datetime import datetime
from django.forms import model_to_dict
from config.settings import MEDIA_URL, STATIC_URL

gender_choices = (
    ('male','Masculino'),
    ('female','Femenino'),
)
    
class Categoria(models.Model):
    Nombre=models.CharField(max_length=150, unique=True)
    Descripcion=models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return 'Nombre: {}'.format(self.Nombre)
    
    def toJSON(self):
        item= model_to_dict(self)
        return item
    
    class Meta:
        verbose_name="Categoria"
        verbose_name_plural="Categorias"
        ordering=['id']

class Producto(models.Model):
    Nombre=models.CharField(max_length=150,unique=True)
    cate=models.ForeignKey(Categoria, on_delete=models.CASCADE, verbose_name='Categoria')
    image=models.ImageField(upload_to='producto/%y/%m/%d',null=True, blank=True, verbose_name='Imagen')
    pvp=models.DecimalField(default=0.00, max_digits=9,decimal_places=2, verbose_name='Precio de venta')

    def __str__(self):
        return self.Nombre
    
    def get_image(self):
        if self.image:
            return '{}{}'.format(MEDIA_URL, self.image)
        return '{}{}'.format(STATIC_URL, 'img/empty.webp')
    class Meta:
        verbose_name='Producto'
        verbose_name_plural='Productos'
        ordering=['id']

class Cliente(models.Model):
    Nombres=models.CharField(max_length=150)
    Apellidos=models.CharField(max_length=150)
    Cedula=models.CharField(max_length=10, unique=True)
    Cumple=models.DateField(default=datetime.now, verbose_name='Fecha de Nacimiento')
    Direccion=models.CharField(max_length=150, null=True, blank=True)
    Sexo=models.CharField(max_length=10, choices=gender_choices,default='male')

    def __str__(self):
        return self.Nombres
    
    class Meta:
        verbose_name='Cliente'
        verbose_name_plural='Clientes'
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
