from django.forms import ModelForm
from django import forms
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Paciente, Cita, Consulta, Nucleo, Integrante, AntecedentesClinicos


class IngresoForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password',)


class PacienteForm(ModelForm):
    class Meta:
        model = Paciente
        fields = ('documento', 'nombre', 'primer_apellido', 'segundo_apellido', 'fecha_nacimiento', 'email', 'celular',
                  'nucleo_activo')

        widgets = {
            'documento': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Sin puntos ni guión', 'display': 'inline-block'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'display': 'inline-block'}),
            'primer_apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'segundo_apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'ej. 01/08/2012'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'celular': forms.TextInput(attrs={'class': 'form-control'}),
            'nucleo_activo': forms.TextInput(attrs={'class': 'form-control'}),
            'relacion_nucleo': forms.Select(attrs={'class': 'form-control'}),
        }


class CitaForm(ModelForm):
    class Meta:
        model = Cita
        fields = ('paciente', 'doctor', 'fecha', 'hora')


class ConsultaForm(ModelForm):
    class Meta:
        model = Consulta
        readonly_fields = 'creado'
        fields = ('paciente', 'doctor', 'diagnostico', 'tratamiento', 'indicaciones')


'''IntegranteFormset = inlineformset_factory(
    Nucleo, Integrante, fields=('matricula', 'paciente.nombre', 'paciente.documento')
)
'''


class NucleoForm(ModelForm):
    class Meta:
        model = Nucleo
        fields = ('matricula', 'titular')


def integrante_generator(request):
    IntegranteFormSet = inlineformset_factory(
        Paciente,
        Nucleo,
        form=PacienteForm,
        fields=('nombre', 'documento', 'direccion', 'matricula',),
        extra=4
    )
    form = NucleoForm()
    formset = IntegranteFormSet()
    if request.method == 'POST':
        form = NucleoForm(request.POST)
        formset = IntegranteFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            url = reverse('alguna_url')
            return HttpResponseRedirect(url)
    return render(request, 'nucleos.html', {
        'form': form,
        'formset': formset
    })


def IntegranteFormset():
    return None


class AntecedenteForm(ModelForm):
    class Meta:
        model = AntecedentesClinicos
        fields = ('paciente', 'fumador', 'alcohol', 'coproparasitario', 'aparato_digestivo', 'desc_aparato_digestivo',
                  'dermatologicos', 'desc_dermatologicos',
                  'alergias', 'desc_alergias', 'autoinmnunes', 'desc_autoinmnunes', 'oncologicas', 'desc_oncologicas',
                  'hematologicas', 'desc_hematologicas',
                  'hematologicas', 'desc_hematologicas', 'intervenciones', 'desc_intervenciones', 'toma_medicacion',
                  'desc_medicacion', 'endocrinometabolico',
                  'desc_endocrinometabolico', 'nefrourologicos', 'desc_nefrourologicos', 'observations')
