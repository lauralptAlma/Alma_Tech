from django.contrib.auth.decorators import login_required
from django.core.checks import messages
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views import View
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, ListView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin

from .forms import CitaForm, PacienteForm
from .models import UserProfile, Consulta, Paciente, Cita, Nucleo
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
    consulta_hoy = Consulta.objects.filter(creado=date.today())
    return render(request, "secretaria/agenda_hoy/agenda_hoy.html",
                  {'agenda_hoy': agenda_hoy, 'consulta_hoy': consulta_hoy})


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
        form = PacienteForm(request.POST)
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


# nucleo e integrantes

class NucleoListView(ListView):
    model = Nucleo
    template_name = 'nucleo/nucleo_lista.html'


class NucleoDetailView(DetailView):
    model = Nucleo
    template_name = 'nucleo/nucleo_detalles.html'


class NucleoCreateView(CreateView):
    """
    Solo crea un nucleo nuevo,agrega integrantes se hace desde
    NucleoIntegrantesUpdateView().
    """
    model = Nucleo
    template_name = 'nucleo/nucleo_crear.html'
    fields = ['matricula','titular']

    def form_valid(self, form):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'EL nucleo ha sido agregado con exito'
        )

        return super().form_valid(form)


class NucleoIntegrantesUpdateView(SingleObjectMixin, FormView):
    """
    Para agregar integrantes a un nucleo o editarlos
    """

    model = Nucleo
    template_name = 'nucleo/nucleo_integrantes_update.html'

    def get(self, request, *args, **kwargs):
        # El nucleo que estamos editando:
        self.object = self.get_object(queryset=Nucleo.objects.all())
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # El nuecleo que estamos editando:
        self.object = self.get_object(queryset=Nucleo.objects.all())
        return super().post(request, *args, **kwargs)

    def get_form(self, form_class=None):
        """
        Use our big formset of formsets, and pass in the Publisher object.
        """

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        form.save()

        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Informacion actualizada'
        )

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('nucleo:nucleo_detalles', kwargs={'pk': self.object.pk})


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

# antecedentes paciente
