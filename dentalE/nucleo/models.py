from django.contrib.admin import models
from dentalE.models import Nucleo, Paciente



# NUCLEO OPTIONS
NUCLEO_OPCIONES = (
    ('CONYUGE', 'CONYUGE'), ('MADRE', 'MADRE'), ('PADRE', 'PADRE'), ('HIJO', 'HIJO'),)

class Integrante(models.Model):
    nucleo = models.ForeignKey(Nucleo, on_delete=models.CASCADE)
    relacion_nucleo = models.CharField(max_length=100,  choices=NUCLEO_OPCIONES, default='', verbose_name="relacionNucleo")
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)


    def __unicode__(self):
        return u'%s' % self.nucleo

    class Meta:
        verbose_name_plural = 'Integrantes'
        ordering = ['nucelo']
