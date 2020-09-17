from django.contrib import admin
from .models import UserProfile, Consulta, Cita, Paciente, AntecedentesClinicos
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Consulta)
admin.site.register(Cita)
admin.site.register(Paciente)
admin.site.register(AntecedentesClinicos)