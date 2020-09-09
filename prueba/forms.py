from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Paciente, Cita, Tratamiento

class IngresoForm(ModelForm):
	class Meta:
		model = User
		fields = ('username', 'password',)


class PacienteForm(ModelForm):
	class Meta:
		model = Paciente
		fields = ('documento','nombre', 'primer_apellido', 'segundo_apellido','fecha_nacimiento','email','celular', 'nucleo_activo','relacion_nucleo' )


class CitaForm(ModelForm):
	class Meta:
		model = Cita
		fields = ('paciente', 'doctor', 'fecha', 'hora')

class TratamientoForm(ModelForm):
	class Meta:
		model = Tratamiento
		readonly_fields = 'creado'
		fields = ('paciente', 'doctor', 'titulo', 'descripcion', 'posicion_dental', 'test_dental')

