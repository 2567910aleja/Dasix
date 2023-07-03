from django.db import models

class Type(models.Model):
    Nombre=models.CharField(max_length=50)

    def __str__(self):
        return self.Nombre
    
    class Meta:
        verbose_name="Tipo"
        verbose_name_plural="Tipos"
        ordering=['id']


class Categoria(models.Model):
    Nombre=models.CharField(max_length=50)

    def __str__(self):
        return self.Nombre
    
    class Meta:
        verbose_name="Categoria"
        verbose_name_plural="Categorias"
        ordering=['id']


class Usuario(models.Model):
    categ=models.ManyToManyField(Categoria)
    type=models.ForeignKey(Type, on_delete=models.PROTECT)
    Identificacion=models.CharField(max_length=15, unique=True)
    Nombres=models.CharField(max_length=50)
    Apellidos=models.CharField(max_length=50)
    Direccion=models.CharField(max_length=50)
    Correo=models.EmailField
    Contraseña=models.CharField(max_length=250, unique=True)
    
    def __str__(self):
        return self.Nombres
    
    class Meta:
        verbose_name="Usuario"
        verbose_name_plural="Usuarios"
        ordering=['id']