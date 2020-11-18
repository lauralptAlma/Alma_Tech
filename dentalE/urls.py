from django.conf.urls import url

from .views import (

    # doctor
    agregartratamiento,
    agregarortodoncia,
    agregarCPO,
    verCPO,
    verantecedentes,
    verhistoriageneral,
    verhistoriaortodoncia,
    compararortodoncia,
    patient_render_background_pdf,

    # contacto
    contacto,

    # secretaria
    resumendia,
    listaprofesionales,
    agregarpaciente,
    listapacientes,
    CalendarPage,
    edit_cita,

    # paciente
    pacienteinicio,
    pacientedetalles,
    pacientecambiopass,
    agregarantecedentes,
    edit_patient,

    # general
    analisis,
    get_data,
    DataView,
    ChartData,
    ChartPatient,

)

urlpatterns = [

    # doctor
    url(r'^agregartratamiento/$', agregartratamiento,
        name="agregartratamiento"),
    url(r'^agregarortodoncia/$', agregarortodoncia, name="agregarortodoncia"),
    url(r'^agregarcpo/$', agregarCPO, name='agregarcpo'),
    url(r'^cpopaciente/(?P<paciente_id>\d+)/$', verCPO, name="cpopaciente"),
    url(r'^antecedentespaciente/(?P<paciente_id>\d+)/$', verantecedentes,
        name="antecedentespaciente"),
    url(r'^tratamientospaciente/(?P<paciente_id>\d+)/$', verhistoriageneral,
        name="tratamientospaciente"),
    url(r'^tratamientosortodoncia/(?P<paciente_id>\d+)/$',
        verhistoriaortodoncia,
        name="ortodonciapaciente"),
    url(r'^compararortodoncia/(?P<paciente_id>\d+)/$',
        compararortodoncia,
        name="compararortodonciapaciente"),
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

    # general
    url(r'^negocio/$', analisis,
        name='analisis'),
    url(r'^api/data/$', get_data,
        name='api-data'),
    url(r'^data/$', DataView,
        name='api-data'),
    url(r'^api/chart/data/$', ChartData.as_view()),
    url(r'^api/chart/generarestadistica/(?P<paciente_id>\d+)/$',
        ChartPatient, name="generarestadistica"),

]
