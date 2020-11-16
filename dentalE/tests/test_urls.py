from django.test import SimpleTestCase
from django.urls import reverse, resolve
from dentalE.views import agregartratamiento


class TestUrls(SimpleTestCase):

    def test_agregar_tratamiento_url(self):
        url = reverse('agregartratamiento')
        self.assertEquals(resolve(url).func, agregartratamiento)
