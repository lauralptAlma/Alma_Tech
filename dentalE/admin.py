from django.contrib import admin
from django import forms
from .models import UserProfile, Consulta, Cita, Paciente, AntecedentesClinicos, Nucleo, Integrante, CPO
import json
import logging
from djongo.models.fields import JSONField
from django.forms import widgets
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Consulta)
admin.site.register(Cita)
admin.site.register(Paciente)
admin.site.register(AntecedentesClinicos)
admin.site.register(CPO)

@admin.register(Nucleo)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('matricula', 'titular',)
    list_display_links = ('matricula',)


@admin.register(Integrante)
class IntegrantesAdmin(admin.ModelAdmin):
    list_display = ('nucleo',  'relacion_nucleo', )
    list_display_links = ('nucleo',)


'''logger = logging.getLogger(__name__)


class PrettyJSONWidget(widgets.Textarea):
    def format_value(self, value):
        try:
            value = json.dumps(json.loads(value), indent=2, sort_keys=True)
            # these lines will try to adjust size of TextArea to fit to content
            row_lengths = [len(r) for r in value.split('\n')]
            self.attrs['rows'] = min(max(len(row_lengths) + 2, 10), 30)
            self.attrs['cols'] = min(max(max(row_lengths) + 2, 40), 120)
            return value
        except Exception as e:
            logger.warning("Error while formatting JSON: {}".format(e))
            return super(PrettyJSONWidget, self).format_value(value)



class JsonAdmin(admin.ModelAdmin):
    formfield_overrides = {
        JSONField
    }


admin.site.register(CPO, JsonAdmin)
'''