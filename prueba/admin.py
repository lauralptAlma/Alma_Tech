from django.contrib import admin
from .models import UserProfile, Consulta, Cita, Paciente
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Consulta)
admin.site.register(Cita)
admin.site.register(Paciente)