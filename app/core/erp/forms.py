from typing import Any, Dict, Mapping, Optional, Type, Union
from django.core.files.base import File
from django.db.models.base import Model
from django.forms import *
from django.forms.utils import ErrorList
from core.erp.models import *

class CategoriaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #for form in self.visible_fields():
            #form.field.widget.attrs['class']= 'form-control'
            #form.field.widget.attrs['autocomplete']= 'off'
        self.fields['Nombre'].widget.attrs['autofocus']= True


    class Meta:
        model=Categoria
        fields='__all__'
        labels={
            'Nombre':'Nombre'
        }
        widgets={
            'Nombre': TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre',
                }
            ),
            'Descripcion': Textarea(
                attrs={
                    'placeholder': 'Ingrese una descripcion',
                    'rows':3,
                    'cols':3
                }
            )
        }