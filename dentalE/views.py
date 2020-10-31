import json

from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth
from django.core.mail import send_mail
from django.conf import settings
# from django.core.checks import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.views import View, generic
from django.db.models import Q
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, ListView, DetailView, \
    FormView, TemplateView
from django.views.generic.detail import SingleObjectMixin
from .forms import CitaForm, PacienteForm, AntecedenteForm, ConsultaForm, \
    ConsultaCPOForm, ContactoForm
from .models import UserProfile, Consulta, Paciente, Cita, Nucleo, \
    AntecedentesClinicos, CPO
from datetime import date


def pruebaBaseFront(request):
    return render(request, "almaFront/cpo.html")


# doctor
@login_required(login_url="/")
def resumendia(request):
    try:
        userprofile = UserProfile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        return render(request, 'almaFront/bases/404.html')
    if userprofile.user_tipo == 'SECRETARIA':
        agenda_hoy = Cita.objects.filter(fecha=date.today()).order_by('hora')
        return render(request, 'almaFront/secretaria/agenda_hoy.html',
                      {'agenda_hoy': agenda_hoy})
    elif userprofile.user_tipo == 'DOCTOR':
        agenda_hoy = Cita.objects.filter(fecha=date.today(),
                                         doctor=request.user).order_by('hora')
        return render(request, 'almaFront/secretaria/agenda_hoy.html',
                      {'agenda_hoy': agenda_hoy})
    else:
        return HttpResponseRedirect('account_logout')


@login_required(login_url="/")
def agregarcita(request):
    form = CitaForm()
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            cita = form.save()
            return HttpResponseRedirect("/dentalE/resumendia/")
    return render(request, "secretaria/agenda_hoy/agregar_cita.html",
                  {'form': form})


@login_required(login_url="/")
def CalendarPage(request):
    citas = Cita.objects.all()
    form = CitaForm()
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            cita = form.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                'Cita agregada exitosamente!'
            )
            return HttpResponseRedirect("/dentalE/resumendia/")
    return render(request, "secretaria/agenda_hoy/agregar_cita.html",
                  {'citasList': citas, 'form': form})


@login_required(login_url="/")
def edit_cita(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)
    citas = Cita.objects.all()
    template = 'secretaria/agenda_hoy/agregar_cita.html'
    if request.method == "POST":
        form = CitaForm(request.POST, instance=cita)
        try:
            if form.is_valid():
                form.save()
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    'Cita editada exitosamente!'
                )
            return HttpResponseRedirect("/dentalE/agregarcita")
        except Exception as e:
            messages.add_message(
                request,
                messages.ERROR,
                'Error al editar cita, error: {}'.format(e)
            )
    else:
        form = CitaForm(instance=cita)
    context = {'form': form,
               'cita': cita,
               'citasList': citas
               }
    return render(request, template, context)


@login_required(login_url="/")
def delete_cita(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)
    citas = Cita.objects.all()
    template = 'secretaria/agenda_hoy/agregar_cita.html'
    if request.method == 'POST':
        form = CitaForm(request.POST, instance=cita)
        if form.is_valid():
            cita = form.save()
            cita.delete()
            messages.add_message(
                request,
                messages.SUCCESS,
                'Cita eliminada exitosamente!'
            )
            return HttpResponseRedirect("/dentalE/agregarcita")
    return render(request, "secretaria/agenda_hoy/agregar_cita.html",
                  {'citasList': citas, 'form': form})


@login_required(login_url="/")
def agregartratamiento(request):
    form = ConsultaForm()
    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            form.instance.doctor = request.user
            consulta = form.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                'Consulta agregada exitosamente!'
            )
            return HttpResponseRedirect("/dentalE/agregartratamiento/")
    return render(request, "almaFront/consultas/agregar_tratamiento.html",
                  {'form': form})


@login_required(login_url="/")
def agregarCPO(request):
    formCPO = ConsultaCPOForm()
    if request.method == 'POST':
        formCPO = ConsultaCPOForm(request.POST)
        if formCPO.is_valid():
            formCPO.instance.doctor = request.user
            consulta_cpo = formCPO.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                'CPO agregado exitosamente!'
            )
            return HttpResponseRedirect("/dentalE/agregarcpo/")
        # En un futuro redirigirlo al historial de CPOs del paciente
    return render(request, "almaFront/cpo.html", {'formCPO': formCPO})


@login_required(login_url="/")
def listaprofesionales(request):
    busqueda = request.GET.get("buscar")
    profesionales = UserProfile.objects.filter(user_tipo='DOCTOR')
    if busqueda:
        profesionales = UserProfile.objects.filter(
            Q(user_tipo__exact='DOCTOR') &
            Q(user__first_name__contains=busqueda) |
            Q(user__last_name__contains=busqueda)
        ).distinct()
    return render(request, "almaFront/doctor/profesionales.html",
                  {'profesionales': profesionales})


