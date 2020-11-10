from django.forms import ModelForm
from django import forms
from django.forms.models import inlineformset_factory, BaseInlineFormSet
from bootstrap_datepicker_plus import DatePickerInput
from django.contrib.auth.models import User
from django.forms.widgets import EmailInput
from .models import Paciente, Cita, Consulta, Nucleo, Integrante, \
    Contacto, AntecedentesClinicos, UserProfile, CPO, \
    CARDIOVASCULAR_OPCIONES, ENDOCRINOLOGICOS_OPCIONES, \
    NEFROUROLOGICOS_OPCIONES, OSTEOARTICULARES_OPCIONES, SN_OPCIONES, \
    PATIENT_GENDER, Ortodoncia


class IngresoForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password',)


class PacienteForm(ModelForm):
    class Meta:
        model = Paciente
        fields = (
            'documento', 'nombre', 'primer_apellido', 'segundo_apellido',
            'genero', 'direccion', 'ciudad',
            'fecha_nacimiento', 'email',
            'celular',
            'nucleo_activo')

        widgets = {
            'documento': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'primer_apellido': forms.TextInput(
                attrs={'class': 'form-control'}),
            'segundo_apellido': forms.TextInput(
                attrs={'class': 'form-control'}),
            'genero': forms.RadioSelect(choices=PATIENT_GENDER),
            'fecha_nacimiento': DatePickerInput(options={
                "format": "DD/MM/YYYY",  # moment date-time format
                "locale": 'es'
            }),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'ciudad': forms.Select(
                attrs={'class': 'form-control mdb-select md-form'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'celular': forms.TextInput(attrs={'class': 'form-control'}),
            'nucleo_activo': forms.CheckboxInput(
                attrs={'type': 'checkbox', 'class': 'custom-checkbox'}),
            'relacion_nucleo': forms.Select(attrs={'class': 'form-control'}),
        }


class CitaForm(ModelForm):
    class Meta:
        model = Cita
        fields = ('paciente', 'doctor', 'fecha', 'hora')

        widgets = {
            'paciente': forms.Select(
                attrs={'class': 'form-control mdb-select md-form',
                       'searchable': 'Buscar paciente...'}),
            'doctor': forms.Select(
                attrs={'class': 'form-control mdb-select md-form',
                       'searchable': 'Buscar Profesional...'}),
            'fecha': forms.TextInput(attrs={'class': 'form-control'}),
            'hora': forms.TextInput(attrs={'class': 'form-control',
                                           'type': 'time', 'min': '07:00',
                                           'max': '19:00', 'step': '600'}),
        }

    def __init__(self, *args, **kwargs):
        super(CitaForm, self).__init__(*args, **kwargs)
        doctors = UserProfile.objects.filter(user_tipo='DOCTOR')
        self.fields['doctor'].queryset = User.objects.all().filter(
            id__in=doctors.values_list('user_id', flat=True))


class ConsultaForm(ModelForm):
    class Meta:
        model = Consulta
        readonly_fields = 'creado'
        fields = ('paciente', 'diagnostico', 'tratamiento', 'indicaciones')
        widgets = {
            'paciente': forms.Select(
                attrs={'class': 'form-control mdb-select md-form',
                       'searchable': 'Buscar paciente...'}),
            'diagnostico': forms.Textarea(attrs={'class': 'form-control'}),
            'tratamiento': forms.Textarea(attrs={'class': 'form-control'}),
            'indicaciones': forms.Textarea(attrs={'class': 'form-control'}),
        }

class OrtodonciaForm(forms.ModelForm):
    class Meta:
        model = Ortodoncia
        fields = ('tipo','paciente', 'diagnostico', 'tratamiento', 'indicaciones', 'image')
        widgets = {
            'tipo': forms.Select(
                attrs={'class': 'form-control mdb-select md-form'}),
            'diagnostico': forms.Textarea(attrs={'class': 'form-control'}),
            'tratamiento': forms.Textarea(attrs={'class': 'form-control'}),
            'indicaciones': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'paciente': forms.Select(
                attrs={'class': 'form-control mdb-select md-form', 'searchable': 'Buscar paciente...'})
        }




class ConsultaCPOForm(ModelForm):
    class Meta:
        model = CPO
        readonly_fields = 'creado'
        fields = ('paciente', 'contenido_cpo', 'ceod', 'ceos', 'cpod', 'cpos')
        widgets = {
            'ceod': forms.NumberInput(attrs={'class': 'form-control'}),
            'ceos': forms.NumberInput(attrs={'class': 'form-control'}),
            'cpod': forms.NumberInput(attrs={'class': 'form-control'}),
            'cpos': forms.NumberInput(attrs={'class': 'form-control'}),
            'contenido_cpo': forms.NumberInput(
                attrs={'class': 'form-control', 'type': 'hidden'}),
            'paciente': forms.Select(
                attrs={'class': 'form-control mdb-select md-form',
                       'searchable': 'Buscar paciente...'})
        }


class AntecedenteForm(ModelForm):
    class Meta:
        model = AntecedentesClinicos
        fields = ('paciente', 'fumador', 'alcohol', 'coproparasitario',
                  'aparato_digestivo', 'desc_aparato_digestivo',
                  'dermatologicos', 'desc_dermatologicos',
                  'alergias', 'desc_alergias', 'autoinmunes',
                  'desc_autoinmunes', 'oncologicas', 'desc_oncologicas',
                  'hematologicas', 'desc_hematologicas', 'intervenciones',
                  'desc_intervenciones', 'toma_medicacion',
                  'desc_medicacion', 'endocrinometabolico',
                  'desc_endocrinometabolico', 'cardiovascular',
                  'desc_cardiovascular', 'nefrourologicos',
                  'desc_nefrourologicos', 'osteoarticulares',
                  'desc_osteoarticulares', 'observations')

        widgets = {
            'paciente': forms.Select(
                attrs={'class': 'form-control mdb-select md-form',
                       'searchable': 'Buscar paciente...'}),
            'fumador': forms.RadioSelect(choices=SN_OPCIONES),
            'alcohol': forms.RadioSelect(choices=SN_OPCIONES),
            'coproparasitario': forms.RadioSelect(choices=SN_OPCIONES),
            'aparato_digestivo': forms.RadioSelect(choices=SN_OPCIONES),
            'desc_aparato_digestivo': forms.TextInput(
                attrs={'class': 'form-control'}),
            'dermatologicos': forms.RadioSelect(choices=SN_OPCIONES),
            'alergias': forms.RadioSelect(choices=SN_OPCIONES),
            'autoinmunes': forms.RadioSelect(choices=SN_OPCIONES),
            'oncologicas': forms.RadioSelect(choices=SN_OPCIONES),
            'hematologicas': forms.RadioSelect(choices=SN_OPCIONES),
            'intervenciones': forms.RadioSelect(choices=SN_OPCIONES),
            'toma_medicacion': forms.RadioSelect(choices=SN_OPCIONES),
            'endocrinometabolico': forms.CheckboxSelectMultiple(
                choices=ENDOCRINOLOGICOS_OPCIONES),
            'cardiovascular': forms.CheckboxSelectMultiple(
                choices=CARDIOVASCULAR_OPCIONES),
            'nefrourologicos': forms.CheckboxSelectMultiple(
                choices=NEFROUROLOGICOS_OPCIONES),
            'osteoarticulares': forms.CheckboxSelectMultiple(
                choices=OSTEOARTICULARES_OPCIONES),
            'desc_dermatologicos': forms.TextInput(
                attrs={'class': 'form-control'}),
            'desc_alergias': forms.TextInput(attrs={'class': 'form-control'}),
            'desc_autoinmunes': forms.TextInput(
                attrs={'class': 'form-control'}),
            'desc_oncologicas': forms.TextInput(
                attrs={'class': 'form-control'}),
            'desc_hematologicas': forms.TextInput(
                attrs={'class': 'form-control'}),
            'desc_intervenciones': forms.TextInput(
                attrs={'class': 'form-control'}),
            'desc_medicacion': forms.TextInput(
                attrs={'class': 'form-control'}),
            'desc_endocrinometabolico': forms.TextInput(
                attrs={'class': 'form-control'}),
            'desc_cardiovascular': forms.TextInput(
                attrs={'class': 'form-control'}),
            'desc_nefrourologicos': forms.TextInput(
                attrs={'class': 'form-control'}),
            'desc_osteoarticulares': forms.TextInput(
                attrs={'class': 'form-control'}),
            'observations': forms.Textarea(attrs={'class': 'form-control'}),
        }


class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = ('nombre', 'email', 'asunto', 'mensaje')
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'email': EmailInput(attrs={'class': 'form-control'}),
            'asunto': forms.TextInput(attrs={'class': 'form-control'}),
            'mensaje': forms.Textarea(attrs={'class': 'form-control'}),
        }


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
        Si un formulario principal no tiene datos, pero sus formularios
        anidados los tienen, deberíamos devolver un error, porque no podemos
        guardar integrantes sin nucleo
        """
        super().clean()

        for form in self.forms:
            if not hasattr(form, 'nested') or self._should_delete_form(form):
                continue

            if self._is_adding_nested_inlines_to_empty_form(form):
                form.add_error(
                    field=None,
                    error=('Esta tratando de agregar integrantes a un nucleo'
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
        return any(not is_empty_form(nested_form) for nested_form in
                   non_deleted_forms)


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
