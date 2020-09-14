from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from .models import Paciente, Cita, Tratamiento

class IngresoForm(ModelForm):
	class Meta:
		model = User
		fields = ('username', 'password',)


class PacienteForm(ModelForm):
	class Meta:
		model = Paciente
		fields = ('documento','nombre', 'primer_apellido', 'segundo_apellido','fecha_nacimiento','email','celular', 'nucleo_activo','relacion_nucleo')

		widgets = {
			'documento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sin puntos ni guión', 'display': 'inline-block'}),
			'nombre': forms.TextInput(attrs={'class': 'form-control', 'display': 'inline-block'}),
			'primer_apellido': forms.TextInput(attrs={'class': 'form-control'}),
			'segundo_apellido': forms.TextInput(attrs={'class': 'form-control'}),
			'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'ej. 01/08/2012'}),
			'email': forms.EmailInput(attrs={'class': 'form-control'}),
			'celular': forms.TextInput(attrs={'class': 'form-control'}),
			'nucleo_activo': forms.TextInput(attrs={'class': 'form-control'}),
			'relacion_nucleo': forms.Select(attrs={'class': 'form-control'}),
		}


class CitaForm(ModelForm):
	class Meta:
		model = Cita
		fields = ('paciente', 'doctor', 'fecha', 'hora')

class TratamientoForm(ModelForm):
	class Meta:
		model = Tratamiento
		readonly_fields = 'creado'
		fields = ('paciente', 'doctor', 'titulo', 'descripcion', 'posicion_dental', 'test_dental')

