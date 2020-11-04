from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User
from djongo import models as djongomodel

# USUARIO OPTIONS
USER_TIPO = (('DOCTOR', 'DOCTOR'), ('SECRETARIA', 'SECRETARIA'))
USER_ESPECIALIDAD = (('ORTOPEDIA', 'ORTOPEDIA'), ('ORTODONCIA', 'ORTODONCIA'),
                     ('GENERAL', 'GENERAL'))
# PACIENTE OPTIONS
PATIENT_CITY = (('ARTIGAS', 'Artigas'), ('CANELONES', 'Canelones'),
                ('CERRO LARGO', 'Cerro Largo'), ('COLONIA', 'Colonia'),
                ('DURAZNO', 'Durazno'), ('FLORES', 'Flores'),
                ('FLORIDA', 'Florida'), ('LAVALLEJA', 'Lavalleja'),
                ('MALDONADO', 'Maldonado'), ('MONTEVIDEO', 'Montevideo'),
                ('PAYSANDÚ', 'Paysandú'), ('RÍO NEGRO', 'Río Negro'),
                ('RIVERA', 'Rivera'), ('ROCHA', 'Rocha'), ('SALTO', 'Salto'),
                ('SAN JOSÉ', 'San José'), ('SORIANO', 'Soriano'),
                ('TACUAREMBÓ', 'Tacuarembó'),
                ('TRENTA Y TRES', 'Treinta y Tres'))
PATIENT_GENDER = (('FEMENINO', 'F'), ('MASCULINO', 'M'), ('OTRO', 'Otro'))
# NUCLEO OPTIONS
NUCLEO_OPCIONES = (
    ('CONYUGE', 'CONYUGE'), ('MADRE', 'MADRE'), ('PADRE', 'PADRE'),
    ('HIJO', 'HIJO'),)
# ANTECEDENTES OPTIONS
CARDIOVASCULAR_OPCIONES = (
    ('NO', 'No'), ('H.T.A.', 'Hipertensión'), ('ARRITMIAS', 'Arritmias'),
    ('I.A.M', 'Infarto Miocardio'),
    ('OTROS', 'Otros'))
ENDOCRINOLOGICOS_OPCIONES = (
    ('NO', 'No'), ('DIABETES', 'Diabetes'), ('TIROIDES', 'Tiroides'),
    ('DISPLEMIAS BAJO TRATAMIENTO', 'Displemias bajo tratamiento'),
    ('OTROS', 'Otros'))
NEFROUROLOGICOS_OPCIONES = (
    ('NO', 'No'), ('UROLITIASIS', 'Uroliatiasis'),
    ('GLOMERULOPATIAS', 'Glomerulopatias'), ('MONORRENO', 'Monorreno'),
    ('OTROS', 'Otros'))
OSTEOARTICULARES_OPCIONES = (
    ('NO', 'No'), ('LUXACIONES FRECUENTES', 'Luxaciones Frecuentes'),
    ('FRACTURAS', 'Fracturas'), ('OTROS', 'Otros'))
SN_OPCIONES = (('SI', 'Sí'), ('NO', 'No'))


# MODELOS
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_tipo = models.CharField(max_length=15, choices=USER_TIPO, default='')
    # Contacto
    celular_regex = RegexValidator(regex=r'^09\d{7,7}$',
                                   message="El número debe ser del "
                                           "formato: '+XXXXXXXXX'. "
                                           "9 digitos admitidos.")
    user_celular = models.CharField("Número de teléfono celular* ",
                                    validators=[celular_regex], max_length=9,
                                    null=True)  # validators should be a list
    user_alta = models.DateTimeField(auto_now_add=True)
    user_especialidad = models.CharField(max_length=15,
                                         choices=USER_ESPECIALIDAD, blank=True,
                                         null=True)

    def __unicode__(self):
        return self.user

    def __str__(self):
        return str(self.user.get_full_name())


