from django.forms import ModelForm
from core.erp.models import *

class CategoriaForm(ModelForm):
    class Meta:
        model=Categoria
        fields='__all__'