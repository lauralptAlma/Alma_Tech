from django.core.exceptions import ValidationError
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
    ('NO', 'NO'), ('H.T.A.', 'HIPERTENSION'), ('ARRITMIAS', 'ARRITMIAS'), ('I.A.M', 'INFARTO MIOCARDIO'),
    ('OTROS', 'OTROS'))
ENDOCRINOLOGICOS_OPCIONES = (
    ('NO', 'NO'), ('DIABETES', 'DIABETES'), ('TIROIDES', 'TIROIDES'),
    ('DISPLEMIAS BAJO TRATAMIENTO', 'DISPLEMIAS BAJO TRATAMIENTO'), ('OTROS', 'OTROS'))
NEFROUROLOGICOS_OPCIONES = (
    ('NO', 'NO'), ('UROLITIASIS', 'UROLITIASIS'), ('GLOMERULOPATIAS', 'GLOMERULOPATIAS'), ('MONORRENO', 'MONORRENO'))
OSTEOARTICULARES_OPCIONES = (
    ('NO', 'NO'), ('LUXACIONES', 'LUXACIONES'), ('FRACTURAS', 'FRACTURAS'), ('OTROS', 'OTROS'))
SN_OPCIONES = (('NO', 'NO'), ('SI', 'SI'))


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
    # Contacto
    celular_regex = RegexValidator(regex=r'^\+?1?\d{9,9}$',
                                   message="El número debe ser del formato: '+XXXXXXXXX'. 9 digitos admitidos.")
    celular = models.CharField("Número de teléfono celular", validators=[celular_regex], max_length=9, unique=True,
                               null=False, blank=True)  # validators should be a list
    email = models.EmailField(max_length=200, unique=True, blank=True)
    # Nucleo
    alta = models.DateTimeField(auto_now_add=True),
    nucleo_activo = models.BooleanField(default=True)

    def clean(self):
        try:
            ci = int(self.documento)
        except ValueError:
            raise ValidationError('Por favor ingrese solamente números')
        print(ci)
        if not self.validate_ci(ci):
            raise ValidationError('El documento no tiene un formato válido')

    # Validación de Cédula
    # The MIT License (MIT)
    #
    # Copyright (c) 2014 Franco Correa
    #
    # Permission is hereby granted, free of charge, #to any person obtaining a copy
    # of this software and associated documentation #files (the "Software"), to deal
    # in the Software without restriction, #including without limitation the rights
    # to use, copy, modify, merge, publish, #distribute, sublicense, and/or sell
    # copies of the Software, and to permit persons #to whom the Software is
    # furnished to do so, subject to the following #conditions:
    #
    # The above copyright notice and this #permission notice shall be included in all
    # copies or substantial portions of the Software.
    #
    # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    # IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    # FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    # AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    # LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    # OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    # SOFTWARE.

    @staticmethod
    def get_validation_digit(ci):
        a = 0
        i = 0
        if len(str(ci)) <= 6:
            for i in range(len(ci), 7):
                ci = '0' + ci
                i = i + 1

        for i in range(0, 7):
            a += (int("2987634"[i]) * int(str(ci)[i])) % 10
            i = i + 1

        if a % 10 == 0:
            return 0
        else:
            return 10 - a % 10

    @staticmethod
    def clean_ci(ci):
        return int(str(ci).replace("-", "").replace('.', ''))

    def validate_ci(self, ci):
        ci = self.clean_ci(ci)
        dig = int(str(ci)[int(len(str(ci))) - 1])
        print(dig)
        print(self.get_validation_digit(ci))
        return dig == self.get_validation_digit(ci)

    def __str__(self):
        return str(self.nombre)


class AntecedentesClinicos(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)  # FK
    fumador = models.CharField('Tabaco', max_length=2, choices=SN_OPCIONES, default='')
    alcohol = models.CharField('Alcohol', max_length=2, choices=SN_OPCIONES, default='')
    coproparasitario = models.CharField('Coproparasitario', max_length=2, choices=SN_OPCIONES, default='')
    aparato_digestivo = models.CharField('Ap.Digestivo', max_length=2, choices=SN_OPCIONES, default='')
    desc_aparato_digestivo = models.CharField('Descripción Ap.Digestivo', max_length=150, null=True, blank=True)
    dermatologicos = models.CharField('Dermatológicos', max_length=2, choices=SN_OPCIONES, default='')
    desc_dermatologicos = models.CharField('Descripción Dermatológicos', max_length=150, null=True, blank=True)
    alergias = models.CharField('Alergias', max_length=2, choices=SN_OPCIONES, default='')
    desc_alergias = models.CharField('Descripción Alergias', max_length=150, null=True, blank=True)
    autoinmnunes = models.CharField('Autoinmunes', max_length=2, choices=SN_OPCIONES, default='')
    desc_autoinmnunes = models.CharField('Descripción Autoinmunes', max_length=150, null=True, blank=True)
    oncologicas = models.CharField('Oncológicas', max_length=2, choices=SN_OPCIONES, default='')
    desc_oncologicas = models.CharField('Descripción Oncológicas', max_length=150, null=True, blank=True)
    hematologicas = models.CharField('Hematológicas', max_length=2, choices=SN_OPCIONES, default='')
    desc_hematologicas = models.CharField('Descripción Hematológicas', max_length=150, null=True, blank=True)
    intervenciones = models.CharField('Intervenciones', max_length=2, choices=SN_OPCIONES, default='')
    desc_intervenciones = models.CharField('Descripción Intervenciones', max_length=150, null=True, blank=True)
    toma_medicacion = models.CharField('Medicación Habitual', max_length=2, choices=SN_OPCIONES, default='')
    desc_medicacion = models.CharField('Descripción Medicación', max_length=150, null=True, blank=True)
    endocrinometabolico = models.CharField('Endocrinometabólico', max_length=27, choices=ENDOCRINOLOGICOS_OPCIONES,
                                           default='')
    desc_endocrinometabolico = models.CharField('Descripción Endocrinometabólico', max_length=150, null=True,
                                                blank=True)
    cardiovascular = models.CharField('Cardiovascular', max_length=27, choices=CARDIOVASCULAR_OPCIONES, default='')
    desc_cardiovascular = models.CharField('Descripción Cardiovascular', max_length=150, null=True, blank=True)
    nefrourologicos = models.CharField('Nefrourológicos', max_length=27, choices=NEFROUROLOGICOS_OPCIONES, default='')
    desc_nefrourologicos = models.CharField('Descripción Cardiovascular', max_length=150, null=True, blank=True)
    observations = models.TextField('Observaciones', null=True, blank=True)

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
        return str(self.matricula) or ''


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
