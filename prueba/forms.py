from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Paciente, Cita, Consulta, Nucleo, Integrante


class IngresoForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password',)


class PacienteForm(ModelForm):
    class Meta:
        model = Paciente
        fields = ('documento', 'nombre', 'primer_apellido', 'segundo_apellido', 'fecha_nacimiento', 'email', 'celular',
                  'nucleo_activo')


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
        fields = ('matricula','titular')


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