from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User
import datetime

# USUARIO OPTIONS
USER_TIPO = (('DOCTOR', 'DOCTOR'), ('SECRETARIA', 'SECRETARIA'), ('PACIENTE', 'PACIENTE'))
USER_ESPECIALIDAD = (('ORTOPEDIA', 'ORTOPEDIA'), ('ORTODONCIA', 'ORTODONCIA'), ('GENERAL', 'GENERAL'))
# NUCLEO OPTIONS
NUCLEO_OPCIONES = (
    ('CONYUGE', 'CONYUGE'), ('MADRE', 'MADRE'), ('PADRE', 'PADRE'), ('HIJO', 'HIJO'),)
# ANTECEDENTES OPTIONS
CARDIOVASCULAR_OPCIONES = (
    ('H.T.A.', 'HIPERTENSION'), ('ARRITMIAS', 'ARRITMIAS'), ('I.A.M', 'INFARTO MIOCARDIO'), ('OTROS', 'OTROS'))
ENDOCRINOLOGICOS_OPCIONES = (
    ('DIABETES', 'DIABETES'), ('TIROIDES', 'TIROIDES'), ('DISPLEMIAS BAJO TRATAMIENTO', 'Infarto Agudo de Miocardio'))
NEFROUROLOGICOS_OPCIONES = (
    ('UROLITIASIS', 'UROLITIASIS'), ('GLOMERULOPATIAS', 'GLOMERULOPATIAS'), ('MONORRENO', 'MONORRENO'))
OSTEOARTICULARES_OPCIONES = (('LUXACIONES', 'LUXACIONES'), ('FRACTURAS', 'FRACTURAS'), ('OTROS', 'OTROS'))
SN_OPCIONES = (('SI', 'SI'), ('NO', 'NO'))


# MODELOS
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_tipo = models.CharField(max_length=15, choices=USER_TIPO, default='')
    user_direccion = models.CharField(max_length=155, null=True)
    user_celular = models.IntegerField(null=True)
    user_alta = models.DateField(blank=True, null=True)
    user_especialidad = models.CharField(max_length=15, choices=USER_ESPECIALIDAD, blank=True, null=True)
    user_calificacion = models.CharField(max_length=100, blank=True, null=True)

    def __unicode__(self):
        return self.user




class Paciente(models.Model):
    # Informacion
    documento = models.CharField(primary_key=True, max_length=8, help_text="Sin puntos ni guión", null=False,
                                 blank=True)
    nombre = models.CharField(max_length=100)
    primer_apellido = models.CharField(max_length=100, null=True, blank=False)
    segundo_apellido = models.CharField(max_length=100, null=True, blank=False)
    fecha_nacimiento = models.DateField('Fecha de nacimiento', help_text="ej. 01/08/2012", default=datetime.date.today)
    # Clinicos.

    # Contacto
    celular_regex = RegexValidator(regex=r'^\+?1?\d{9,9}$',
                                   message="El número debe ser del formato: '+XXXXXXXXX'. 9 digitos admitidos.")
    celular = models.CharField("Número de teléfono celular", validators=[celular_regex], max_length=9, unique=True,
                               null=False, blank=True)  # validators should be a list
    email = models.EmailField(max_length=200, unique=True, blank=True)
    # Nucleo
    alta = models.DateTimeField(auto_now_add=True),
    nucleo_activo = models.BooleanField(default=True)

    def __str__(self):
        return str(self.nombre)

class AntecedentesClinicos(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)  # FK
    fumador = models.CharField('Tabaco', max_length=2, choices=SN_OPCIONES, default='')
    coproparasitario = alergias = models.CharField('Coproparasitario', max_length=2, choices=SN_OPCIONES, default='')
    aparato_digestivo = models.CharField('Ap.Digestivo', max_length=2, choices=SN_OPCIONES, default='')
    alergias = models.CharField('Alergias', max_length=2, choices=SN_OPCIONES, default='')
    oncologicas = models.CharField('Oncologicas', max_length=2, choices=SN_OPCIONES, default='')
    autoinmnunes = models.CharField('Autoinmunes', max_length=2, choices=SN_OPCIONES, default='')
    intervenciones = models.CharField('Intervenciones', max_length=2, choices=SN_OPCIONES, default='')
    endocrinometabólico = models.CharField('Endocrinometabólico', max_length=27, choices=ENDOCRINOLOGICOS_OPCIONES,
                                           default='')
    cardiovascular = models.CharField('Cardiovascular', max_length=27, choices=CARDIOVASCULAR_OPCIONES, default='')
    observations = models.TextField('Observaciones')

    def __str__(self):
        return str(self.paciente)

class Nucleo(models.Model):
    matricula = models.CharField(primary_key=True, max_length=8, help_text="solo numeros", null=False,
                                 blank=True)
    titular = models.ForeignKey(Paciente, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Nucleo"
        verbose_name_plural = "Nucleos"

    def __str__(self):
        return self.matricula


class Integrante(models.Model):
    nucleo = models.ForeignKey(Nucleo, on_delete=models.CASCADE)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    relacion_nucleo = models.CharField(max_length=12, choices=NUCLEO_OPCIONES, default='')

    class Meta:
        verbose_name = "Integrante"
        verbose_name_plural = "Integrantes"

    def __str__(self):
        return self.nucleo


class Consulta(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, related_name='trat_doctor', on_delete=models.CASCADE)
    diagnostico = models.CharField(max_length=250, default='', blank=False, null=False)
    tratamiento = models.CharField(max_length=250, default='', blank=False, null=False)
    indicaciones = models.CharField(max_length=250, default='', blank=False, null=False)
    creado = models.DateField(auto_now_add=True, blank=True, null=True)
    modificado = models.DateField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return str(self.paciente)


class Foto(models.Model):
    """ Subida de imagenes """
    doctor = models.ForeignKey(User, related_name='foto_trat_doctor', on_delete=models.CASCADE)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fecha = models.DateField("Fecha", auto_now_add=True)
    titulo = models.CharField("Titulo", max_length=125, default='')
    contenido = models.TextField("Contenido", default='')
    image = models.ImageField("Imagen", upload_to='upload/imagenesConsulta')

    class Meta:
        db_table = "ImgConsultas"


class Cita(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, related_name='app_doctor', on_delete=models.CASCADE)
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
