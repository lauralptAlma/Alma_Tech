import ast
from operator import attrgetter
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# from django.core.checks import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.views import View
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.views.generic import CreateView, ListView, \
    DetailView, FormView, TemplateView
from django.views.generic.detail import SingleObjectMixin
from django.utils import formats
from .forms import CitaForm, PacienteForm, AntecedenteForm, ConsultaForm, \
    ConsultaCPOForm
from .models import UserProfile, Consulta, Paciente, Cita, Nucleo, \
    AntecedentesClinicos, CPO
from datetime import date
# Imports needed for pdf generation
from itertools import chain
from dentalE.historiaPdf.pdf import generate_pdf


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
    if request.POST and form.is_valid():
        paciente = form.cleaned_data['paciente']
        doctor = form.cleaned_data['doctor']
        fecha = form.cleaned_data['fecha']
        hora = form.cleaned_data['hora']
        Cita.objects.get_or_create(
            paciente=paciente,
            doctor=doctor,
            fecha=fecha,
            hora=hora
        )
        return HttpResponseRedirect("/dentalE/resumendia/")
    return render(request, "secretaria/agenda_hoy/agregar_cita.html",
                  {'form': form})


@login_required(login_url="/")
def agregartratamiento(request):
    form = ConsultaForm()
    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            form.instance.doctor = request.user
            form.save()
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
            formCPO.save()
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


class BuscarView(TemplateView):
    def post(self, request, *args, **kwargs):
        return render(request, {'alma/pacientes/buscarpaciente.html'})


@login_required(login_url="/")
def agregarpaciente(request):
    form = PacienteForm()
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                'Paciente agregado exitosamente!'
            )
            return HttpResponseRedirect("/dentalE/agregarpaciente/")
    return render(request, "almaFront/agregar_paciente.html", {'form': form})


