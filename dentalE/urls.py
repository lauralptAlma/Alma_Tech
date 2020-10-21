from django.conf.urls import url
from django.contrib import admin
from .views import (

    # doctor
    agregartratamiento,
    agregarCPO,
    verCPO,
    verantecedentes,
    verhistoriageneral,
    historiapaciente,
    pacientes_render_pdf_view,

    # secretaria
    resumendia,
    listaprofesionales,
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
    url(r'^cpopaciente/(?P<paciente_id>\d+)/$', verCPO, name="cpopaciente"),
    url(r'^antecedentespaciente/(?P<paciente_id>\d+)/$', verantecedentes, name="antecedentespaciente"),
    url(r'^tratamientospaciente/(?P<paciente_id>\d+)/$', verhistoriageneral, name="tratamientospaciente"),
    url(r'^historiapaciente/(?P<paciente_id>\d+)/$', historiapaciente, name="historiapaciente"),
    url(r'^pdf/(?P<paciente_id>\d+)/$', pacientes_render_pdf_view, name="paciente-pdf-view"),

    # secretaria
    url(r'^resumendia/$', resumendia, name='resumendia'),
    url(r'^profesionales/$', listaprofesionales, name='profesionales'),
    url(r'^agregarpaciente/$', agregarpaciente, name="agregarpaciente"),
    url(r'^listapacientes/$', listapacientes, name="listapacientes"),
    url(r'^agregarcita/$', agregarcita, name="agregarcita"),

    # paciente
    url(r'^pacienteincio/$', pacienteinicio, name='pacienteincio'),
    url(r'^pacientedetalles/(?P<paciente_id>\d+)/$', pacientedetalles, name='pacientedetalles'),
    url(r'^pacientecambiopass/$', pacientecambiopass, name='pacientecambiopass'),
    url(r'^agregarantecedentes/$', agregarantecedentes, name='agregarantecedentes'),

    url(r'^pruebafront/$', pruebaBaseFront),
]
