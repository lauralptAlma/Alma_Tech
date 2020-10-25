import json
import os
from operator import attrgetter

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth
# from django.core.checks import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.views import View
from django.db.models import Q
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, ListView, DetailView, FormView, TemplateView
from django.views.generic.detail import SingleObjectMixin
from .forms import CitaForm, PacienteForm, AntecedenteForm, ConsultaForm, ConsultaCPOForm
from .models import UserProfile, Consulta, Paciente, Cita, Nucleo, AntecedentesClinicos, CPO
from datetime import datetime
from django.utils import formats
from datetime import date
# Imports needed for pdf generation
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.views.generic import ListView
from itertools import chain
from django.template.loader import render_to_string


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
        agenda_hoy = Cita.objects.filter(fecha=date.today(), doctor=request.user).order_by('hora')
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
    return render(request, "secretaria/agenda_hoy/agregar_cita.html", {'form': form})


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
    return render(request, "almaFront/consultas/agregar_tratamiento.html", {'form': form})


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
    return render(request, "almaFront/doctor/profesionales.html", {'profesionales': profesionales})


@login_required(login_url="/")
def listapacientes(request):
    pacientes = Paciente.objects.all().order_by('primer_apellido')
    busqueda = request.GET.get("buscar")
    if busqueda:
        pacientes = pacientes.filter(
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
    antecedentes_paciente = AntecedentesClinicos.objects.filter(paciente_id=paciente_id).last()
    consultas_paciente = Consulta.objects.filter(paciente_id=paciente_id).order_by('-id')
    if antecedentes_paciente:
        antecedentes = [antecedentes_paciente.fumador, antecedentes_paciente.alcohol,
                        antecedentes_paciente.coproparasitario, antecedentes_paciente.aparato_digestivo,
                        antecedentes_paciente.dermatologicos,
                        antecedentes_paciente.alergias, antecedentes_paciente.autoinmunes,
                        antecedentes_paciente.oncologicas,
                        antecedentes_paciente.hematologicas, antecedentes_paciente.intervenciones,
                        antecedentes_paciente.toma_medicacion,
                        antecedentes_paciente.endocrinometabolico,
                        antecedentes_paciente.cardiovascular, antecedentes_paciente.nefrourologicos,
                        antecedentes_paciente.osteoarticulares]
        antecedentes_negativos = antecedentes.count("NO") + antecedentes.count("['NO']")
        if antecedentes_negativos == 15:
            sin_patologias = True
    if consultas_paciente:
        consultas_paciente = consultas_paciente[:3]
    return render(request, "almaFront/pacientes/paciente.html",
                  {'patient': paciente, 'antecedentes': antecedentes_paciente, 'consultas': consultas_paciente,
                   'sin_patologias': sin_patologias})


@login_required(login_url="/")
def verhistoriageneral(request, paciente_id):
    paciente = Paciente.objects.get(paciente_id=paciente_id)
    consultas_list = Consulta.objects.filter(paciente_id=paciente_id).order_by('-id')
    paginator = Paginator(consultas_list, 10)  # Show 10 treatments per page.
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(request, "almaFront/pacientes/patient_treatments_history.html",
                  {'patient': paciente, 'treatments': page_obj})


@login_required(login_url="/")
def verCPO(request, paciente_id):
    paciente = Paciente.objects.get(paciente_id=paciente_id)
    cpos_list = CPO.objects.filter(paciente_id=paciente_id).order_by('-cpo_id')
    paginator = Paginator(cpos_list, 1)  # Show 1 cpo per page.
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(request, "almaFront/pacientes/patient_cpo.html",
                  {'patient': paciente, 'page_obj': page_obj})


# Get patitent clinical background
def getantecedentes(paciente_id):
    antecedentes_list = AntecedentesClinicos.objects.filter(paciente_id=paciente_id).last()
    if antecedentes_list:
        antecedentes_list.creado = formats.date_format(antecedentes_list.creado, "SHORT_DATE_FORMAT")
        antecedentes_list.endocrinometabolico = eval(antecedentes_list.endocrinometabolico)
        antecedentes_list.cardiovascular = eval(antecedentes_list.cardiovascular)
        for c in antecedentes_list.cardiovascular:
            if c == 'H.T.A.':
                c_index = antecedentes_list.cardiovascular.index(c)
                antecedentes_list.cardiovascular[c_index] = 'Hipertensión arterial'
            if c == 'I.A.M':
                c_index = antecedentes_list.cardiovascular.index(c)
                antecedentes_list.cardiovascular[c_index] = 'Infarto agudo de miocardio'
        antecedentes_list.nefrourologicos = eval(antecedentes_list.nefrourologicos)
        antecedentes_list.osteoarticulares = eval(antecedentes_list.osteoarticulares)
    return antecedentes_list


@login_required(login_url="/")
def verantecedentes(request, paciente_id):
    paciente = Paciente.objects.get(paciente_id=paciente_id)
    antecedentes_list = getantecedentes(paciente_id)
    return render(request, "almaFront/pacientes/patient_background.html",
                  {'patient': paciente, 'antecedentes': antecedentes_list})


'''@login_required(login_url="/")
def verantecedentes(request, paciente_id):
    paciente = Paciente.objects.get(paciente_id=paciente_id)
    antecedentes_list = AntecedentesClinicos.objects.filter(paciente_id=paciente_id).last()
    if antecedentes_list:
        antecedentes_list.creado = formats.date_format(antecedentes_list.creado, "SHORT_DATE_FORMAT")
        antecedentes_list.endocrinometabolico = eval(antecedentes_list.endocrinometabolico)
        antecedentes_list.cardiovascular = eval(antecedentes_list.cardiovascular)
        for c in antecedentes_list.cardiovascular:
            if c == 'H.T.A.':
                c_index = antecedentes_list.cardiovascular.index(c)
                antecedentes_list.cardiovascular[c_index] = 'Hipertensión arterial'
            if c == 'I.A.M':
                c_index = antecedentes_list.cardiovascular.index(c)
                antecedentes_list.cardiovascular[c_index] = 'Infarto agudo de miocardio'
        antecedentes_list.nefrourologicos = eval(antecedentes_list.nefrourologicos)
        antecedentes_list.osteoarticulares = eval(antecedentes_list.osteoarticulares)
    return render(request, "almaFront/pacientes/patient_background.html",
                  {'patient': paciente, 'antecedentes': antecedentes_list})'''


@login_required(login_url="/")
def historiapaciente(request, paciente_id):
    paciente = Paciente.objects.get(paciente_id=paciente_id)
    return render(request, "almaFront/ver_historia.html", {'patient': paciente})


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
                return HttpResponseRedirect('/dentalE/resumendia/', {'user': userprofile})
            elif userprofile.user_tipo == 'DOCTOR':
                return HttpResponseRedirect('/dentalE/pacientesdeldia/', {'user': userprofile})
            else:
                return HttpResponseRedirect('/dentalE/pacienteincio', {'user': userprofile})
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
    return render(request, "almaFront/agregar_antecedentes_clinicos.html", {'form': form})


def logout_view(request):
    logout(request)
    return redirect('ingreso')


def build_clean_teeth_dic(teeth_list, status):
    list_clean = {}
    if teeth_list:
        for teeth in teeth_list:
            cara_list = teeth[0]
            pieza_list = teeth[-2] + teeth[-1]
            list_dic = dict(cara=[cara_list], pieza=pieza_list)
            if pieza_list in list_clean:
                existing_list_caras = list_clean[pieza_list][status].get('cara')
                existing_list_caras.append(cara_list)
                list_clean[pieza_list][status] = dict(cara=existing_list_caras,
                                                      pieza=pieza_list)
            else:
                list_clean[pieza_list] = {status: list_dic}
    return list_clean


def merge(a, b, path=None):
    # merges b into a
    if path is None:
        path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass  # same leaf value
            else:
                raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a


'''def getcpo(patient):
    cpos = CPO.objects.filter(paciente_id=patient).order_by('-cpo_id')
    if cpos:
        cpo_clean = {}
        for c in cpos:
            c.contenido_cpo = eval(c.contenido_cpo)
            caries = c.contenido_cpo['cariados']
            caries_clean = build_clean_teeth_dic(caries, 'caries')
            obturaciones = c.contenido_cpo['obturados']
            obturaciones_clean = build_clean_teeth_dic(obturaciones, 'obturados')
            perdidos = c.contenido_cpo['perdidos']
            perdidas_clean = {}
            ausentes = c.contenido_cpo['ausentes']
            ausentes_clean = {}
            if perdidos:
                for p in perdidos:
                    pieza_perdida = p[-2] + p[-1]
                    perdidas_dic = dict(pieza=pieza_perdida)
                    perdidas_clean[pieza_perdida] = {'perdidas': perdidas_dic}
            if ausentes:
                for a in ausentes:
                    pieza_ausente = a[-2] + a[-1]
                    ausentes_dic = dict(pieza=pieza_ausente)
                    ausentes_clean[pieza_ausente] = {'ausentes': ausentes_dic}
            z = merge(caries_clean, obturaciones_clean)
            cpo = z.copy()
            cpo.update(perdidas_clean)
            cpo.update(ausentes_clean)
            c.contenido_cpo = cpo
    return cpos'''


def clean_tooth(teeth):
    list_clean = []
    if teeth:
        for t in teeth:
            tooth = t[-2] + t[-1]
            if tooth in list_clean:
                pass
            else:
                list_clean.append(tooth)
    return list_clean


def getcpo(patient):
    cpos = CPO.objects.filter(paciente_id=patient).order_by('-cpo_id')
    if cpos:
        cpo_clean = {}
        for c in cpos:
            c.contenido_cpo = eval(c.contenido_cpo)
            caries = c.contenido_cpo['cariados']
            obturaciones = c.contenido_cpo['obturados']
            perdidos = c.contenido_cpo['perdidos']
            perdidos_clean = clean_tooth(perdidos)
            ausentes = c.contenido_cpo['ausentes']
            ausentes_clean = clean_tooth(ausentes)
            caries_clean = []
            list_clean= {}
            for teeth in caries:
                cara_list = teeth[0]
                pieza_list = teeth[-2] + teeth[-1]
                list_dic = dict(cara=[cara_list], pieza=pieza_list)
                if pieza_list in list_clean:
                    existing_list_caras = list_clean[pieza_list].get('cara')
                    existing_list_caras.append(cara_list)
                    list_clean[pieza_list] = dict(cara=existing_list_caras,
                                                          pieza=pieza_list)
                else:
                    list_clean[pieza_list] = {'cariados': list_dic}
                caries_clean.append([list_clean[pieza_list]['cariados']['pieza'], list_clean[pieza_list]['cariados']['cara']])
            c.caries = caries_clean
            c.obturaciones = obturaciones
            c.perdidos = perdidos_clean
            c.ausentes = ausentes_clean
            print('AHORA TAAAAA')
            print(caries_clean)
    return cpos


def link_callback(uri, rel):
    # convert URIs to absolute system paths
    if uri.startswith(settings.MEDIA_URL):
        path = os.path.join(settings.MEDIA_ROOT,
                            uri.replace(settings.MEDIA_URL, ""))
    elif uri.startswith(settings.STATIC_URL):
        path = os.path.join(settings.STATIC_ROOT,
                            uri.replace(settings.STATIC_URL, ""))
    else:
        # handle absolute uri (i.e., "http://my.tld/a.png")
        return uri

    # make sure that the local file exists
    if not os.path.isfile(path):
        raise Exception(
            "Media URI must start with "
            f"'{settings.MEDIA_URL}' or '{settings.STATIC_URL}'")

    return path


def pacientes_render_pdf_view(request, *args, **kwargs):
    user = request.user
    paciente_id = kwargs.get('paciente_id')
    patient = get_object_or_404(Paciente, paciente_id=paciente_id)
    treatments = Consulta.objects.filter(paciente_id=paciente_id).order_by('-id')
    # cpos = CPO.objects.filter(paciente_id=paciente_id).order_by('-cpo_id')
    cpos = getcpo(paciente_id)
    all_ordered = sorted(
        chain(treatments, cpos),
        key=attrgetter('creado'), reverse=True)
    background = getantecedentes(paciente_id)
    # Template that we are going to use to render the pdf
    template_path = 'almaFront/historiapdf/pdf2.html'
    context = {'patient': patient, 'treatments': treatments, 'user': user, 'background': background, 'cpo': cpos,
               'all': all_ordered}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    # If download:
    # response['Content-Disposition'] = 'attachment; filename="historia-clínica.pdf"'
    # If display on browser
    response['Content-Disposition'] = 'filename="historia-clínica.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response,
        link_callback=link_callback)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
