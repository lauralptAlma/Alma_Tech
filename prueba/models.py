from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User
import datetime

USER_TIPO = (('DOCTOR', 'DOCTOR'), ('SECRETARIA', 'SECRETARIA'),('PACIENTE','PACIENTE'))
USER_ESPECIALIDAD = (('ORTOPEDIA', 'ORTOPEDIA'), ('ORTODONCIA', 'ORTODONCIA'),('GENERAL', 'GENERAL'))
NUCLEO_OPCIONES = (('TITULAR', 'TITULAR'), ('CONYUGE', 'CONYUGE'),('MADRE', 'MADRE'), ('PADRE', 'PADRE'),('HIJO', 'HIJO'),)


# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_tipo = models.CharField(max_length=15, choices=USER_TIPO, default='PACIENTE')
    user_direccion = models.CharField(max_length=155, null=True)
    user_celular = models.IntegerField(null=True)
    user_alta = models.DateField(blank=True, null=True)
    user_especialidad = models.CharField(max_length=15, choices=USER_ESPECIALIDAD, blank=True, null=True)
    user_calificacion = models.CharField(max_length=100, blank=True, null=True)

    def __unicode__(self):
        return self.user


class Paciente(models.Model):
    documento = models.CharField(primary_key=True, max_length=8, help_text="Sin puntos ni guión", null=False, blank=True)
    nombre = models.CharField(max_length=100)
    primer_apellido = models.CharField(max_length=100, null=True, blank=False)
    segundo_apellido = models.CharField(max_length=100, null=True, blank=False)
    fecha_nacimiento = models.DateField('Fecha de nacimiento', help_text="ej. 01/08/2012", default=datetime.date.today)
    celular_regex = RegexValidator(regex=r'^\?09?\d{10}$', message="Número debe ser ingresado en formato '09XXXXXXX'.")
    celular = models.CharField("Número de teléfono celular", validators=[celular_regex], max_length=9, unique=True, null=False, blank=True)
    email = models.EmailField(max_length=200, unique=True, blank=True)
    alta = models.DateTimeField(auto_now_add=True),
    nucleo_activo = models.BooleanField(default=True)
    relacion_nucleo = models.CharField(max_length=12, choices=NUCLEO_OPCIONES, default='TITULAR')


    def __str__(self):
        return str(self.nombre)


class Tratamiento(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, related_name='trat_doctor',  on_delete=models.CASCADE)
    titulo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    posicion_dental = models.CharField(max_length=50, blank=True, null=True)
    test_dental = models.CharField(max_length=100, blank=True, null=True)
    creado = models.DateField(auto_now_add=True, blank=True, null=True)
    modificado = models.DateField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return str(self.paciente)


class Cita(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, related_name='app_doctor',  on_delete=models.CASCADE)
    fecha = models.DateField(blank=True, null=True)
    hora = models.TimeField(null=True, blank=True)
    creado = models.DateField(auto_now_add=True, blank=True, null=True)
    modificado = models.DateField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return str(self.paciente.nombre)

    class Meta:
        ordering = ('fecha',)

    def __str__(self):
        return str(self.paciente)
