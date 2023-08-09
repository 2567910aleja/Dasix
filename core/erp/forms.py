from django.forms import *

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
        
        exclude=['user_creation','user_update']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
    
    #def clean(self):
        #cleaned=super().clean()
        #if len(cleaned['Nombre']) <=50:
            #raise forms.ValidationError('Validacion xxx')
            #self.add_error('Nombre', 'Le faltan caracteres')
        #print(cleaned)
       # return cleaned
    
class ProductoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = Producto
        fields = '__all__'
        widgets = {
            'Nombre': TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre',
                }
            ),
        }
    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

class TestForm(Form):
    categorias = ModelChoiceField(queryset=Categoria.objects.all(), widget=Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))

    productos = ModelChoiceField(queryset=Producto.objects.none(), widget=Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))

    #search=CharField(widget=TextInput(attrs={
        #'class': 'form-control',
        #'placeholder': 'Ingrese una descripcion'
   # }))

    search = ModelChoiceField(queryset=Producto.objects.none(), widget=Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))

class ClienteForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Nombres'].widget.attrs['autofocus'] = True

    class Meta:
        model = Cliente
        fields = '__all__'
        widgets = {
            'Nombres': TextInput(
                attrs={
                    'placeholder': 'Ingrese sus nombres',
                }
            ),
            'Apellidos': TextInput(
                attrs={
                    'placeholder': 'Ingrese sus apellidos',
                }
            ),
            'Cedula': TextInput(
                attrs={
                    'placeholder': 'Ingrese su cedula',
                }
            ),
            'Cumple': DateInput(format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                }
            ),
            'Direccion': TextInput(
                attrs={
                    'placeholder': 'Ingrese su direccion',
                }
            ),
            'Sexo': Select()
        }
        exclude = ['user_updated', 'user_creation']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

    # def clean(self):
    #     cleaned = super().clean()
    #     if len(cleaned['name']) <= 50:
    #         raise forms.ValidationError('Validacion xxx')
    #         # self.add_error('name', 'Le faltan caracteres')
    #     return cleaned

class VentaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class']= 'form-control'
            form.field.widget.attrs['autocomplete']= 'off'
        self.fields['Cli'].widget.attrs['autofocus'] = True
        self.fields['Cli'].widget.attrs['class'] = 'form-control select2'
        self.fields['Cli'].widget.attrs['style'] = 'width: 100%'

    class Meta:
        model = Venta
        fields = '__all__'
        widgets = {
            'Cli': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%'
            }),
            'Date_joined': DateInput(format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                }
            ),  
        }