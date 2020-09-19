from django.forms import ModelForm
from django import forms
from django.forms.models import inlineformset_factory, BaseInlineFormSet
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
        fields = ('documento', 'nombre', 'primer_apellido', 'segundo_apellido', 'direccion', 'fecha_nacimiento', 'email', 'celular',
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


class AntecedenteForm(ModelForm):
    class Meta:
        model = AntecedentesClinicos
        fields = ('paciente', 'fumador', 'alcohol', 'coproparasitario', 'aparato_digestivo', 'desc_aparato_digestivo',
                  'dermatologicos', 'desc_dermatologicos',
                  'alergias', 'desc_alergias', 'autoinmnunes', 'desc_autoinmnunes', 'oncologicas', 'desc_oncologicas',
                  'hematologicas', 'desc_hematologicas', 'intervenciones', 'desc_intervenciones', 'toma_medicacion',
                  'desc_medicacion', 'endocrinometabolico', 'desc_endocrinometabolico', 'cardiovascular',
                  'desc_cardiovascular', 'nefrourologicos', 'desc_nefrourologicos', 'observations')


PacienteIntegranteFormset = inlineformset_factory(
    Nucleo,
    Integrante,
    fields=('nucleo', 'relacion_nucleo'),
    extra=6)


class BaseIntegrantesFormset(BaseInlineFormSet):
    """
    Formulario base para editar los integrantes de un nucleo

    """

    def is_valid(self):
        """
        Also validate the nested formsets.
        """
        result = super().is_valid()

        if self.is_bound:
            for form in self.forms:
                if hasattr(form, 'nested'):
                    result = result and form.nested.is_valid()

        return result

    def clean(self):
        """
        Si un formulario principal no tiene datos, pero sus formularios anidados los tienen, deberíamos
         devolver un error, porque no podemos guardar integrantes sin nucleo

        """
        super().clean()

        for form in self.forms:
            if not hasattr(form, 'nested') or self._should_delete_form(form):
                continue

            if self._is_adding_nested_inlines_to_empty_form(form):
                form.add_error(
                    field=None,
                    error=_('Esta tratando de agregar integrantes a un nucleo'
                            'que no existe'
                            'Por favor ingrese la informacion del nucleo '
                            'e intente luego con los integrantes'))

    def save(self, commit=True):
        """
        Also save the nested formsets.
        """
        result = super().save(commit=commit)

        for form in self.forms:
            if hasattr(form, 'nested'):
                if not self._should_delete_form(form):
                    form.nested.save(commit=commit)

        return result

    def _is_adding_nested_inlines_to_empty_form(self, form):
        """
        Are we trying to add data in nested inlines to a form that has no data?
        e.g. Adding Images to a new Book whose data we haven't entered?
        """
        if not hasattr(form, 'nested'):
            # A basic form; it has no nested forms to check.
            return False

        if is_form_persisted(form):
            # We're editing (not adding) an existing model.
            return False

        if not is_empty_form(form):
            # The form has errors, or it contains valid data.
            return False

        # All the inline forms that aren't being deleted:
        non_deleted_forms = set(form.nested.forms).difference(
            set(form.nested.deleted_forms)
        )

        # At this point we know that the "form" is empty.
        # In all the inline forms that aren't being deleted, are there any that
        # contain data? Return True if so.
        return any(not is_empty_form(nested_form) for nested_form in non_deleted_forms)


#

def is_empty_form(form):
    """
    A form is considered empty if it passes its validation,
    but doesn't have any data.

    This is primarily used in formsets, when you want to
    validate if an individual form is empty (extra_form).
    """
    if form.is_valid() and not form.cleaned_data:
        return True
    else:
        # Either the form has errors (isn't valid) or
        # it doesn't have errors and contains data.
        return False


def is_form_persisted(form):
    """
    Does the form have a model instance attached and it's not being added?
    e.g. The form is about an existing Book whose data is being edited.
    """
    if form.instance and not form.instance._state.adding:
        return True
    else:
        # Either the form has no instance attached or
        # it has an instance that is being added.
        return False
