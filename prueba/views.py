from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views import View
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.views.generic import CreateView, UpdateView

from .forms import CitaForm, PacienteForm, IntegranteFormset
from .models import UserProfile, Tratamiento, Paciente, Cita, Nucleo
from datetime import date


def pruebaBaseFront(request):
    form = PacienteForm()
    if request.method == 'POST':
        form = Paciente(request.POST)
        if form.is_valid():
            patient = form.save()
            return HttpResponseRedirect("/prueba/resumendia/")
    return render(request, "almaFront/agregar_paciente.html", {'form': form})


# doctor
@login_required
def pacientesdeldia(request):
    return render(request, "doctor/paciente_dia/paciente_dia.html", {})


@login_required
def pacientedeldiadetalles(request):
    return render(request, "doctor/paciente_dia/paciente_dia_detalles.html", {})


@login_required
def doccambiopass(request):
    return render(request, "doctor/common/cambiar_pass.html", {})


# secretaria
@login_required
def resumendia(request):
    agenda_hoy = Cita.objects.filter(creado=date.today())
    tratamiento_hoy = Tratamiento.objects.filter(creado=date.today())
    return render(request, "secretaria/agenda_hoy/agenda_hoy.html",
                  {'agenda_hoy': agenda_hoy, 'tratamiento_hoy': tratamiento_hoy})


@login_required
def agregarcita(request):
    form = CitaForm()
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            cita = form.save()
            return HttpResponseRedirect("/prueba/resumendia/")
    return render(request, "secretaria/agenda_hoy/agregar_cita.html", {'form': form})


@login_required
def agregartratamiento(request):
    form = CitaForm()
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            tratamiento = form.save()
            return HttpResponseRedirect("/prueba/resumendia/")
    return render(request, "secretaria/agenda_hoy/agregar_tratamiento.html", {'form': form})


@login_required
def listadoctores(request):
    doctors = UserProfile.objects.filter(user_type='DOCTOR')
    return render(request, "secretaria/lista_doctores/lista_doctores.html", {'doctors': doctors})


@login_required
def listapacientes(request):
    pacientes = Paciente.objects.all()
    print(pacientes)
    return render(request, "secretaria/lista_pacientes/lista_pacientes.html", {'patients': pacientes})


@login_required
def rechangepassword(request):
    return render(request, "secretaria/common/cambiar_pass.html", {})


@login_required
def agregarpaciente(request):
    form = PacienteForm()
    if request.method == 'POST':
        form = Paciente(request.POST)
        if form.is_valid():
            patient = form.save()
            return HttpResponseRedirect("/prueba/resumendia/")
    return render(request, "secretaria/agenda_hoy/agregar_paciente.html", {'form': form})


# paciente
@login_required
def pacienteinicio(request):
    return render(request, "paciente/home/home.html", {})


@login_required
def pacientedetalles(request):
    return render(request, "paciente/home/detalles.html", {})


@login_required
def pacientecambiopass(request):
    return render(request, "paciente/common/cambiar_constrasena.html", {})


# nucleo
class ParentCreateView(CreateView):
    model = Nucleo
    fields = ["matricula"]

    def get_context_data(self, **kwargs):
        # we need to overwrite get_context_data
        # to make sure that our formset is rendered
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["integrantes"] = IntegranteFormset(self.request.POST)
        else:
            data["integrantes"] = IntegranteFormset()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        children = context["integrantes"]
        self.object = form.save()
        if children.is_valid():
            children.instance = self.object
            children.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("nucleos:list")

# actualizar nucleo
class NucleoUpdateView(UpdateView):
    model = Nucleo
    fields = ["matricula"]
    def get_context_data(self, **kwargs):
        # we need to overwrite get_context_data
        # to make sure that our formset is rendered.
        # the difference with CreateView is that
        # on this view we pass instance argument
        # to the formset because we already have
        # the instance created
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["integrantes"] = IntegranteFormset(self.request.POST, instance=self.object)
        else:
            data["integrantes"] = IntegranteFormset(instance=self.object)
        return data
    def form_valid(self, form):
        context = self.get_context_data()
        children = context["integrantes"]
        self.object = form.save()
        if children.is_valid():
            children.instance = self.object
            children.save()
        return super().form_valid(form)
    def get_success_url(self):
        return reverse("nucleos:list")




# frontpage
@login_required
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
            if userprofile.user_tipo == 'SECRETARIA':
                return HttpResponseRedirect('/prueba/resumendia/')
            elif user.UserProfile.user_tipo == 'DOCTOR':
                return HttpResponseRedirect('/prueba/pacientesdeldia/')
            else:
                return HttpResponseRedirect('/prueba/pacienteincio')
    return render(request, 'frontpage/index.html')