class Paciente(models.Model):
    # Informacion
    paciente_id = models.AutoField(primary_key=True)
    documento = models.CharField('Documento* ', max_length=8, unique=True,
                                 help_text="Sin puntos ni guión", null=False,
                                 blank=False)
    nombre = models.CharField('Nombre* ', max_length=100, null=False,
                              blank=False)
    primer_apellido = models.CharField('Primer Apellido* ', max_length=100,
                                       null=False, blank=False)
    segundo_apellido = models.CharField('Segundo Apellido', max_length=100,
                                        null=True, blank=True)
    genero = models.CharField('Género*', max_length=10, choices=PATIENT_GENDER,
                              default='')
    direccion = models.CharField('Dirección* ', max_length=155, null=False,
                                 blank=False)
    ciudad = models.CharField(max_length=15, choices=PATIENT_CITY, blank=True,
                              null=True)
    fecha_nacimiento = models.DateField('Fecha de nacimiento* ',
                                        help_text="ej. 01/08/2012",
                                        null=False, blank=False)
    # Contacto
    celular_regex = RegexValidator(regex=r'^09\d{7,7}$',
                                   message="El número debe ser del "
                                           "formato: '+XXXXXXXXX'. "
                                           "9 digitos admitidos.")
    celular = models.CharField("Número de teléfono celular* ",
                               validators=[celular_regex], max_length=9,
                               unique=True,
                               null=False,
                               blank=False)  # validators should be a list
    email = models.EmailField('Email', max_length=200, blank=True)
    # Nucleo
    alta = models.DateTimeField(auto_now_add=True),
    nucleo_activo = models.BooleanField('Núcleo Activo', default=True)

    def clean(self):
        try:
            ci = int(self.documento)
        except ValueError:
            raise ValidationError('Por favor ingrese solamente números')
        if not self.validate_ci(ci):
            raise ValidationError('El documento no tiene un formato válido')

    # Validación de Cédula
    # The MIT License (MIT)
    #
    # Copyright (c) 2014 Franco Correa
    #
    # Permission is hereby granted, free of charge, #to any person obtaining a
    # copy of this software and associated documentation files
    # (the "Software"), to deal in the Software without restriction,
    # including without limitation the rights to use, copy, modify, merge,
    # publish, #distribute, sublicense, and/or sell copies of the Software,
    # and to permit persons to whom the Software is furnished to do so,
    # subject to the following #conditions:
    #
    # The above copyright notice and this #permission notice shall be included
    # in all copies or substantial portions of the Software.
    #
    # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
    # OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
    # MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
    # IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
    # CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
    # TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
    # SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

    @staticmethod
    def get_validation_digit(ci):
        a = 0
        i = 0
        str_ci = (str(ci))
        if len(str_ci) <= 7:
            for i in range(len(str_ci), 8):
                str_ci = '0' + str_ci
                i = i + 1
        for i in range(0, 7):
            a += (int("2987634"[i]) * int(str_ci[i])) % 10
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
        return dig == self.get_validation_digit(ci)

    def __str__(self):
        return str(self.nombre + " " + self.primer_apellido)


