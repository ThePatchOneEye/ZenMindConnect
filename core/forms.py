from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Comment, Post, Especialidad, Psicologo, Horarios, Agenda, Persona
from datetime import date



class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = ['rut', 'nombre', 'apellido', 'fechaNac', 'correo', 'telefono']
        labels = {
            'rut': 'Rut',
            'nombre': 'Nombre',
            'apellido': 'Apellido',
            'fechaNac': 'Fecha de Nacimiento',
            'correo': 'Correo Electrónico',
            'telefono': 'Teléfono',
        }
        widgets = {
            'rut': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese rut', 'id': 'rut'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su nombre', 'id': 'nombre'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su apellido', 'id': 'apellido'}),
            'fechaNac': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su fecha de nacimiento', 'id': 'fechaNac'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ejemplo etzio@gmail.com', 'id': 'correo'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ejemplo +56951393925', 'id': 'telefono'}),
        }

class CommentForm(forms.ModelForm):
    nombre_del_autor = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'})
    )

    class Meta:
        model = Comment
        fields = ['name', 'body']
        labels ={
            'name':  'Ingrese nombre de titulo del comentario:', 
            'body': 'Agregue un comentario:',
        }
        widgets={
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control', 
                    'id': 'slug'
                }
            ), 
            'body': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'id': 'body'
                }
            ),
        }

class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['slug'].widget = forms.HiddenInput()

    def clean_slug(self):
        # Obtén el valor actual del campo slug
        slug = self.cleaned_data.get('slug')

        # Verifica si ya existe un objeto Post con el mismo slug
        if Post.objects.filter(slug=slug).exists():
            raise forms.ValidationError('El slug ya existe. Debe ser único.')

        # Devuelve el valor limpio del campo slug
        return self.cleaned_data['slug']

    class Meta:
        model = Post
        fields = ['title', 'slug', 'intro', 'body', 'hilo']
        labels = {
            'title': 'Titulo del post', 
            'slug': 'slug es parte de tu username', 
            'intro': 'intro del post',
            'body': 'Body del post ',
            'hilo': 'Tema de su post ',    
        }
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control', 
                    'placeholder': 'Ingrese titulo del Post', 
                    'id': 'title'
                }
            ), 
            'intro': forms.TextInput(
                attrs={
                    'class': 'form-control', 
                    'placeholder': 'Ingrese una breve introducción', 
                    'id': 'intro'
                }
            ), 
            'body': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese su historia ',   
                    'id': 'body'
                }
            ),
            'hilo': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese descripcion del gatito',  
                    'id': 'hilo'
                }
            )
        }
        










class EspecialidadForm(forms.ModelForm):
    class Meta:
        model = Especialidad
        fields = ('nombre',)
        labels ={
            'nombre': 'Nombre de especialidad',    
        }

        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'class': 'form-control', 
                    'placeholder': 'Ingrese Especialidad', 
                    'id': 'nombre'
                }
            ), 
        }

class PsicologoForm(forms.ModelForm):
    class Meta:
        model = Psicologo
        fields = ('nombre','rut','email','telefono','especialidad')

        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
            'rut': forms.TextInput(attrs= {'class':'form-control'}),
            'email':forms.TextInput(attrs= {'class':'form-control','placeholder':'Psicologo@gmail.com'}),
            'telefono':forms.TextInput(attrs= {'class':'form-control','placeholder':'+56951393925'}),
            'especialidad':forms.Select(attrs={'class':'form-control'}),
        }




class HorariosForm(forms.ModelForm):
    class Meta:
        model = Horarios
        fields = ('horas',)

        widgets = {
            'horas': forms.Select(attrs={'class':'form-control'}),
        }


class AgendaForm(forms.ModelForm):
    class Meta:
        model = Agenda
        fields = ('psicologo','data','horarios')

        widgets = {
            'psicologo':forms.Select(attrs={'class':'form-control'}),
            'data': forms.SelectDateWidget(),
            'horarios':forms.SelectMultiple(attrs={'class':'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super(AgendaForm, self).__init__(*args, **kwargs)
        # Cambia la etiqueta del campo 'data' a 'fecha'
        self.fields['data'].label = 'Fecha'

    def clean(self):
        super(AgendaForm, self).clean()

        data = self.cleaned_data.get('data')
        data_hj = date.today()

        if data < data_hj:
            self.errors['data'] = self.error_class(['¡No es posible seleccionar una fecha que ya haya pasado!'])

        psicologo = self.cleaned_data.get('psicologo')
        agenda_psicologo = Agenda.objects.filter(psicologo__id = psicologo.id)
        
        for agenda in agenda_psicologo:
            if data == agenda.data:
                self.errors['data'] = self.error_class(['¡No es posible crear dos horarios en la misma fecha para un mismo Psicologo!'])           
                break          

        return self.cleaned_data




        