@login_required(login_url="/")
def edit_patient(request, paciente_id):
    paciente = get_object_or_404(Paciente, paciente_id=paciente_id)
    template = 'almaFront/agregar_paciente.html'
    if request.method == "POST":
        form = PacienteForm(request.POST, instance=paciente)
        try:
            if form.is_valid():
                form.save()
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    'Paciente editado exitosamente!'
                )
        except Exception as e:
            messages.add_message(
                request,
                messages.ERROR,
                'Error al editar paciente, error: {}'.format(e)
            )
    else:
        form = PacienteForm(instance=paciente)
    context = {'form': form,
               'paciente': paciente
               }
    return render(request, template, context)


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
def verhistoriageneral(request, paciente_id):
    paciente = Paciente.objects.get(paciente_id=paciente_id)
    consultas_list = Consulta.objects.filter(paciente_id=paciente_id).order_by(
        '-id')
    paginator = Paginator(consultas_list, 10)  # Show 10 treatments per page.
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(request,
                  "almaFront/pacientes/patient_treatments_history.html",
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
    antecedentes_list = AntecedentesClinicos.objects.filter(
        paciente_id=paciente_id).last()
    if antecedentes_list:
        antecedentes_list.creado = formats.date_format(
            antecedentes_list.creado, "SHORT_DATE_FORMAT")
        antecedentes_list.endocrinometabolico = ast.literal_eval(
            antecedentes_list.endocrinometabolico)
        antecedentes_list.cardiovascular = ast.literal_eval(
            antecedentes_list.cardiovascular)
        for c in antecedentes_list.cardiovascular:
            if c == 'H.T.A.':
                c_index = antecedentes_list.cardiovascular.index(c)
                antecedentes_list.cardiovascular[
                    c_index] = 'Hipertensión arterial'
            if c == 'I.A.M':
                c_index = antecedentes_list.cardiovascular.index(c)
                antecedentes_list.cardiovascular[
                    c_index] = 'Infarto agudo de miocardio'
        antecedentes_list.nefrourologicos = ast.literal_eval(
            antecedentes_list.nefrourologicos)
        antecedentes_list.osteoarticulares = ast.literal_eval(
            antecedentes_list.osteoarticulares)
    return antecedentes_list


@login_required(login_url="/")
def verantecedentes(request, paciente_id):
    paciente = Paciente.objects.get(paciente_id=paciente_id)
    antecedentes_list = getantecedentes(paciente_id)
    return render(request, "almaFront/pacientes/patient_background.html",
                  {'patient': paciente, 'antecedentes': antecedentes_list})


@login_required(login_url="/")
def historiapaciente(request, paciente_id):
    paciente = Paciente.objects.get(paciente_id=paciente_id)
    return render(request, "almaFront/ver_historia.html",
                  {'patient': paciente})


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


# antecedentes paciente
@login_required(login_url="/")
def agregarantecedentes(request):
    form = AntecedenteForm()
    if request.method == 'POST':
        form = AntecedenteForm(request.POST)
        if form.is_valid():
            form.save()
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


# Historia clínica paciente
# Limpieza de cpo

def build_clean_teeth_dic(teeth_list, status):
    list_clean = {}
    maxilla = ['1', '2', '5', '6']
    lower_jaw = ['3', '4', '7', '8']
    if teeth_list:
        for teeth in teeth_list:
            cara_list = cara(teeth[0])
            pieza_list = teeth[-2] + teeth[-1]
            if pieza_list[0] in maxilla and cara_list == 'Lingual/Paladino':
                cara_list = 'Paladino'
            if pieza_list[0] in lower_jaw and cara_list == 'Lingual/Paladino':
                cara_list = 'Lingual'
            list_dic = dict(cara=[cara_list], pieza=pieza_list)
            if pieza_list in list_clean:
                existing_list_caras = list_clean[pieza_list][status].get(
                    'cara')
                existing_list_caras.append(cara_list)
                list_clean[pieza_list][status] = dict(cara=existing_list_caras,
                                                      pieza=pieza_list)
            else:
                list_clean[pieza_list] = {status: list_dic}
    return list_clean


def cara(argument):
    switcher = {
        't': "Vestibular",
        'l': "Distal",
        'b': "Lingual/Paladino",
        'r': "Mesial",
        'c': "Oclusal",
    }
    return switcher.get(argument, "Cara de diente no válida")


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


def clean_decayed_filled(decayed_filled_teeth):
    decayed_filled_list = []
    for id, info in decayed_filled_teeth.items():
        pieza = id
        for key in info:
            caras = info[key]['cara']
        decayed_filled_list.append([pieza, caras])
    return decayed_filled_list


def get_cpo(patient):
    cpos = CPO.objects.filter(paciente_id=patient).order_by('-cpo_id')
    if cpos:
        for c in cpos:
            c.contenido_cpo = ast.literal_eval(c.contenido_cpo)
            caries = c.contenido_cpo['cariados']
            caries_dic = build_clean_teeth_dic(caries, 'cariados')
            caries_clean = clean_decayed_filled(caries_dic)
            obturaciones = c.contenido_cpo['obturados']
            obturaciones_dic = build_clean_teeth_dic(obturaciones, 'obturados')
            obturaciones_clean = clean_decayed_filled(obturaciones_dic)
            perdidos = c.contenido_cpo['perdidos']
            perdidos_clean = clean_tooth(perdidos)
            ausentes = c.contenido_cpo['ausentes']
            ausentes_clean = clean_tooth(ausentes)

            c.caries = caries_clean
            c.obturaciones = obturaciones_clean
            c.perdidos = perdidos_clean
            c.ausentes = ausentes_clean
    return cpos


@login_required(login_url="/")
def patient_render_background_pdf(request, *args, **kwargs):
    try:
        userprofile = UserProfile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        return render(request, 'almaFront/bases/404.html')
    if userprofile.user_tipo == 'SECRETARIA':
        return render(request, 'almaFront/bases/404.html')
    elif userprofile.user_tipo == 'DOCTOR':
        user = request.user
        paciente_id = kwargs.get('paciente_id')
        patient = get_object_or_404(Paciente, paciente_id=paciente_id)
        treatments = Consulta.objects.filter(paciente_id=paciente_id).order_by(
            '-id')
        background = getantecedentes(paciente_id)
        cpos = get_cpo(paciente_id)
        all_ordered = sorted(
            chain(treatments, cpos),
            key=attrgetter('creado'), reverse=True)

        # Template that we are going to use to render the pdf
        template_path = 'almaFront/historiapdf/historia_pdf.html'
        context = {'patient': patient, 'treatments': treatments, 'user': user,
                   'background': background, 'cpo': cpos,
                   'all': all_ordered}
        patient_name = patient.nombre + patient.primer_apellido
        filename = patient_name + "-HistoriaClínicaDental"
        response = generate_pdf(template_path, context, filename)
        return response
    else:
        return HttpResponseRedirect('account_logout')
