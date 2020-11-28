import ast
import pandas as pd
import base64
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
# from django.core.checks import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.utils import formats
from django.views.generic import CreateView, ListView, DetailView, \
    FormView
from django.views.generic.detail import SingleObjectMixin
from dentalE.historiaPdf import pdf, clean_cpo
from .forms import CitaForm, PacienteForm, AntecedenteForm, ConsultaForm, \
    ConsultaCPOForm, ContactoForm, OrtodonciaForm, TermsForm
from .models import UserProfile, Consulta, Paciente, Cita, Nucleo, \
    AntecedentesClinicos, CPO, Ortodoncia, Terms
from datetime import date
# Imports needed for pdf generation
from rest_framework.views import APIView
from rest_framework.response import Response


# doctor


@login_required(login_url="/")
def resumendia(request):
    terms = TermsForm
    busqueda = request.GET.get("buscar")
    if request.method == 'POST':
        form = TermsForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return HttpResponseRedirect("/dentalE/resumendia/")
    accepted = Terms.objects.filter(user=request.user).order_by('alta').last()
    if not accepted:
        return render(request, "almaFront/bases/terms.html",
                      {'terms': terms})
    try:
        userprofile = UserProfile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        return render(request, 'almaFront/bases/404.html', status=404)
    if userprofile.user_tipo == 'SECRETARIA' and accepted.agreement:
        agenda_hoy = Cita.objects.filter(fecha=date.today()).order_by('hora')
        if busqueda:
            agenda_hoy = agenda_hoy.filter(
                Q(paciente__nombre__contains=busqueda) |
                Q(paciente__primer_apellido__contains=busqueda) |
                Q(paciente__documento__contains=busqueda)
            ).distinct().order_by('hora')
        return render(request, 'almaFront/secretaria/agenda_hoy.html',
                      {'agenda_hoy': agenda_hoy})
    elif userprofile.user_tipo == 'DOCTOR' and accepted.agreement:
        agenda_hoy = Cita.objects.filter(fecha=date.today(),
                                         doctor=request.user).order_by('hora')
        if busqueda:
            agenda_hoy = agenda_hoy.filter(
                Q(paciente__nombre__contains=busqueda) |
                Q(paciente__primer_apellido__contains=busqueda) |
                Q(paciente__documento__contains=busqueda)
            ).distinct().order_by('hora')
        return render(request, 'almaFront/secretaria/agenda_hoy.html',
                      {'agenda_hoy': agenda_hoy})
    else:
        return render(request, "almaFront/bases/terms.html",
                      {'terms': terms})


@login_required(login_url="/")
def agregarcita(request):
    form = CitaForm()
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            form.save()
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
            form.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                'Cita agregada exitosamente!'
            )
            return HttpResponseRedirect("/dentalE/agregarcita")
    return render(request, "secretaria/agenda_hoy/agregar_cita.html",
                  {'citasList': citas, 'form': form})


