from django.conf.urls import url
from .views import (

    # doctor
    agregartratamiento,
    agregarCPO,
    verCPO,
    verantecedentes,
    verhistoriageneral,
    patient_render_background_pdf,

    # contacto
    contacto,

    # secretaria
    resumendia,
    listaprofesionales,
    agregarpaciente,
    listapacientes,
    agregarcita,
    CalendarPage,
    edit_cita,
    delete_cita,

    # paciente
    pacienteinicio,
    pacientedetalles,
    pacientecambiopass,
    agregarantecedentes,
    edit_patient,

)

urlpatterns = [

    # doctor
    url(r'^agregartratamiento/$', agregartratamiento,
        name="agregartratamiento"),
    url(r'^agregarcpo/$', agregarCPO, name='agregarcpo'),
    url(r'^cpopaciente/(?P<paciente_id>\d+)/$', verCPO, name="cpopaciente"),
    url(r'^antecedentespaciente/(?P<paciente_id>\d+)/$', verantecedentes,
        name="antecedentespaciente"),
    url(r'^tratamientospaciente/(?P<paciente_id>\d+)/$', verhistoriageneral,
        name="tratamientospaciente"),
    url(r'^generarhistoriapdf/(?P<paciente_id>\d+)/$',
        patient_render_background_pdf,
        name="paciente-pdf-view"),
    
    # contacto
    url(r'^contacto/$', contacto,
        name="contacto"),

    # secretaria
    url(r'^resumendia/$', resumendia, name='resumendia'),
    url(r'^profesionales/$', listaprofesionales, name='profesionales'),
    url(r'^agregarpaciente/$', agregarpaciente, name="agregarpaciente"),
    url(r'^listapacientes/$', listapacientes, name="listapacientes"),
    url(r'^agregarcita/$', CalendarPage, name="agregarcita"),
    url(r'^editarcita/(?P<cita_id>\d+)/$', edit_cita, name="editarcita"),
    url(r'^borrarcita/(?P<cita_id>\d+)/$', delete_cita, name="deletecita"),

    # paciente
    url(r'^pacienteincio/$', pacienteinicio, name='pacienteincio'),
    url(r'^pacientedetalles/(?P<paciente_id>\d+)/$', pacientedetalles,
        name='pacientedetalles'),
    url(r'^pacientecambiopass/$', pacientecambiopass,
        name='pacientecambiopass'),
    url(r'^agregarantecedentes/$', agregarantecedentes,
        name='agregarantecedentes'),
    url(r'^editarpaciente/(?P<paciente_id>\d+)/$', edit_patient,
        name='editarpaciente'),
]
