from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views import View
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

from .forms import CitaForm, PacienteForm
from .models import UserProfile, Tratamiento, Paciente, Cita
from datetime import date


# doctor
def pacientesdeldia(request):
    return render(request, "doctor/paciente_dia/paciente_dia.html", {})


def pacientedeldiadetalles(request):
    return render(request, "doctor/paciente_dia/paciente_dia_detalles.html", {})


def doccambiopass(request):
    return render(request, "doctor/common/cambiar_pass.html", {})


# secretaria
def resumendia(request):
    agenda_hoy = Cita.objects.filter(date=date.today())
    tratamiento_hoy = Tratamiento.objects.filter(created_at=date.today())
    return render(request, "secretaria/agenda_hoy/agenda_hoy.html",
                  {'agenda_hoy': agenda_hoy, 'tratamiento_hoy': tratamiento_hoy})


def agregarcita(request):
    form = CitaForm()
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            cita = form.save()
            return HttpResponseRedirect("/prueba/retodaybooking/")
    return render(request, "secretaria/agenda_hoy/agregar_cita.html", {'form': form})


def agregartratamiento(request):
    form = CitaForm()
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            tratamiento = form.save()
            return HttpResponseRedirect("/prueba/retodaybooking/")
    return render(request, "secretaria/agenda_hoy/agregar_tratamiento.html", {'form': form})


def listadoctores(request):
    doctors = UserProfile.objects.filter(user_type='DOCTOR')
    return render(request, "secretaria/lista_doctores/lista_doctores.html", {'doctors': doctors})


def listapacientes(request):
    pacientes = Paciente.objects.all()
    print(pacientes)
    return render(request, "secretaria/lista_pacientes/lista_pacientes.html", {'patients': pacientes})


def rechangepassword(request):
    return render(request, "secretaria/common/cambiar_pass.html", {})


def agregarpaciente(request):
    form = PacienteForm()
    if request.method == 'POST':
        form = Paciente(request.POST)
        if form.is_valid():
            patient = form.save()
            return HttpResponseRedirect("/prueba/retodaybooking/")
    return render(request, "secretaria/agenda_hoy/agregar_paciente.html", {'form': form})


# paciente
def pacienteinicio(request):
    return render(request, "paciente/home/home.html", {})


def pacientedetalles(request):
    return render(request, "paciente/home/detalles.html", {})


def pacientecambiopass(request):
    return render(request, "paciente/common/cambiar_constrasena.html", {})


# frontpage
class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "frontpage/index.html")


def ingreso(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            userprofile = UserProfile.objects.get(user=user)
            if userprofile.user_type == 'SECRETARIA':
                return HttpResponseRedirect('/prueba/retodaybooking/')
            elif user.UserProfile.user_type == 'DOCTOR':
                return HttpResponseRedirect('/prueba/dotodaypatient/')
            else:
                return HttpResponseRedirect('/prueba/patienthome')
    return render(request, 'frontpage/index.html')
