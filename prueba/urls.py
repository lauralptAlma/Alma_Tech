from django.conf.urls import url
from django.contrib import admin
from .views import (

    # doctor
    pacientedeldiadetalles,
    pacientesdeldia,
    doccambiopass,

    # secretaria
    resumendia,
    listadoctores,
    rechangepassword,
    agregarpaciente,
    listapacientes,
    agregarcita,
    agregartratamiento,

    # paciente
    pacienteinicio,
    pacientedetalles,
    pacientecambiopass,
)

urlpatterns = [

    # doctor
    url(r'^pacientesdeldia/$', pacientesdeldia, name='pacientesdeldia'),
    url(r'^pacientedeldiadetalles/$', pacientedeldiadetalles, name='pacientedeldiadetalles'),
    url(r'^doccambiopass/$', doccambiopass, name='doccambiopass'),

    # secretaria
    url(r'^resumendia/$', resumendia, name='resumendia'),
    url(r'^doctorlista/$', listadoctores, name='listadoctores'),
    url(r'^rechangepassword/$', rechangepassword, name='rechangepassword'),
    url(r'^agregarpaciente/$', agregarpaciente, name="agregarpaciente"),
    url(r'^listapacientes/$', listapacientes, name="listapacientes"),
    url(r'^agregarcita/$', agregarcita, name="agregarcita"),
    url(r'^agregartratamiento/$', agregartratamiento, name="agregartratamiento"),

    # paciente
    url(r'^pacienteincio/$', pacienteinicio, name='pacienteincio'),
    url(r'^pacientedetalles/$', pacientedetalles, name='pacientedetalles'),
    url(r'^pacientecambiopass/$', pacientecambiopass, name='pacientecambiopass'),


]