@login_required(login_url="/")
def edit_cita(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)
    citas = Cita.objects.all()
    eliminar = request.POST.get('eliminar')
    cancelar = request.POST.get('cancelar')
    template = 'secretaria/agenda_hoy/agregar_cita.html'
    if request.method == "POST" and cancelar:
        return HttpResponseRedirect("/dentalE/agregarcita")
    elif request.method == "POST" and eliminar:
        cita.delete()
        messages.add_message(
            request,
            messages.SUCCESS,
            'Cita eliminada exitosamente!'
        )
        return HttpResponseRedirect("/dentalE/agregarcita")
    elif request.method == "POST":
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
def agregarortodoncia(request):
    form = OrtodonciaForm()
    if request.method == 'POST':
        form = OrtodonciaForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.doctor = request.user
            form.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                'Consulta guardada exitosamente!'
            )
            return HttpResponseRedirect("/dentalE/agregarortodoncia/")
    return render(request, "almaFront/consultas/agregar_ortodoncia.html",
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
                return HttpResponseRedirect(
                    "/dentalE/pacientedetalles/{}".format(paciente_id))
        except Exception as e:
            messages.add_message(
                request,
                messages.ERROR,
                'Error al editar paciente, error: {}'.format(e)
            )
    else:
        form = PacienteForm(instance=paciente)
        form.fields['documento'].widget.attrs['readonly'] = True
    form.fields['documento'].widget.attrs['readonly'] = True
    context = {'form': form,
               'paciente': paciente
               }
    return render(request, template, context)


def encode_image(img):
    img_content = img.read()
    return base64.b64encode(img_content).decode('utf-8')


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
    ortodoncia_paciente = Ortodoncia.objects.filter(
        paciente_id=paciente_id).order_by('-creado').first()
    if ortodoncia_paciente:
        image_data = encode_image(ortodoncia_paciente.image)
        ortodoncia_paciente.image = image_data
    return render(request, "almaFront/pacientes/paciente.html",
                  {'patient': paciente, 'antecedentes': antecedentes_paciente,
                   'consultas': consultas_paciente,
                   'sin_patologias': sin_patologias,
                   'ortodoncia': ortodoncia_paciente})


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


# Get patient clinical background
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


# Get patient orthodontics background


def getconsultasortodoncia(paciente_id):
    ortodoncia_paciente = Ortodoncia.objects.filter(
        paciente_id=paciente_id).order_by('-creado')
    if ortodoncia_paciente:
        for o in ortodoncia_paciente:
            if o.image:
                image_data = encode_image(o.image)
                o.image = image_data
    return ortodoncia_paciente


@login_required(login_url="/")
def verhistoriaortodoncia(request, paciente_id):
    paciente = Paciente.objects.get(paciente_id=paciente_id)
    ortodoncia_paciente = getconsultasortodoncia(paciente_id)
    paginator = Paginator(ortodoncia_paciente, 1)  # Show 1 cpo per page.
    page_number = request.GET.get('page', 1)
    ortodoncia_obj = paginator.get_page(page_number)
    return render(request, "almaFront/pacientes/patient_orthodontics.html",
                  {'patient': paciente, 'ortodoncia_obj': ortodoncia_obj})


@login_required(login_url="/")
def compararortodoncia(request, paciente_id):
    paciente = Paciente.objects.get(paciente_id=paciente_id)
    ortodoncia_paciente = getconsultasortodoncia(paciente_id)
    ortodoncia_imagenes = []
    if ortodoncia_paciente:
        for o in ortodoncia_paciente:
            if o.image:
                ortodoncia_imagenes.append(o)
    ortodoncia_comparativa = [ortodoncia_imagenes[0], ortodoncia_imagenes[-1]]
    print(ortodoncia_comparativa)
    return render(request,
                  "almaFront/pacientes/patient_orthodontics_beforeafter.html",
                  {'patient': paciente, 'ortodoncia': ortodoncia_comparativa})


# frontpage
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


# Historia clínica paciente pdf

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
        cpos = clean_cpo.get_cpo(paciente_id)
        ortodoncia = getconsultasortodoncia(paciente_id)
        # Template that we are going to use to render the pdf
        template_path = 'almaFront/historiapdf/historia_pdf.html'
        context = {'patient': patient, 'treatments': treatments, 'user': user,
                   'background': background, 'cpo': cpos,
                   'ortodoncia': ortodoncia}
        patient_name = patient.nombre + patient.primer_apellido
        filename = patient_name + "-HistoriaClínicaDental"
        response = pdf.generate_pdf(template_path, context, filename)
        return response
    else:
        return HttpResponseRedirect('account_logout')


@login_required(login_url="/")
def contacto(request):
    form = ContactoForm()
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            form.save()
            subject = "Usuario " + request.POST['nombre'] + ": " + \
                      request.POST['asunto']
            remitente = "\nEmail remitente:  " + request.POST['email']
            message = request.POST['mensaje'] + remitente
            email_from = settings.EMAIL_HOST_USER
            recipient_list = ['almatech20@gmail.com']
            try:
                send_mail(subject, message, email_from, recipient_list)
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    'Mensaje enviado exitosamente!'
                )
                return redirect("/dentalE/resumendia/")
            except Exception as e:
                messages.add_message(
                    request,
                    messages.ERROR,
                    'Error al enviar la consulta, error: {}'.format(e)
                )
        else:
            messages.add_message(
                request,
                messages.ERROR,
                'Hubo un error al enviar su mensaje, '
                'por favor intente nuevamente.'
            )
    return render(request, "almaFront/bases/contacto.html", {'form': form})


