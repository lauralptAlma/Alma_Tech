from django.conf.urls import url
from django.contrib import admin
from .views import (

    # doctor
    agregartratamiento,
    agregarCPO,

    # secretaria
    resumendia,
    listadoctores,
    agregarpaciente,
    listapacientes,
    agregarcita,

    # paciente
    pacienteinicio,
    pacientedetalles,
    pacientecambiopass,
    agregarantecedentes,
    pruebaBaseFront,

)

urlpatterns = [

    # doctor
    url(r'^agregartratamiento/$', agregartratamiento, name="agregartratamiento"),
    url(r'^agregarcpo/$', agregarCPO, name='agregarcpo'),

    # secretaria
    url(r'^resumendia/$', resumendia, name='resumendia'),
    url(r'^doctorlista/$', listadoctores, name='listadoctores'),
    url(r'^agregarpaciente/$', agregarpaciente, name="agregarpaciente"),
    url(r'^listapacientes/$', listapacientes, name="listapacientes"),
    url(r'^agregarcita/$', agregarcita, name="agregarcita"),

    # paciente
    url(r'^pacienteincio/$', pacienteinicio, name='pacienteincio'),
    url(r'^pacientedetalles/(?P<paciente_id>[0-9])/$', pacientedetalles, name='pacientedetalles'),
    url(r'^pacientecambiopass/$', pacientecambiopass, name='pacientecambiopass'),
    url(r'^agregarantecedentes/$', agregarantecedentes, name='agregarantecedentes'),

    url(r'^pruebafront/$', pruebaBaseFront),
]
