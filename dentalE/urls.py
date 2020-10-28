from django.conf.urls import url
from django.contrib import admin
from .views import (

    # doctor
    agregartratamiento,
    agregarCPO,
    verCPO,

    # secretaria
    resumendia,
    listaprofesionales,
    agregarpaciente,
    listapacientes,
    agregarcita,
    CalendarPage,
    edit_cita,

    # paciente
    pacienteinicio,
    pacientedetalles,
    pacientecambiopass,
    agregarantecedentes,
    pruebaBaseFront,

)

urlpatterns = [

    # doctor
    url(r'^agregartratamiento/$', agregartratamiento,
        name="agregartratamiento"),
    url(r'^agregarcpo/$', agregarCPO, name='agregarcpo'),
    url(r'^cpopaciente/(?P<paciente_id>\d+)/$', verCPO, name="cpopaciente"),

    # secretaria
    url(r'^resumendia/$', resumendia, name='resumendia'),
    url(r'^profesionales/$', listaprofesionales, name='profesionales'),
    url(r'^agregarpaciente/$', agregarpaciente, name="agregarpaciente"),
    url(r'^listapacientes/$', listapacientes, name="listapacientes"),
    url(r'^agregarcita/$', CalendarPage, name="agregarcita"),
    url(r'^editarcita/(?P<cita_id>\d+)/$', edit_cita, name="editarcita"),

    # paciente
    url(r'^pacienteincio/$', pacienteinicio, name='pacienteincio'),
    url(r'^pacientedetalles/(?P<paciente_id>\d+)/$', pacientedetalles,
        name='pacientedetalles'),
    url(r'^pacientecambiopass/$', pacientecambiopass,
        name='pacientecambiopass'),
    url(r'^agregarantecedentes/$', agregarantecedentes,
        name='agregarantecedentes'),

    url(r'^pruebafront/$', pruebaBaseFront),
]