@login_required(login_url="/")
def terminos(request):
    if request.method == 'POST':
        return HttpResponseRedirect("/dentalE/resumendia/")
    return render(request, "almaFront/bases/terminos-y-condiciones.html")


@login_required(login_url="/")
def analisis(request):
    return render(request, "almaFront/charts.html")


@login_required(login_url="/")
def DataView(request):
    return render(request, "almaFront/charts.html")


@login_required(login_url="/")
def get_data(request, *args, **kwargs):
    try:
        userprofile = UserProfile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        return HttpResponse('Unauthorized', status=401)
    if userprofile.user_tipo == 'SECRETARIA':
        return HttpResponse('Unauthorized', status=401)
    elif userprofile.user_tipo == 'DOCTOR':
        data = {
            "sales": 100,
            "customers": 10,
        }
        return JsonResponse(data)  # http response


class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        pacientes = Paciente.objects.all().values()
        pacientes_data_set = pd.DataFrame(pacientes)
        pacientes_por_depto = pacientes_data_set['ciudad'].value_counts()
        pacientes_por_depto = pacientes_por_depto.reset_index()
        pacientes_por_depto.columns = ['Departamento',
                                       'Cantidad']  # change column names
        deparamentos = pacientes_por_depto['Departamento'].tolist()
        cantidades = pacientes_por_depto['Cantidad'].tolist()
        data = {
            "labels": deparamentos,
            "values": cantidades,
        }

        pacientes_por_genero = pacientes_data_set['genero'].value_counts()
        pacientes_por_genero = pacientes_por_genero.reset_index()
        pacientes_por_genero.columns = ['Genero',
                                        'Cantidad']
        genero = pacientes_por_genero['Genero'].tolist()
        cantidad = pacientes_por_genero['Cantidad'].tolist()
        datos = {
            "labelsGen": genero,
            "valuesGen": cantidad,
        }

        antecedentes_paciente = AntecedentesClinicos.objects.all().values()
        antecedentes_data = pd.DataFrame(antecedentes_paciente)
        total_antecedentes = antecedentes_data[
            ['alcohol', 'fumador', 'aparato_digestivo', 'dermatologicos',
             'alergias', 'autoinmunes', 'oncologicas',
             'hematologicas']]

        total_antecedentes = total_antecedentes.reset_index()

        soloSI = total_antecedentes.groupby(['fumador']).size().reset_index(
            name='cantidad')
        soloSIA = total_antecedentes.groupby(['alcohol']).size().reset_index(
            name='cantidad')
        soloSIAg = total_antecedentes.groupby(
            ['aparato_digestivo']).size().reset_index(name='cantidad')
        soloSID = total_antecedentes.groupby(
            ['dermatologicos']).size().reset_index(name='cantidad')
        soloSIAl = total_antecedentes.groupby(['alergias']).size().reset_index(
            name='cantidad')
        soloSIAi = total_antecedentes.groupby(
            ['autoinmunes']).size().reset_index(name='cantidad')
        soloSIO = total_antecedentes.groupby(
            ['oncologicas']).size().reset_index(name='cantidad')
        soloSIH = total_antecedentes.groupby(
            ['hematologicas']).size().reset_index(name='cantidad')

        fumador = soloSI.loc[soloSI['fumador'] == 'SI']
        alcohol = soloSIA.loc[soloSIA['alcohol'] == 'SI']
        digestivo = soloSIAg.loc[soloSIAg['aparato_digestivo'] == 'SI']
        dermatologico = soloSID.loc[soloSID['dermatologicos'] == 'SI']
        alergias = soloSIAl.loc[soloSIAl['alergias'] == 'SI']
        autoinmunes = soloSIAi.loc[soloSIAi['autoinmunes'] == 'SI']
        oncologicas = soloSIO.loc[soloSIO['oncologicas'] == 'SI']
        hematologicas = soloSIH.loc[soloSIH['hematologicas'] == 'SI']

        prueba_f = fumador.transpose().T
        prueba_a = alcohol.transpose().T
        prueba_d = digestivo.transpose().T
        prueba_de = dermatologico.transpose().T
        prueba_al = alergias.transpose().T
        prueba_ai = autoinmunes.transpose().T
        prueba_o = oncologicas.transpose().T
        prueba_h = hematologicas.transpose().T

        data_final = pd.concat(
            [prueba_a, prueba_f, prueba_d, prueba_de, prueba_al, prueba_ai,
             prueba_o, prueba_h],
            axis=0)
        p = pd.melt(data_final, id_vars='cantidad')
        p = p.loc[p['value'] == 'SI']
        antecedente = p['variable'].tolist()
        cantidad = p['cantidad'].tolist()

        def switch_antecedentes(argument):
            switcher = {
                "alcohol": "Alcohol",
                "fumador": "Fumador",
                "aparato_digestivo": "Aparato Digestivo",
                "dermatologicos": "Dermatológicos",
                "alergias": "Alergias",
                "autoinmunes": "Autoinmunes",
                "oncologicas": "Oncológicas",
                "hematologicas": "Hematológicas"
            }
            return switcher.get(argument, "Antecedente inválido")

        for a in antecedente:
            indice = antecedente.index(a)
            antecedente[indice] = switch_antecedentes(a)

        datosA = {
            "labelsAnt": antecedente,
            "valuesAnt": cantidad,
        }

        # Cantidad de consultas por tipo
        consultaso = Ortodoncia.objects.all().values()
        consultas0_data_set = pd.DataFrame(consultaso)
        consultasg = Consulta.objects.all().values()
        consultasg_data_set = pd.DataFrame(consultasg)
        # consulta general
        consultasg_data_set['tipo'] = 'GENERAL'
        consultasg_data_set = consultasg_data_set['tipo'].value_counts()
        consultasg_data_set = consultasg_data_set.reset_index()
        consultasg_data_set.columns = ['Tipo',
                                       'Cantidad']  # change column names
        # consulta ortodoncia ortopedia
        consultas_ort = consultas0_data_set['tipo'].value_counts()
        consultas_ort = consultas_ort.reset_index()
        consultas_ort.columns = ['Tipo',
                                 'Cantidad']  # change column names
        # consultas totales
        consultasT = pd.concat([consultasg_data_set, consultas_ort])
        tipo = consultasT['Tipo'].tolist()
        cantidades = consultasT['Cantidad'].tolist()
        dataTipos = {
            "labelsT": tipo,
            "valuesT": cantidades,

        }

        data = {"data": data, "datos": datos, "datosA": datosA,
                "datosB": dataTipos}
        return Response(data)


