from django.contrib import admin
from .models import UserProfile, Consulta, Cita, Paciente, AntecedentesClinicos, Nucleo, Integrante

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Consulta)
admin.site.register(Cita)
admin.site.register(Paciente)
admin.site.register(AntecedentesClinicos)


@admin.register(Nucleo)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('matricula', 'titular',)
    list_display_links = ('matricula',)


@admin.register(Integrante)
class IntegrantesAdmin(admin.ModelAdmin):
    list_display = ('nucleo',  'relacion_nucleo', )
    list_display_links = ('nucleo',)


