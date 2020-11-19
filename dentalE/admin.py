from django.contrib import admin
from .models import UserProfile, Consulta, Cita, Paciente, \
    AntecedentesClinicos, Nucleo, Integrante, CPO, Ortodoncia, Terms

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Consulta)
admin.site.register(Cita)
admin.site.register(Paciente)
admin.site.register(AntecedentesClinicos)
admin.site.register(CPO)
admin.site.register(Ortodoncia)
admin.site.register(Terms)




@admin.register(Nucleo)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('matricula', 'titular',)
    list_display_links = ('matricula',)


@admin.register(Integrante)
class IntegrantesAdmin(admin.ModelAdmin):
    list_display = ('nucleo',  'relacion_nucleo', )
    list_display_links = ('nucleo',)