@login_required(login_url="/")
def ChartPatient(request, paciente_id):
    paciente = get_object_or_404(
        Paciente.objects.filter(paciente_id=paciente_id))
    consulta = Consulta.objects.filter(paciente_id=paciente_id).values()
    data = {}
    data_caries = {}
    if consulta:
        pacientes_data_set = pd.DataFrame(consulta)
        pacientes_por_consulta = pacientes_data_set['creado'].value_counts()
        pacientes_por_consulta = pacientes_por_consulta.reset_index()
        pacientes_por_consulta.columns = ['Fecha', 'Cantidad']
        fechas = pd.to_datetime(pacientes_por_consulta['Fecha'],
                                format='%Y-%m-%d')
        consultas = fechas.astype(str).tolist()
        cantidad = pacientes_por_consulta['Cantidad'].tolist()
        data = {
            "labels": consultas,
            "values": cantidad,
        }

    cpo_fechas = []
    cantidad_caries = []
    cpos = reversed(clean_cpo.get_cpo(paciente_id))
    if cpos:
        i = 0
        for c in cpos:
            cpo_fechas.append(c.creado.strftime("%Y-%m-%d"))
            i = i + len(c.caries)
            cantidad_caries.append(i)
        data_caries = {
            "labels": cpo_fechas,
            "values": cantidad_caries,
        }

    return render(request, "almaFront/pacientes/patient_statistics.html",
                  {'data': data, 'data_caries': data_caries,
                   'patient': paciente})


# Vistas para funcionalidades no completadas
# paciente
@login_required(login_url="/")
def pacienteinicio(request):
    return render(request, "paciente/home/home.html", {})


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