@login_required(login_url="/")
def listapacientes(request):
    busqueda = request.GET.get("buscar")
    pacientes = Paciente.objects.all().order_by('primer_apellido')
    if busqueda:
        pacientes = Paciente.objects.filter(
            Q(nombre__icontains=busqueda) |
            Q(primer_apellido__icontains=busqueda) |
            Q(documento__icontains=busqueda)
        ).distinct().order_by('primer_apellido')
    return render(request, "almaFront/pacientes/pacientes.html",
                  {'patients': pacientes})


class buscarView(TemplateView):
    def post(self, request, *args, **kwargs):
        return render(request, {'alma/pacientes/buscarpaciente.html'})


@login_required(login_url="/")
def agregarpaciente(request):
    form = PacienteForm()
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            patient = form.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                'Paciente agregado exitosamente!'
            )
            return HttpResponseRedirect("/dentalE/agregarpaciente/")
    return render(request, "almaFront/agregar_paciente.html", {'form': form})


# paciente
@login_required(login_url="/")
def pacienteinicio(request):
    return render(request, "paciente/home/home.html", {})


@login_required(login_url="/")
def pacientedetalles(request, paciente_id):
    sin_patologias = False
    paciente = Paciente.objects.get(paciente_id=paciente_id)
    antecedentes_paciente = AntecedentesClinicos.objects.filter(
        paciente_id=paciente_id).last()
    consultas_paciente = Consulta.objects.filter(
        paciente_id=paciente_id).order_by('-id')
    if antecedentes_paciente:
        antecedentes = [antecedentes_paciente.fumador,
                        antecedentes_paciente.alcohol,
                        antecedentes_paciente.coproparasitario,
                        antecedentes_paciente.aparato_digestivo,
                        antecedentes_paciente.dermatologicos,
                        antecedentes_paciente.alergias,
                        antecedentes_paciente.autoinmunes,
                        antecedentes_paciente.oncologicas,
                        antecedentes_paciente.hematologicas,
                        antecedentes_paciente.intervenciones,
                        antecedentes_paciente.toma_medicacion,
                        antecedentes_paciente.endocrinometabolico,
                        antecedentes_paciente.cardiovascular,
                        antecedentes_paciente.nefrourologicos,
                        antecedentes_paciente.osteoarticulares]
        antecedentes_negativos = antecedentes.count("NO") + antecedentes.count(
            "['NO']")
        if antecedentes_negativos == 15:
            sin_patologias = True
    if consultas_paciente:
        consultas_paciente = consultas_paciente[:3]
    return render(request, "almaFront/pacientes/paciente.html",
                  {'patient': paciente, 'antecedentes': antecedentes_paciente,
                   'consultas': consultas_paciente,
                   'sin_patologias': sin_patologias})


@login_required(login_url="/")
def verCPO(request, paciente_id):
    paciente = Paciente.objects.get(paciente_id=paciente_id)
    ultimo_cpo_paciente = CPO.objects.filter(paciente_id=paciente_id).last()
    return render(request, "almaFront/ver_cpo.html",
                  {'patient': paciente, 'cpo': ultimo_cpo_paciente})


@login_required(login_url="/")
def contacto(request):
    form = ContactoForm()
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            contacto = form.save()
            subject = request.POST['asunto'] + "  Usuario:  " + request.POST['nombre']
            message = request.POST['mensaje'] + " Email:  " + request.POST['email']
            email_from = settings.EMAIL_HOST_USER
            recipient_list = ['andrea.correa@estudiantes.utec.edu.uy']
            send_mail(subject, message, email_from, recipient_list)
            messages.add_message(
                request,
                messages.SUCCESS,
                'Mensaje enviado exitosamente!'
            )
        return redirect("/dentalE/resumendia/")
    return render(request, "almaFront/bases/contacto.html", {'form': form})


@login_required(login_url="/")
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
    fields = ['matricula', 'titular']

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
@login_required(login_url="/")
class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "almaFront/index.html")


def ingreso(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            userprofile = UserProfile.objects.get(user=user)
            if userprofile.user_tipo == 'SECRETARIA':
                return HttpResponseRedirect('/dentalE/resumendia/',
                                            {'user': userprofile})
            elif userprofile.user_tipo == 'DOCTOR':
                return HttpResponseRedirect('/dentalE/pacientesdeldia/',
                                            {'user': userprofile})
            else:
                return HttpResponseRedirect('/dentalE/pacienteincio',
                                            {'user': userprofile})
    return render(request, 'almaFront/index.html')


# def user_view(request):
# current_user = request.user
# return current_user.get_full_name()

# antecedentes paciente
@login_required(login_url="/")
def agregarantecedentes(request):
    form = AntecedenteForm()
    if request.method == 'POST':
        form = AntecedenteForm(request.POST)
        if form.is_valid():
            patient = form.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                'Atencedentes guardados exitosamente!'
            )
            return HttpResponseRedirect("/dentalE/agregarantecedentes/")
    return render(request, "almaFront/agregar_antecedentes_clinicos.html",
                  {'form': form})


def logout_view(request):
    logout(request)
    return redirect('ingreso')
