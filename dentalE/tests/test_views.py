from django.test import TestCase, Client
from django.urls import reverse
from dentalE.models import UserProfile
from django.contrib.auth.models import User


class TestViews(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = '@lma'
        test_user = User.objects.create(username=self.username)
        test_user.set_password(self.password)
        test_user.save()
        self.client = Client()

    def test_resumendia_GET_error(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('resumendia'))
        self.assertEquals(response.status_code, 404)
        self.assertTemplateUsed(response, 'almaFront/bases/404.html')

    def test_pacientes_GET(self):
        self.username = 'testuser'
        self.password = '@lma'
        user = User.objects.filter(username=self.username).last()
        profile = UserProfile.objects.create(user=user,
                                             user_tipo='DOCTOR',
                                             user_celular='091741852')
        profile.save()
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('resumendia'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'almaFront/secretaria/agenda_hoy.html')