class AntecedentesClinicos(models.Model):
    creado = models.DateField(auto_now_add=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fumador = models.CharField('Fumador*', max_length=2, choices=SN_OPCIONES,
                               default='')
    alcohol = models.CharField('Alcohol* ', max_length=2, choices=SN_OPCIONES,
                               default='')
    coproparasitario = models.CharField('Coproparasitario * ', max_length=2,
                                        choices=SN_OPCIONES, default='')
    aparato_digestivo = models.CharField('Aparato Digestivo* ', max_length=2,
                                         choices=SN_OPCIONES, default='')
    desc_aparato_digestivo = models.CharField(
        'Descripción Aparato Digestivo* ', max_length=150, null=True,
        blank=True)
    dermatologicos = models.CharField('Dermatológicos* ', max_length=2,
                                      choices=SN_OPCIONES, default='')
    desc_dermatologicos = models.CharField('Descripción Dermatológicos* ',
                                           max_length=150, null=True,
                                           blank=True)
    alergias = models.CharField('Alergias* ', max_length=2,
                                choices=SN_OPCIONES, default='')
    desc_alergias = models.CharField('Descripción Alergias* ', max_length=150,
                                     null=True, blank=True)
    autoinmunes = models.CharField('Autoinmunes* ', max_length=2,
                                   choices=SN_OPCIONES, default='')
    desc_autoinmunes = models.CharField('Descripción Autoinmunes* ',
                                        max_length=150, null=True, blank=True)
    oncologicas = models.CharField('Oncológicas* ', max_length=2,
                                   choices=SN_OPCIONES, default='')
    desc_oncologicas = models.CharField('Descripción Oncológicas* ',
                                        max_length=150, null=True, blank=True)
    hematologicas = models.CharField('Hematológicas* ', max_length=2,
                                     choices=SN_OPCIONES, default='')
    desc_hematologicas = models.CharField('Descripción Hematológicas* ',
                                          max_length=150, null=True,
                                          blank=True)
    intervenciones = models.CharField('Intervenciones* ', max_length=2,
                                      choices=SN_OPCIONES, default='')
    desc_intervenciones = models.CharField('Descripción Intervenciones* ',
                                           max_length=150, null=True,
                                           blank=True)
    toma_medicacion = models.CharField('Medicación Habitual* ', max_length=2,
                                       choices=SN_OPCIONES, default='')
    desc_medicacion = models.CharField('Descripción Medicación* ',
                                       max_length=150, null=True, blank=True)
    endocrinometabolico = models.CharField('Endocrinometabólico* ', null=False,
                                           max_length=150, default='')
    desc_endocrinometabolico = models.CharField(
        'Descripción Endocrinometabólico* ', max_length=150, null=True,
        blank=True)
    cardiovascular = models.CharField('Cardiovascular* ', null=False,
                                      max_length=150, default='')
    desc_cardiovascular = models.CharField('Descripción Cardiovascular* ',
                                           max_length=150, null=True,
                                           blank=True)
    nefrourologicos = models.CharField('Nefrourológicos* ', null=False,
                                       max_length=150, default='')
    desc_nefrourologicos = models.CharField('Descripción Nefrourológicos* ',
                                            max_length=150, null=True,
                                            blank=True)
    osteoarticulares = models.CharField('Osteoarticulares* ', null=False,
                                        max_length=150, default='')
    desc_osteoarticulares = models.CharField('Descripción Osteoarticulares* ',
                                             max_length=150, null=True,
                                             blank=True)
    observations = models.TextField('Observaciones', max_length=150, null=True,
                                    blank=True)

    def __str__(self):
        return str(self.paciente)


class Nucleo(models.Model):
    matricula = models.CharField(primary_key=True, max_length=8,
                                 help_text="solo numeros", null=False,
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
    relacion_nucleo = models.CharField(max_length=12, choices=NUCLEO_OPCIONES,
                                       default='')

    class Meta:
        verbose_name = "Integrante"
        verbose_name_plural = "Integrantes"

    def __str__(self):
        return self.nucleo


class Consulta(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, related_name='consulta_doctor',
                               on_delete=models.CASCADE)
    diagnostico = models.TextField('Diagnóstico', max_length=250, default='',
                                   blank=False, null=False)
    tratamiento = models.TextField(max_length=250, default='', blank=False,
                                   null=False)
    indicaciones = models.TextField(max_length=250, default='', blank=False,
                                    null=False)
    creado = models.DateField(auto_now_add=True, blank=True, null=True)

    modificado = models.DateField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return str(self.paciente)

    class Meta:
        ordering = ('creado',)


class Ortodoncia(models.Model):
    doctor = models.ForeignKey(User, related_name='doctor_ortodoncia', on_delete=models.CASCADE)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    tipo = models.TextField('Tipo', choices=CONSULTA_OPCIONES, default='ORTODONCIA')
    diagnostico = models.TextField('Diagnóstico', max_length=250, default='', blank=False, null=False)
    tratamiento = models.TextField(max_length=250, default='', blank=False, null=False)
    indicaciones = models.TextField(max_length=250, default='', blank=False, null=False)
    creado = models.DateField(auto_now_add=True, blank=True, null=True)
    modificado = models.DateField(auto_now=True, blank=True, null=True)
    image = djongomodel.ImageField(storage=GridFSStorage(collection='image'))

    class Meta:
        verbose_name = " Consulta de Ortodoncia | Ortopedia"
        verbose_name_plural = "Consultas de Ortodoncia | Ortopedia"

    def __str__(self):
        return str(self.paciente)


class CPO(models.Model):
    creado = models.DateField(auto_now_add=True, blank=True, null=True)
    modificado = models.DateField(auto_now=True, blank=True, null=True)
    doctor = models.ForeignKey(User, related_name='cpo_doctor',
                               on_delete=models.CASCADE)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    cpo_id = models.AutoField(primary_key=True)
    contenido_cpo = models.TextField()
    ceod = models.IntegerField(blank=True, null=True)
    ceos = models.IntegerField(blank=True, null=True)
    cpod = models.IntegerField(blank=True, null=True)
    cpos = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = "dentalE_CPOs"

    def __str__(self):
        return str(self.cpo_id)


class Cita(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, related_name='app_doctor',
                               on_delete=models.CASCADE)
    fecha = models.DateField(blank=True, null=True)
    hora = models.TimeField(null=True, blank=True)
    creado = models.DateField(auto_now_add=True, blank=True, null=True)
    modificado = models.DateField(auto_now=True, blank=True, null=True)

    class Meta:
        ordering = ('fecha',)

    def __str__(self):
        return str(self.paciente)


class Contacto(models.Model):
    nombre = models.CharField(max_length=50, blank=False, null=False,
                              default='')
    email = models.EmailField(max_length=50, blank=False, null=False,
                              default='')
    asunto = models.CharField(max_length=50, blank=False, null=False,
                              default='')
    mensaje = models.TextField(max_length=550, blank=False, null=False,
                               default='')
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Contacto"

    def __str__(self):
        return self.name + "-" + self.email
