from django.contrib import admin
from .models import UserProfile, Tratamiento, Cita, Paciente
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Tratamiento)
admin.site.register(Cita)
admin.site.register(Paciente)